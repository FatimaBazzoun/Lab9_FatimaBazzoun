"""Apply the same checks after replacing the fast function everywhere."""

import time
import unittest
import memory_profiler
from profiler import memory_intensive_function, optimized_fast_function, slow_function


class TestProfiler(unittest.TestCase):
    def time_function(self, func):
        start_time = time.perf_counter()
        result = func()
        return time.perf_counter() - start_time, result

    def test_slow_function(self):
        duration, result = self.time_function(slow_function)
        print(f"\nslow_function: {duration:.6f} seconds; result={result}")
        self.assertEqual(result, 333283335000)
        self.assertGreater(duration, 2, "The original two-second sleep is retained.")

    def test_optimized_fast_function(self):
        duration, result = self.time_function(optimized_fast_function)
        print(f"\noptimized_fast_function: {duration:.9f} seconds; result={result}")
        self.assertEqual(result, 328350)
        self.assertLess(duration, 1, "Handout timing target: less than one second.")

    def test_memory_intensive_function(self):
        before = memory_profiler.memory_usage(-1, interval=0.01, timeout=0.01)[0]
        duration, result = self.time_function(memory_intensive_function)
        after = memory_profiler.memory_usage(-1, interval=0.01, timeout=0.01)[0]
        print(f"\nmemory_intensive_function: {duration:.6f} seconds; result={result}")
        print(f"RSS before: {before:.3f} MiB; after: {after:.3f} MiB; delta: {after-before:+.3f} MiB")
        print("RSS is observed, not required to increase after the function returns.")
        self.assertEqual(result, 333333283333335000000)
        self.assertLess(duration, 5, "Handout timing target: less than five seconds (machine dependent).")
        # Same correction as the baseline; do not assume a positive RSS delta.
        self.assertGreater(before, 0)
        self.assertGreater(after, 0)


def main():
    unittest.main(verbosity=2)


if __name__ == "__main__":
    main()
