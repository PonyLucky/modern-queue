"""
A queue that returns results in a multithreaded environment.
"""

from threading import Thread, active_count
from time import sleep


class ModernQueue:
    """
    A queue that returns results in a multithreaded environment.
    """
    def __init__(self, max_threads: int = -1):
        """
        A queue that returns results in a multithreaded environment.

        Args:
        - max_threads (int, optional): The maximum number of threads
        to run at once [-1 for no limit]. Default: -1
        """
        # If max_threads is 0, throw an error
        if max_threads == 0:
            raise ValueError("max_threads can't be 0")
        # The maximum number of threads to run at once
        self.max_threads = max_threads
        # The list of threads
        self.threads = []
        # The queue of functions to run
        self.queue = []
        # The results of the functions
        self.results = []
        # The index of the function in the queue
        self.index = 0

    def _wrapper(self, func: any, args: any, index: int) -> None:
        """
        A wrapper for the function to run.
        We need this to get the result of the function.

        Args:
        - func (callable): The function to run.
        - args (dict|tuple): The arguments to pass to the function.
        - index (int): The index of the function in the queue.
        """
        # Run the function and get the result
        # If args is a tuple, use *args
        # If args is a dict, use **args
        if isinstance(args, tuple):
            self.results.append((index, func(*args)))
        elif isinstance(args, dict):
            self.results.append((index, func(**args)))

    def add(self, func: any, args: any) -> None:
        """
        Add a function to the queue.

        There are 2 ways to pass arguments to the function:
        - args: A tuple of arguments (value1, value2, ...)
        - args: A dict of arguments {'arg1': value1, 'arg2': value2, ...}

        The 'dict' way is recommended because it's easier to read and understand.
        
        Args:
        - func (callable): The function to run.
        - args (dict|tuple): The arguments to pass to the function.
        """
        # If the function is not callable, throw an error
        if not callable(func):
            raise TypeError("func must be callable")
        # If args is not a tuple or a dict, throw an error
        if not isinstance(args, (tuple, dict)):
            raise TypeError("args must be a tuple or a dict")
        # Add the function to the queue
        self.queue.append((self._wrapper, (func, args, self.index)))
        # Increment the index
        self.index += 1

    def run(self, is_blocking: bool = True) -> None:
        """
        Run the queue.

        Args:
        - is_blocking (bool, optional): If True, the function will block until
        the queue is finished. Default: True
        """
        # While there are still functions in the queue
        while self.queue:
            if self.max_threads != -1:
                # If there are too many threads, wait
                while active_count() > self.max_threads:
                    sleep(0.1)
            # Get the next function in the queue
            func, args = self.queue.pop(0)
            # Run the function in a new thread
            thread = Thread(target=func, args=args)
            thread.start()
            # Add the thread to the list of threads
            self.threads.append(thread)

        if is_blocking:
            # If the function is blocking, wait for all threads to finish
            for thread in self.threads:
                thread.join()

    def get_results(self, is_ordered: bool = True) -> list:
        """
        Get the results of the queue in order.

        If order don't matter, is_ordered can be set to False to improve
        performance.

        Args:
        - is_ordered (bool, optional): If True, the results will be sorted.
        Default: True

        Returns:
        - (list) A list of results.
        """
        # self.results is a list of tuples (index, result)
        if is_ordered:
            # We sort the list by the index and return the results only
            return [res[1] for res in sorted(self.results, key=lambda x: x[0])]
        else:
            # Return the results only
            return [res[1] for res in self.results]

    def running(self) -> int:
        """
        Get the number of threads running.

        Returns:
        - (int) The number of threads running. 0 if the queue is finished.
        """
        return active_count() - 1
