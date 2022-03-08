import os

os.nice(10)  # ensures that this process and all of its children are low priority.


def add_numbers(number_a: int, number_b: int):
    # This is a trivial example, but subprocess would be very useful here.
    return number_a + number_b
