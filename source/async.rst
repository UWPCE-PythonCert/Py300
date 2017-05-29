:orphan:

.. _async:

######################
Asychronous Programing
######################

Async: Not knowing what is happening when...

Whirlwind Tour of Concurrency
==============================

Before we get into async, it helps to know a a bit about Concurrency:

Having different code running at the same time.

Async and Concurency are really two different things -- you can do either one without the other -- but they are closely related.

Types of Concurrency
--------------------

(definitions here)

Multithreading:

what is a thread?

Multiprocessing:

what is a process

Advantages / Disadvantages of Threads
--------------------------------------

Threads are light-weight -- they share memory space, and thus can be created
fairly quickly without much memory use. Multiple threads share the same memory,
so easy and cheap to pass data around.

But -- since threads share the same memory, things can get out of whack -- thus the dreaded:

**Global Interpreter Lock**

(**GIL**)

The GIL locks the interpreter so that only a single thread can run at once,
assuring that one thread doesn't make a mess of the python objects that
another thread needs. The upshot:

Python threads do not work well for computationally intensive work.

Python threads work will if the threads are spending time waiting for something:

 - Database Access
 - Network Access
 - File I/O

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

Fill in the mechanics here.....
 - starting threads
 - keeing things in sync
 - queues
 - locks
 - etc.

Asynchronous Programming
========================

What is it?

approaches:

- callbacks
- event loops

Coroutines
----------

async features of Python:
-------------------------

Web servers and clients
-----------------------

There have been a few async frameworks around for Python for a while:

The granddaddy of them all:

Twisted https://twistedmatrix.com/trac/

Relative Newcomer:

Tornado:
http://www.tornadoweb.org/en/stable/

Using the latest and greatest: In Python 3.4, the asyncio package was added
to the standard lib:

https://www.python.org/dev/peps/pep-3156/

https://docs.python.org/3/library/asyncio.html

It provides the core pieces needed for asynchronous development.

``aiohttp`` is an http server (and client) built on top of ``asyncio``:

http://aiohttp.readthedocs.io/

(Twisted, Tornado, and the others have their own implementation of much
of what is in asycio)

As it's the most "modern" implementation -- we will use it for examples in this class:

.. code-block:: bash

    pip install aiohttp














