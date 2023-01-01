# __main__.py

from time import sleep
from .modernqueue import ModernQueue


# Define the function to run
def print_number(number: int) -> int:
    """
    Print a number and sleep for 1 second.

    Args:
    - number (int): The number to print.

    Returns:
    - (int) The number multiplied by 2.
    """
    sleep(1)
    print(number)
    return number * 2

def main():
    # Create the queue, with a maximum of 4 threads
    #
    # max_threads is optional and defaults to -1 (no limit)
    queue = ModernQueue(max_threads=4)

    # Add the functions to the queue
    for i in range(1, 11):
        # There are 2 ways to pass arguments to the function
        # 1. As a dict (kwargs):
        queue.add(func=print_number, args={'number': i})
        # 2. As a tuple (args):
        # queue.add(func=print_number, args=(i,))

    # Run the queue, blocking the function until finished
    # is_blocking is optional and defaults to True
    queue.run(is_blocking=True)

    # Print "Done", if the function is blocking
    # This will be printed after all the numbers are printed
    print("Done")

    # Get the results of the queue
    # 
    # If you don't want to take the processing time to sort the results,
    # set is_ordered to False
    # 
    # is_ordered is optional and defaults to True
    results = queue.get_results(is_ordered=True)
    print(results)

    # EXEMPLE 1
    # waiting for the queue to finish in blocking mode
    print("\nEXEMPLE 1")
    queue = ModernQueue(max_threads=4)
    for i in range(1, 11):
        queue.add(func=print_number, args={'number': i})
    queue.run(is_blocking=True)
    print("Done")
    results = queue.get_results(is_ordered=True)
    print(results)

    # EXEMPLE 2
    # waiting for the queue to finish in non-blocking mode
    print("\nEXEMPLE 2")
    queue = ModernQueue(max_threads=4)
    for i in range(1, 11):
        queue.add(func=print_number, args={'number': i})
    queue.run(is_blocking=False)
    print("Not done yet...", f"({queue.running()} threads running)")
    while queue.running() != 0:
        sleep(0.1)
    print("Done")
    results = queue.get_results(is_ordered=True)
    print(results)

if __name__ == "__main__":
    main()

# --- OUTPUT ---
# 4
# 2
# 3
# 1
# 5
# 7
# 6
# 8
# 9
# 10
# Done
# [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# EXEMPLE 1
# 1
# 3
# 2
# 4
# 5
# 7
# 6
# 8
# 9
# 10
# Done
# [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# EXEMPLE 2
# 1
# 3
# 2
# 4
# 5
# 7
# 6
# 8
# Not done yet... (2 threads running)
# 9
# 10
# Done
# [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
