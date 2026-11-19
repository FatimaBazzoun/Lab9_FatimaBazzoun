"""Original Lab 9 workload, with the handout's formatting repaired."""

import time


def slow_function():
    """Wait two seconds, then sum the squares from 0 through 9,999."""
    time.sleep(2)
    total = 0
    for i in range(10000):
        total += i ** 2
    return total


def fast_function():
    """Sum the squares from 0 through 99 with an explicit loop."""
    total = 0
    for i in range(100):
        total += i ** 2
    return total


def memory_intensive_function():
    """Run the handout's ten-million-iteration workload.

    Despite its name, this accumulates one integer rather than storing a list.
    """
    total = 0
    for i in range(10000000):
        total += i ** 2
    return total


def main():
    slow_function()
    fast_function()
    memory_intensive_function()


if __name__ == "__main__":
    main()
