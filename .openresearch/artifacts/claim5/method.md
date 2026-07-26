# Claim 5 method

`source_scope_audit()` records the source hash, all substantive section groups,
and the absence of an empirical benchmark or training protocol.
`repro/run_audit.py` emits the record on every cumulative run, and the pytest
suite checks that Claim 5 remains present.
