# Python profiling lab analysis

Fatima Bazzoun

## Purpose and method

This lab compares the original workload with the handout's proposed change to the fast function. Both versions keep the two-second sleep, the 10,000-iteration slow loop, the 100-item fast sum, and the 10,000,000-iteration large loop. All figures below come from saved runs in results/. The terminal screenshots are separate evidence of these runs.

The line-profiling scripts import the corresponding profiler.py functions so they measure the same implementation. The memory-profiling scripts repeat those functions with @profile decorators, as requested. Coverage is deliberately scoped to profiler.py in each version; the figures do not claim coverage of every helper or profiler wrapper.

## cProfile results

| Measurement | Before | After |
| --- | ---: | ---: |
| Total instrumented elapsed time in seconds | 2.844 | 2.842 |

The time.sleep call accounts for about two seconds, while the ten-million-iteration calculation is the main computational cost. The short fast function contributes very little to the complete program. In the report, tottime is time inside the function excluding called functions; cumtime includes callees. Thus the two-second sleep appears separately from slow_function's own time.

cProfile rounds its default time columns to milliseconds, so 0.000 for the fast function does not mean zero execution time. The optimized version also introduces generator calls and builtins.sum. Differences in total duration must be interpreted with normal run-to-run noise in mind, especially because the expensive functions were not changed.

## Line profiler results

| Version | Function | Instrumented function time in seconds |
| --- | --- | ---: |
| Before | slow_function | 2.02103000 |
| Before | fast_function | 0.00012860 |
| Before | memory_intensive_function | 5.39279000 |
| After | slow_function | 2.01475000 |
| After | optimized_fast_function | 0.00009260 |
| After | memory_intensive_function | 4.98817000 |

The slow-function table isolates the deliberate sleep. The large function's loop and total += i ** 2 lines show where the computational work is repeated ten million times. The loop header has 10,000,001 hits because its final termination check is counted. In the optimized fast function, the generator expression appears on one source line; profiling can count multiple events on that line.

Line tracing adds overhead, particularly to loops and generators. Compare before and after within a tool, and use the repeated uninstrumented benchmark below to assess the tiny fast function. Do not compare line-profiler timings directly with plain execution as if the tracing cost were an application regression.

## Memory profiler results

| Version | Largest displayed process RSS in MiB |
| --- | ---: |
| Before | 25.4 |
| After | 25.5 |

Mem usage is the resident memory of the whole process, including the interpreter and imported packages. It is not the size of the local variable alone. The first profiled line's Increment includes the starting RSS baseline and must not be described as memory allocated by @profile. The displayed line measurements have limited precision.

For a line executed repeatedly, memory_profiler 0.61.0 accumulates differences against the previous line's recorded maximum RSS. If the operating system reduces the working set during a long loop, those repeated differences can produce a very large negative Increment total. Such a value is a tracing aggregation artifact, not evidence that the program freed that many MiB. Interpret the Mem usage column and the occurrence counts together; retain the raw output rather than replacing a surprising value.

Despite its name, memory_intensive_function does not retain ten million results: range is lazy and total holds one running integer. The integer grows in bit length, but there is no list whose length grows with the loop. It is primarily a CPU workload. Both fast-function versions also avoid building a list. A generator expression does not by itself establish an RSS reduction compared with the original accumulator. Small differences between separate process runs may reflect interpreter state or allocation reuse rather than the code change.

The long memory-profiling duration is measurement overhead from tracing and querying memory for many line events. It is not the normal execution time of the original calculation.

## Test results and the handout correction

Both versions run three tests, checking the exact numerical results and retaining the handout's timing targets (slow greater than two seconds, fast less than one second, and the large loop less than five seconds). These thresholds depend on the machine and instrumentation; a slow-machine failure should be investigated rather than hidden. time.perf_counter measures elapsed durations with a monotonic timer.

The handout requires RSS after the large function to be greater than RSS before it. That is not a valid correctness property of this accumulator: temporary integers can be freed and existing memory can be reused. Both test files therefore print before/after RSS and the delta, check that the readings are positive, and verify the exact sum 333333283333335000000. This documented correction is applied equally before and after optimization.

## Coverage results

| Version | Statements | Missing | Statement coverage | Unexecuted lines |
| --- | ---: | ---: | ---: | --- |
| Before | 23 | 4 | 82.61% | 35, 36, 37, 41 |
| After | 20 | 4 | 80.00% | 29, 30, 31, 35 |

The tests call the three calculation functions directly. They do not call the three statements inside main or the call to main beneath the script entry guard; those are the four unexecuted statements in each version. They remain visible instead of being excluded or artificially marked as executed. The optimized source has fewer executable statements, so the same four missed statements yield a lower percentage. This percentage change does not show that the arithmetic functions lost coverage. Statement coverage also does not prove that every behavior or test assertion is adequate. The complete HTML directories are included so index.html can load its stylesheet, scripts, and source pages.

## Optimization and repeated timing

The explicit fast-function accumulator was replaced by optimized_fast_function, implemented as sum(i ** 2 for i in range(100)), exactly as proposed in the handout. The after-version main function, line profiler, memory profiler, and test suite all call the renamed function. Both implementations return 328350.

The uninstrumented benchmark used 7 alternating-order rounds and 50,000 calls per function in each round. Median time was 5.377 microseconds per call before and 6.643 microseconds per call after. The measured runtime reduction was -23.55%; a negative value means the proposed version was slower.

On this run the proposed generator version was slower for this short function. Using sum with a generator changes iteration and function-call overhead; it does not remove the 100 square operations. The result is specific to this interpreter, machine, and run. Because the two-second delay and the much larger calculation are unchanged, this small edit cannot remove the full program's dominant costs.

## Tool references

- Python cProfile: https://docs.python.org/3/library/profile.html
- line_profiler: https://kernprof.readthedocs.io/en/release/manual/legacy_readme.html
- memory_profiler: https://pypi.org/project/memory-profiler/
- coverage.py: https://coverage.readthedocs.io/en/latest/
