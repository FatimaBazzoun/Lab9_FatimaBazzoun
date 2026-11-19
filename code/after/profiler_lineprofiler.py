"""Line-by-line timing of the optimized version of profiler.py."""

from line_profiler import LineProfiler
from profiler import (
    main,
    memory_intensive_function,
    optimized_fast_function,
    slow_function,
)


def profile_main():
    profiler = LineProfiler()
    profiler.add_function(slow_function)
    profiler.add_function(optimized_fast_function)
    profiler.add_function(memory_intensive_function)
    profiler.runcall(main)
    profiler.print_stats(output_unit=1e-6)


if __name__ == "__main__":
    profile_main()
