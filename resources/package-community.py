"""Package a clean, locally built Windows community release without publishing."""

import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tomllib
import zipfile


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target-dir", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    status = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=root, text=True
    )
    if status.strip():
        raise SystemExit("Commit the intended source changes before packaging.")
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True
    ).strip()
    version = tomllib.loads((root / "Cargo.toml").read_text())["workspace"]["package"]["version"]
    target = args.target_dir or root / "target"
    inputs = {
        "engine/tools/scc.exe": target / "release/scc.exe",
        "engine/tools/scc_lib.dll": target / "release/scc_lib.dll",
        "engine/config/base/scripts.ini": root / "resources/mod/windows/engine/config/base/scripts.ini",
        "r6/config/cybercmd/scc.toml": root / "resources/mod/windows/r6/config/cybercmd/scc.toml",
        "redscript-community/LICENSE": root / "LICENSE",
        "redscript-community/COMPATIBILITY-2.5.md": root / "COMPATIBILITY-2.5.md",
    }
    community = root / "resources/community"
    for path in sorted(community.rglob("*")):
        if path.is_symlink():
            raise SystemExit("Symbolic links are not release inputs.")
        if path.is_file():
            inputs["redscript-community/" + path.relative_to(community).as_posix()] = path
    payload = {}
    for name, path in inputs.items():
        if path.is_symlink() or not path.is_file():
            raise SystemExit(f"Missing or non-regular release input: {name}")
        payload[name] = path.read_bytes()
    for name in ("engine/tools/scc.exe", "engine/tools/scc_lib.dll"):
        data = payload[name]
        if len(data) < 64 or data[:2] != b"MZ":
            raise SystemExit(f"Not a PE binary: {name}")
        offset = struct.unpack_from("<I", data, 60)[0]
        if offset + 6 > len(data) or data[offset:offset + 4] != b"PE\0\0":
            raise SystemExit(f"Invalid PE header: {name}")
        if struct.unpack_from("<H", data, offset + 4)[0] != 0x8664:
            raise SystemExit(f"Not Windows x64: {name}")
    info = {
        "version": version,
        "source": "https://github.com/Antrakt92/redscript",
        "sourceCommit": commit,
        "cargoLockSha256": sha256((root / "Cargo.lock").read_bytes()),
        "platform": "windows-x86_64",
        "prerelease": True,
        "members": {name: sha256(data) for name, data in sorted(payload.items())},
    }
    payload["redscript-community/BUILD-INFO.json"] = (
        json.dumps(info, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    output = args.output.resolve()
    if not output.parent.is_dir():
        raise SystemExit("The output directory must already exist.")
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(payload.items()):
            member = zipfile.ZipInfo(name, date_time=(2000, 1, 1, 0, 0, 0))
            member.create_system = 3
            member.external_attr = 0o100644 << 16
            member.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(member, data, compresslevel=9)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise SystemExit("Archive CRC verification failed.")
        actual = {name: archive.read(name) for name in archive.namelist()}
        if actual != payload:
            raise SystemExit("Archive members differ from the release inputs.")
    print(json.dumps({
        "archive": str(output),
        "version": version,
        "sourceCommit": commit,
        "members": len(payload),
        "size": output.stat().st_size,
        "sha256": sha256(output.read_bytes()),
    }, indent=2))


if __name__ == "__main__":
    main()
