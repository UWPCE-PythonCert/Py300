#!/usr/bin/python

"""
Trivial example of a race condition...
"""

import time
import threading
import random

# A global data structure
storage = []


def add_numbers(nums):

    # put them in storage
    storage.extend(nums)

    # add them up
    total = 0
    for i in range(len(nums)):
        time.sleep(0.0)
        total += storage.pop()
    return total

# bunch of examples:
numbers_to_add = [(1, 4, 2, 3, 5, 7),
                  (3, 1, 3),
                  (8, 2, 9, 4, 8),
                  (3, 8, 4, 8, 2),
                  ]


def make_lots(n):
    for i in range(n):
        nums = tuple((random.randint(0, 100) for i in range(1000)))
        numbers_to_add.append(nums)
    return numbers_to_add


def check_results(results):
    print("checking results of {} summations".format(len(results)))
    for nums, total in results.items():
        assert total == sum(nums), "It did not add up!"


def compute_sequential(numbers_to_add):
    # regular old sequential operation:
    seq_results = {}
    for nums in numbers_to_add:
        seq_results[nums] = add_numbers(nums)

    # print(seq_results)
    check_results(seq_results)
    print("It worked sequentially")


t_results = {}


def thread_operation(nums):
    """
    This computes the result, and puts it in the result dict.
    """
    # print("computing: {}".format(nums))
    #time.sleep(5)
    t_results[nums] = add_numbers(nums)
    # print(t_results)


def compute_threads(numbers_to_add):
    # now with threads
    seq_results = {}
    threads = []
    for nums in numbers_to_add:
        t = threading.Thread(target=thread_operation, args=(nums,),)
        t.start()
        threads.append(t)
    print("done starting all the threads")
    # now make sure they are all done to check results
    for t in threads:
        t.join()
        print("thread: {} is done".format(t.name))
    print("threads are all done")
    seq_results[nums] = add_numbers(nums)

    # print(t_results)
    check_results(t_results)
    print("It worked with threads")


if __name__ == "__main__":
    compute_sequential(numbers_to_add)
    compute_threads(numbers_to_add)

    # # now try with a larger dataset
    # nta = make_lots(10)
    # print("computing with large dataset")
    # compute_threads(nta)

