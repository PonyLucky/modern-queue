# ModernQueue
A modern and permissive Python queue that returns results in a multithreaded environment.

## Table of contents
- [Features](#features)
- [Installation](#installation)
  - [From PyPI](#from-pypi)
  - [From GitHub](#from-github)
- [Usage](#usage)
  - [Importing](#importing)
  - [Creating a queue](#creating-a-queue)
  - [Adding functions to the queue](#adding-functions-to-the-queue)
  - [Running the queue](#running-the-queue)
  - [Getting the results](#getting-the-results)
  - [Waiting for the queue to finish](#waiting-for-the-queue-to-finish)
- [Examples](#examples)
  - [1)](#1)
  - [2)](#2)
  - [3)](#3)

## Installation
### From PyPI
```bash
pip install modernqueue
```

### From GitHub
Download `modernqueue.py` and put it in your project folder.

## Usage
### Importing
```python
from modernqueue import ModernQueue
```

### Creating a queue
```python
# Create a queue with 4 threads
queue = ModernQueue(max_threads=4)

# Create a queue with no limit on threads
queue = ModernQueue()
```

### Adding functions to the queue
```python
# Add a function to the queue
queue.add(func=print_number, args={'number': 1})

# Add a function to the queue, with tuple arguments
queue.add(func=print_number, args=(1,))
```

### Running the queue
```python
# Run the queue, blocking the function until finished
queue.run()

# Run the queue, without blocking the function
queue.run(is_blocking=False)
```

### Getting the results
```python
# Get the results of the queue, in order
results = queue.get_results()

# Get faster the results of the queue
results = queue.get_results(is_ordered=False)
```

### Waiting for the queue to finish
```python
# Wait for the queue to finish, in blocking mode
queue.run()

# Wait for the queue to finish, in non-blocking mode
queue.run(is_blocking=False)
while queue.running() != 0:
    sleep(0.1)
```

## Examples
### 1)
Simple example of a queue with 4 threads, that prints numbers from 1 to 10, with a 1-second delay between each number.

This one is greatly commented, so you can understand how it works.
```python
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
```

### 2)
Same as above, but with fewer comments.
```python
# waiting for the queue to finish in blocking mode
queue = ModernQueue(max_threads=4)
for i in range(1, 11):
    queue.add(func=print_number, args={'number': i})
queue.run(is_blocking=True)
print("Done")
results = queue.get_results(is_ordered=True)
print(results)

# --- OUTPUT ---
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
```

### 3)
Same as above, but in non-blocking mode.

It will print “Not done yet…” while the queue is running, and “Done” when it's finished. To mark when the process is finished and when it's not in the code.
```python
# waiting for the queue to finish in non-blocking mode
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

# --- OUTPUT ---
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
```

## License
You can use this code however you want, no credit is required.

Though, if you want to give me credit, you can do it by linking to my GitHub profile:
[https://github.com/PonyLucky](https://github.com/PonyLucky)