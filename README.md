# redscript — unofficial Cyberpunk 2077 2.5 compatibility build

Compile redscript mods on Cyberpunk 2077 2.5 for Windows PC. This experimental
build adapts redscript v0.5.31 to the game's updated full script-cache format.

**[Download 0.5.31-cp25.2 for Windows x64](https://github.com/Antrakt92/redscript/releases/tag/v0.5.31-cp25.2)**

**Install this instead of the official redscript package, not alongside it.**
Keep one redscript compiler enabled in your mod manager.

## What changes

Compared with official redscript v0.5.31:

- Reads the additional table used by 2.5 full script bundles and writes matching
  table counts, offsets and checksums after compiling mods. Legacy bundles remain supported.
- Preserves an unchanged extended bundle byte for byte and rejects unsupported
  external patch bundles with an explicit error.
- Corrects the compiler's signature marker for the 2.5 native loader.
- Finishes serialization before opening the output file. A serialization failure
  therefore leaves an existing output intact; writes are not atomic once they start.
- Refreshes reviewed dependencies and adapts the engine command-line parser,
  including a working `--help`. Some dependency upgrades remain deferred.
- Fixes the DLL error-copy API writing into a buffer whose declared capacity is zero
  (added in 0.5.31-cp25.2).

This is a compatibility fork maintained by Antrakt92. The original compiler is
by [jac3km4 and contributors](https://github.com/jac3km4/redscript).
The format changes have been submitted as [upstream PR #203](https://github.com/jac3km4/redscript/pull/203).
This is one community contribution; other contributors are also working on 2.5 support.
Move back to a supported official release when it includes the required fixes.

## Installation

For **Cyberpunk 2077 2.5, Windows x64**. Other mods and frameworks must support
your game version separately. This package includes the compiler and its configuration;
it does not bundle RED4ext, Codeware, ArchiveXL, CET or gameplay mods.
For REDmod integration, use a compatible RED4ext release as documented by upstream.

1. Close the game.
2. Download `redscript-0.5.31-cp25.2-windows.zip` from the release's **Assets**.
   GitHub's automatic “Source code” downloads are for developers.
3. In Vortex, disable the existing redscript package, install this ZIP from file,
   enable it and deploy. Do not leave both packages enabled.
4. Fully restart the game. Check `r6/logs/redscript_rCURRENT.log` for
   `Compilation complete` and `Output successfully saved`.

For manual installation, back up the existing redscript files and extract the ZIP
into the game folder. You should have `engine/tools/scc.exe` and
`engine/tools/scc_lib.dll` inside that folder, without an extra nested game directory.
Use one installation method. The ZIP's SHA-256 is supplied in `SHA256SUMS.txt`.

To return to the official build through Vortex, disable this package, enable a
supported official redscript package and deploy. With a manual install, remove
this package's four compiler/configuration files and its `redscript-community`
documentation directory, then install the complete supported official package.
Do not delete shared script folders or restore cache backups from another game patch.
The exact package file list is in `BUILD-MANIFEST.json` on the release page.

## Compatibility and testing

The 2.5 compiler changes were tested in a minimal profile with RED4ext 1.30.0 and
an unreleased Auto Continue 1.1.2 build: compilation, save loading, automatic final
confirmation and a rendered game world. That game run used the preceding DEV2
build. The public cp25.2 binaries have separate isolated DLL/CLI and official
REDmod SCC interoperability checks; the exact public ZIP has not been retested
in the running game. The cp25.2 runtime change is the zero-capacity error-buffer guard.

The local suite passes **6232 tests** and Clippy, excluding the bindgen-based
`scc-lib-tests` suite because libclang is unavailable. Stable formatting checks pass
with nightly-only options ignored. This is not full collection or cross-platform validation.

Mods using changed game APIs and native plugins may still need their own updates.
A compiler update does not establish compatibility for those mods. No performance
improvement is claimed.

## Known limits and troubleshooting

- External patch bundles requiring a separate precompiled base are unsupported.
  Normal compilation is checked against the pristine full game cache. Other nonzero
  producer linkage fields are not fully understood.
- The flexstr 0.11 migration and optional non-Windows GTK advisory matches remain
  unresolved. This is a Windows-only distribution, not an all-platform dependency cleanup.
- Existing parser/FFI paths have not received exhaustive malformed-input or fuzz testing.
  Output writes are not crash-safe transactions.

If compilation fails, keep the error log and report your game version, this build's
version, other frameworks and steps to reproduce in
[this fork's issues](https://github.com/Antrakt92/redscript/issues).
Do not share private saves or account information. Report fork-specific failures here
so they can be separated from upstream issues.

## Source, credits and permissions

The original **MIT licence remains unchanged**. The download includes third-party,
Rust and MinGW runtime notices. No additional Donation Points or custom reuse
conditions apply to this fork.

[Technical changes and limits](COMPATIBILITY-2.5.md) ·
[Build and packaging instructions](BUILD-COMMUNITY.md) ·
[Original v0.5.31 developer documentation](https://github.com/jac3km4/redscript/blob/v0.5.31/README.md)

AI tools were used to write and review the compatibility changes and documentation.
Third-party components retain their original credits and licences.
