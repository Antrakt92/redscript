# redscript 0.5.31-cp25.1 — experimental Windows 2.5 compatibility

Unofficial compatibility build by Antrakt92, based on redscript v0.5.31 by
jac3km4 and contributors. The original MIT licence is included unchanged.
Source: https://github.com/Antrakt92/redscript
Upstream contribution: https://github.com/jac3km4/redscript/pull/203
Official project: https://github.com/jac3km4/redscript

## Scope

This Windows x64 prerelease adds support for full script bundles from Cyberpunk
2077 2.5. It also refreshes dependencies and retains engine CLI argument behavior.
It is intended as a temporary replacement while upstream reviews compatibility.
Use a supported official release when it includes the necessary fixes.

This is not a general fix for every mod broken by 2.5. Mods using changed game
APIs or native frameworks may need their own updates. The verified runtime scene
is a minimal profile with RED4ext 1.30.0 and an unreleased Auto Continue 1.1.2 test
build: startup compilation, save loading, one automatic final confirmation and a
rendered game world. Full collections and other platforms are not verified.

## Install

Close the game. In Vortex, disable the existing redscript package, install this
ZIP from file, enable it and deploy. Keep one compiler enabled. Do not install
this as an additional dependency alongside the official redscript package.

For a manual installation, keep a backup of the existing redscript files, then
extract this ZIP into the game root. The files engine/tools/scc.exe and
engine/tools/scc_lib.dll must end up inside that installation, not a second
nested Cyberpunk 2077 directory. Do not install a second copy through a manager.

The package does not include RED4ext, Codeware, CET, ArchiveXL, game caches or
other mods. For a REDmod setup, use a compatible RED4ext release as documented
by upstream. Each mod's other requirements remain its own responsibility.

## Verify and revert

Check r6/logs/redscript_rCURRENT.log after a full game restart. A successful run
reports Compilation complete and Output successfully saved. Preserve the error
log if compilation fails; do not share private save files or account information.

To return to upstream, disable this package and enable a supported official
redscript build, then deploy. Do not leave both enabled. Do not restore a script
cache backup from a different game patch. Keep the previous package for rollback.

## Known limits

External patch bundles that require a precompiled-base resolver are unsupported;
compile against the pristine full game cache. Nonzero producer linkage fields
are not fully understood. Windows-only distribution: optional non-Windows GTK
advisory matches are not fixed here. flexstr 0.11 ownership/API migration is deferred.
No performance improvement or universal compatibility is claimed.

The local suite passed 6231 tests and Clippy excluding scc-lib-tests, which needs
libclang. The exported DLL was checked independently with compiler error popups
disabled. Official REDmod SCC accepted 2.5 outputs in LoadAndSave and functional
comparison checks. See COMPATIBILITY-2.5.md in the source for the format scope.

The native game smoke test used the preceding DEV2 build. All 46 Rust source
files and the registry/git dependency pins match this version; the public version
changes package metadata and documentation. The final release DLL/CLI also pass
separate isolated API and official-SCC checks. Exact public ZIP installation in
other users' profiles remains prerelease testing.
