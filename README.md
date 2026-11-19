# Python profiling lab

Fatima Bazzoun | Software Tools Lab 9

This lab compares execution time, memory usage, and test coverage before and after replacing the fast function's loop with a `sum` generator expression.

## Files

- `code/before/`: original functions, line profiler, memory profiler, and tests.
- `code/after/`: optimized functions and corresponding profiling scripts and tests.
- `screenshots/`: terminal and coverage screenshots for both versions.
- `results/`: profiling output, test results, HTML coverage reports, and the fast-function timing comparison.
- `report/analysis.md`: analysis of the measured results.
- `requirements.txt`: Python dependencies.
- `submission.txt`: GitHub repository link.

## Running the code

Install the dependencies from the repository root:

```text
python -m pip install -r requirements.txt
```

Enter `code/before` or `code/after`, then run:

```text
python -m cProfile -s time profiler.py
python profiler_lineprofiler.py
python -m memory_profiler profiler_memoryprofiler.py
python -m unittest discover -v
python -m coverage run -m unittest discover -v
python -m coverage report -m
python -m coverage html
```

Full memory profiling includes all 10,000,000 iterations and takes several minutes. The saved HTML reports can be opened through `results/before/htmlcov/index.html` and `results/after/htmlcov/index.html`.

## Results and test notes

The optimized fast function uses `sum(i ** 2 for i in range(100))`. The other workloads are unchanged. In the saved repeated timing comparison, the generator version was slower than the original loop.

Each version has three tests that check return values and the assignment's timing targets. The tests record RSS before and after the large calculation. They check positive memory readings rather than requiring RSS to increase after the function returns, since memory can be reused or released.

Coverage is measured for `profiler.py`. The tests call the calculation functions directly, leaving the calls inside `main()` and the script entry-point call unexecuted. The analysis explains the measured timings, memory-profiler increments, and coverage gaps.
