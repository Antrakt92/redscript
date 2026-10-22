# Building the Windows community prerelease

Use Rust 1.89.0 and the x86_64-pc-windows-gnu toolchain with a compatible MinGW-w64
linker. The tested linker is w64devkit. This is a Windows-only distribution.
Python 3.11 or newer packages the archive without additional Python dependencies.

```text
cargo build --locked --workspace --exclude scc-lib-tests
cargo test --locked --workspace --exclude scc-lib-tests
cargo clippy --locked --workspace --exclude scc-lib-tests --all-targets
cargo build --locked --release -p redscript-cli -p scc-lib -p scc --features mmap,popup
python resources/package-community.py --output target/redscript-0.5.31-cp25.1-windows.zip
```

If CARGO_TARGET_DIR is overridden, pass the same directory to the packager using
--target-dir. Build from a clean committed checkout. The packager records the
source commit, member hashes and version, uses fixed ZIP metadata and rejects
unexpected input layout. It does not modify the game, install mods or publish.

The separate scc-lib-tests suite requires libclang. Install it in a developer
build environment to run the original generated C ABI tests. The published
release also has independent DLL/API checks with error popups disabled, plus
official REDmod SCC interoperability and a minimal in-game test. These do not
replace full-collection, cross-platform or exhaustive malformed-input coverage.

The archive includes the original redscript MIT licence, dependency notices,
Rust library copyright/licence texts and the MinGW-w64 runtime notices. Dependency
notices were assembled from the locked Windows normal/build graph with mmap and
popup enabled. Crate-provided licence texts were used; missing workspace licences
were obtained from the packages' pinned upstream source. The Rust notice comes
from the tested 1.89.0 toolchain. Regenerate the notices when changing dependencies
or toolchain components. Do not include game caches, decompiled game source or
other mod packages in release archives.
