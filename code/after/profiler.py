"""Lab 9 after replacing fast_function with the handout's sum generator."""

import time


def slow_function():
    """Keep the original two-second delay and 10,000 iterations."""
    time.sleep(2)
    total = 0
    for i in range(10000):
        total += i ** 2
    return total


def optimized_fast_function():
    """Use the optimization proposed in the handout; measure its impact."""
    return sum(i ** 2 for i in range(100))


def memory_intensive_function():
    """Keep all ten million iterations for a like-for-like comparison."""
    total = 0
    for i in range(10000000):
        total += i ** 2
    return total


def main():
    slow_function()
    optimized_fast_function()
    memory_intensive_function()


if __name__ == "__main__":
    main()
