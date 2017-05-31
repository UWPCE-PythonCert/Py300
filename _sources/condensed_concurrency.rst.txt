:orphan:

.. _concurrency:

######################
Concurrent Programing
######################

What does it mean to do something in parallel?

 - Parallelism is about doing things at the same time; 
 - Concurrency is about dealing with mulitple things at the same time.
 - Parallelism needs concurrency, but concurrency need not be in parallel.


Whirlwind Tour of Concurrency
==============================

Concurrency:

Having different code running at the same time, or kind of the same time.

Asynchrony:

The occurrence of events independent of the main program flow and ways to deal with such events.

Asynchrony and Concurrency are really two different things -- you can do either
one without the other -- but they are closely related, and often used together.
They solve different problems, but the problems and the solutions overlap.


https://vimeo.com/49718712

Despite Rob Pike using an example about burning books, I recommend listening to
at least the first half of his talk.

In "Concurrency is not parallelism" Rob Pike makes a key point:
Breaking down tasks into concurrent subtasks only allows parallelism,
it’s the scheduling of these subtasks that creates it.


Types of Concurrency
--------------------

Multithreading:

what is a thread?

Multiprocessing:

what is a process?


Lots of different packages both in the standard library and 3rd party libaries.

How to know what to choose?

- IO bound vs. CPU bound
- event driven cooperative multitasking vs preemptive multitasking
-callbacks vs coroutines + scheduler/event loop


Concurrency in the standard library:
------------------------------------

 - threading: processing is interweaved to get more done (doing dishes while taking a break from cooking)
   - sched: Scheduler, safe in mulit-threaded enivoronments
   - queue: The queue module implements multi-producer, multi-consumer queues. It is especially useful in threaded programming when information must be exchanged safely between multiple threads. 
 - multiprocessing: processing is parallel (someone else does the dishes while you cook)
   - subprocess: (replaces os.system, os.spawn) allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.  parallel, hands to OS
 - concurrent.futures: https://www.blog.pythonlibrary.org/2016/08/03/python-3-concurrency-the-concurrent-futures-module/ This is also in the asyncio package, and we go into it in more depth there)


Concurrency outside the standard library:

 - Celery + Rabbitmq
 - Redis + RQ
 - Twisted


Advantages / Disadvantages of Threads
--------------------------------------

Advantages:
They share memory space:

 - Threads are light-weight, shared memory means can be created fairly quickly without much memory use. 
 - Easy and cheap to pass data around.

Disadvantages:
They share memory space:

 - Operations often take several steps and may be interrupted mid-stream
 - Thus, access to shared data is also non-deterministic

Creating threads is easy, but programming with threads is difficult.

Q: Why did the multithreaded chicken cross the road?
A: to To other side. get the

-- Jason Whittington



**Global Interpreter Lock**

(**GIL**)

The GIL locks the interpreter so that only a single thread can run at once,
assuring that one thread doesn't make a mess of the python objects that
another thread needs. The upshot:

Python threads do not work well for computationally intensive work.

Python threads work well if the threads are spending time waiting for something:

 - Database Access
 - Network Access
 - File I/O

More on the GIL:

https://emptysqua.re/blog/grok-the-gil-fast-thread-safe-python/

If you really want to understand the GIL -- and get blow away -- watch this one:

http://pyvideo.org/pycon-us-2010/pycon-2010--understanding-the-python-gil---82.html

Advantages / Disadvantages of Processes
---------------------------------------

Processes are heavier weight -- each process makes a copy of the entire interpreter (Mostly...) -- uses more resources.

You need to copy the data you need back and forth between processes.

Slower to start, slower to use, more memory.

 **no GIL**

Multiprocessing is suitable for computationally intensive work.

Works best for "large" problems with not much data:


The mechanics: how do you use threads and/or processes
======================================================

Python provides the `threading` and `multiprocessing` modules to facility concurrency.

They have similar APIs -- so you can use them in similar ways.

Key points:

There is no Python thread scheduler, it is up to the host OS

Do not use for CPU bound problems, will go slower than no threads, especially on multiple cores!!!

Works well for I/O bound problems, can use literally thousands of threads.

Limit CPU-bound processing to C extensions (that release the GIL)

Starting threads is relatively simple, but there are many potential issues.


We already talked about shared data, this can lead to a race condition.

 - may produce sligthly different results every run
 - may just flake out mysteriously every once in a while
 - Thus must synchronize threads!


Synchronization options:

 - Locks
 - Semaphore
 - BoundedSemaphore
 - Event
 - Condition
 - Queues


Mutex locks (threading.Lock)
----------------------------

 - probably most common
 - only one thread can modify shared data a any given time
 - thread determines when unlocked
 - must put lock/unlock around critical code in ALL threads
 - difficult to manage

Easiest with context manager:

.. code-block:: python

    x = 0
    x_lock = threading.Lock()

    # Example critical section
    with x_lock:
        # statements using x


Only one lock per thread! (or risk mysterious deadlocks)

Or use RLock for code-based locking (locking function/method execution rather than data access)


Semaphores (threading.Semaphore)
--------------------------------

 - Counter-based synchronization primitive
    - when acquire called, wait if count is zero, otherwise decrement 
    - when release called, increment count, signal any waiting threads
 - Can be called in any order by any thread
 - more tunable than locks
    - Can limit number of threads performing certain operations
    - Can signal between threads


Events (threading.Event)
------------------------

 - threads can wait for particular event
 - setting an event unblocks all waiting threads
Common use: barriers, notification


Condition (threading.Condition)
-------------------------------

 - combination of locking/signaling
 - lock protects code that establishes a "condition" (e.g., data available)
 - signal notifies threads that "condition" has changed
Common use: producer/consumer patterns


Queues (Queue)
--------------

 - easier to use than many of above
 - do not need locks
 - has signaling
Common use: producer/consumer patterns


.. code-block:: python


    from Queue import Queue
    data_q = Queue()

    Producer thread:
    for item in produce_items():
        data_q.put(items

    Consumer thread:
    while True:
        item = q.get()
        consume_item(item)


Scheduling (sched)
------------------

 - Schedules based on time, either absolute or delay
 - Low level, so has many of the traps of the threading synchromization primitives.


Multiprocessing
---------------

For this to work, want to send messages, as each process runs its own
independent Python interpreter.


Pipes and Pickle and Subprocess
-------------------------------

 - Very low level, for the brave of heart
 - Can send just about any Python object


Multiprocessing (multiprocessing)
---------------------------------

 - processes are completely isolated
 - no locking :)
 - instead messaging


Messaging
---------

Pipes (multiprocessing.Pipe):

 - Returns a pair of coneected objects
 - Largely mimics Unix pipes, but higher level
 - send picked objects or buffers


Queues (multiprocessing.Queue):

 - same interface as Queue
 - implemented on top of pipes
 - means you can pretty easily port threaded programs using queues to mutiprocessing
   - queue is only shared data


Other features of Multiprocessing

 - Pools
 - Shared objects and arrays
 - Synchronization primitives
 - Managed objects
 - Connections
