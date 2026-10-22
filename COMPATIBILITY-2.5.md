# Experimental Cyberpunk 2077 2.5 full-bundle compatibility

Based on redscript v0.5.31 by jac3km4 and contributors, under the original MIT
licence. This is an unofficial compatibility contribution, not an upstream release.

The 2.5 format keeps version 14 but adds header flag 0x2 and a seventh table
header. There is one 12-byte linkage record per definition, including index zero.
The reader follows stored table offsets and validates linkage count, bounds and
CRC. Unchanged bundles preserve their bytes; edited full bundles regenerate zero
linkage rows with matching counts and checksums. Legacy layout is retained.
External patch linkage (row bit 0) needs resolution against a precompiled base;
this patch rejects it explicitly. Other nonzero producer fields are not fully
understood, so this is not a general patch-bundle implementation.

The SCC signature enum uses four-byte storage, accepted by the official 2.5
REDmod compiler. Serialization finishes before output files are opened, so a
serialization failure does not truncate an existing output file. This does not
make filesystem writes atomic after they start.

## Validation

Synthetic tests cover legacy writing, unchanged extended byte preservation,
definition growth, invalid linkage bounds/count/CRC and external-patch rejection.
No new game cache, decompiled game code or proprietary mod source is included.
The tests build extended input from the existing upstream predef fixture.

Independent local Windows checks also exercised the exported DLL API, compilation
against a pristine 2.5 cache, and official SCC LoadAndSave plus functional compare.
New classes, fields, added methods, wrappers and replacements survived those
format checks. Invalid input preserved the original cache and an existing CLI
output sentinel. A minimal game run of the preceding DEV2 build compiled and loaded Auto Continue 1.1.2,
confirmed the final loading prompt automatically and reached the rendered world.
These checks do not establish full-collection or other framework compatibility.

## Local checks

```text
cargo build --locked -p redscript-cli -p scc-lib -p scc
cargo test --locked --workspace --exclude scc-lib-tests
cargo clippy --locked --workspace --exclude scc-lib-tests --all-targets
cargo fmt --all -- --check
```

The bindgen-based scc-lib-tests suite needs libclang. Exported DLL behavior was
also exercised independently with compiler error popups disabled. The stable
formatter ignores this repository's nightly-only formatting options.

## 0.5.31-cp25.2 follow-up audit

A direct call to the cp25.1 release DLL reproduced an inherited error-copy bug:
`scc_copy_error` wrote 290 bytes plus its terminator despite a declared buffer
capacity of zero. The probe deliberately allocated a larger physical buffer to
observe the contract violation without an actual out-of-allocation write.

The function now returns zero without accessing the pointer for zero capacity.
The safety contract explicitly permits a null pointer in that case. Tests cover
zero, one, truncated and sufficient capacities, termination and guard bytes.
The external ABI and ordinary nonzero-buffer behavior are unchanged. This is a
narrow correction, not general FFI panic containment or exhaustive parser hardening.
The exact cp25.2 public binaries have isolated checks; they have not been run in-game.
