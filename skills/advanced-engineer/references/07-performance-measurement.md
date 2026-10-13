# Performance measurement

Use before deciding from a performance comparison or reporting a measured improvement. For a requested rough estimate, label a single run as such and still check output correctness and completed work.

## Establish a valid comparison

State the claim, workload, metric, and acceptable regression conditions before changing code. Read the harness to identify what it times and what it excludes.

- Use realistic data sizes, state, and concurrency that reproduce the complaint.
- Compare equivalent work with comparable builds, versions, production settings, and cache conditions. If configurations differ intentionally, name that difference in the claim.
- Count errors and completed work. Check actual outputs; fast rejection, skipped rows, unawaited promises, or unconsumed results can look like speedups.
- Capture a baseline before the change. If the harness cannot distinguish a known meaningful workload difference, investigate its sensitivity first.

## Separate improvement from noise

Interleave baseline and treatment runs so machine load, warmup, and drift do not favor one side. Choose the sample count from variability, measurement cost, and the decision's required confidence. Record a representative value, spread, and sample count; do not claim a difference below observed noise.

Profile separately from reported timing. Identify the limiting resource or code path and relate it to source. Check whether the result fits resource limits and the fraction of total time affected. A component taking 10% of a request cannot save more than that share by itself.

For a microbenchmark, also examine the end-to-end path the user waits on. If causal attribution is uncertain, report the measured change with that limit rather than inventing a bottleneck.

## Run one hypothesis at a time

Prefer eliminating unused work, then avoiding repetition or reducing frequency, before making each operation cheaper. Keep the measurement method fixed across an experiment. If it was wrong, correct it and recapture the baseline.

Make one change, measure, and run the relevant behavior checks. Retain changes supported by evidence; revert ineffective experiments. Stop when the agreed target is met or remaining ideas do not justify their cost. Do not manufacture an iteration quota or weaken the target to claim success.

Report the workload, before and after values with units, sample count and spread, error/work counts, and evidence location. Distinguish faster, slower, no measurable difference, and inconclusive.

Adapted from Lauren Tan's pstack benchmark-checklist, explain-the-number, and performance playbooks.
