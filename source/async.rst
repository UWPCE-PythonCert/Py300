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

Async and Concurrency are really two different things -- you can do either
one without the other -- but they are closely related.


https://vimeo.com/49718712

In "Concurrency is not parallelism" Rob Pike makes a key point:
Breaking down tasks into concurrent subtasks only allows parallelism,
it’s the scheduling of these subtasks that creates it.

Async is about the scheduling.


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

More in the GIL:

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

Fill in the mechanics here.....
 - starting threads
 - keeing things in sync
 - queues
 - locks
 - etc.

Asynchronous Programming
========================

What is it?

Approaches:

- Event Loops
- Callbacks
- Coroutines

Why Async?
----------

This is a pretty good overview of why you might want to use async:

https://hackernoon.com/asyncio-for-the-working-python-developer-5c468e6e2e8e#.dlhcuy23h

In: "A Web Crawler With asyncio Coroutines", Guido himself writes:

  Many networked programs spend their time not computing, but holding open many connections that are slow, or have infrequent events. These programs present a very different challenge: to wait for a huge number of network events efficiently. A contemporary approach to this problem is asynchronous I/O, or "async".

http://www.aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html

So my take:

Async is the good approach to support many connections that are spending a lot of time waiting, and doing short tasks when they do do something.

**NOTE:** the backbone of the web is HTTP -- which is a "stateless" protocol. That is, each request is independent (state is "faked" with sessions via cookies). So "classic" web apps are NOT keeping many connections alive, there may be many clients at once, but each request is still independent. And often there is substantial work do be done with each one. A multi-threaded or multi-processes web server works fine for this.

Single Page Apps and WebSockets
-------------------------------

**"Single Page Apps"**

  A single-page application (SPA) is a web application ... providing a user experience similar to that of a desktop application. ... *Interaction with the single page application often involves dynamic communication with the web server behind the scenes.*

  https://en.wikipedia.org/wiki/Single-page_application

Communication with the web service can be regular old http (AJAX), or in modern implementations:

**WebSocket**:

  WebSocket is a computer communications protocol, providing full-duplex communication channels over a single TCP connection.

  https://en.wikipedia.org/wiki/WebSocket

WebSocket gives the advantage of "pushing" -- the server can push information to the client, rather than the client having to poll the server to see if anything needs to be updated.

Either HTTP or WebSocket can generate many small requests to the server, which async is good for, but WebSocket pretty much requires an async server if you want it to scale well, as each active client is keeping a connection open.

Also: often a web service is depending on other web services to do it's task. Kind of nice if your web server can do other things while waiting on a third-party service.


Blocking
--------
A "Blocking" call means a function call that does not return until it is complete. That is, an ordinary old function call:

.. code-block:: python

  call_a_func()

The program will stop there and wait until the function returns before moving on. Nothing else can happen. Usually this is fine, the program may not be able to do anything else until it gets the result of that function.

But what if:

- That function will take a while?
- And it's mostly just waiting for the network or database, or....

Maybe your application needs to be responsive to user input, or do other
work while that function is working. how do you deal with that?

Event Loops
-----------

Asynchronous programming is not new -- it is the key component of traditional desktop Graphical User Interface Programs. The GUI version is often referred to as "event-driven" development:

You write "event handlers" that respond to particular events in the GUI: moving the mouse, clicking on a button, etc.

The trick is that you don't know in what order anything might happen -- there are Multiple GUI objects on the screen at a given time, and users could click on any of them in any order.

This is all handles by and "event loop", essentially code like this:

.. code-block:: python

  while True:
     evt = event_queue.pop()
     if evt:
         evt.call_handler()

That's it -- it is an infinite loop that continually looks to see if there are any events to handle, and if there are, it calls the event handler for that event. Meanwhile, the system is putting events on the event queue as they occur: someone moving the mouse, typing in control, etc.

It's important is that event handlers run quickly -- if they take a long time to run, then the GUI is "locked up", or not responsive to user input.

If the program does need to do some work that takes time, it needs to do that work in another thread or processes, and then put an event on the event queue when it is done.

For some examples of this, see:

https://www.blog.pythonlibrary.org/2013/06/27/wxpython-how-to-communicate-with-your-gui-via-sockets/

Callbacks
---------

Callbacks are a way to tell a non-blocking function what to do when they are done. This is a common way for systems to handle non-blocking operations. For instance, in Javascript http requests are non-blocking. The request function call will return right away.

.. code-block:: javascript

  request('http://www.google.com',
          function(error, response, body){
              console.log(body);
          });

What this means is make a request to Google, and when the request is complete, call the function with three parameters: ``error``, ``response``, and ``body``. This function is defined inline, and simply passes the body to the console log. But it could do anything.

That function is put on the event queue when the request is done, and will be called when the other events on the queue are processed.

Contrast with with the "normal" python request:

.. code-block:: python

  import requests
  r = requests.get('http://www.google.com')
  print(r.text)

The difference here is that the program will wait for ``requests.get()`` call to return, and that won't happen until the request is complete. If you are making a lot of requests and they take a while, that is a lot of time sitting around waiting when your computer isn't doing anything.

Async programming usually (always?) involves an event loop to schedule operations.

But callbacks are only one way to communicate with the event loop.

Coroutines
----------

  Coroutines are computer program components that generalize subroutines for non-preemptive multitasking, by allowing multiple entry points for suspending and resuming execution at certain locations. Coroutines are well-suited for implementing more familiar program components such as cooperative tasks, exceptions, event loops, iterators, infinite lists and pipes.

https://en.wikipedia.org/wiki/Coroutine

  Coroutines are functions that can hold state, and varies between invocations; there can be multiple instances of a given coroutine at once.

This may sound a bit familiar from generators -- a generator function can hold state when it yields, and there can be multiple instances of the same generator function at once.

In fact, you can use generators and yield to make coroutines, and that was done in Python before version 3.5 added new features to directly support coroutines.

**Warning:** This is really hard stuff to wrap your head around!

.. image:: images/coroutines_plot.png

(from: http://www.dabeaz.com/coroutines/Coroutines.pdf)

``async`` / ``await``
---------------------

In Python 3.5, the ``async`` and ``await`` keywords were added to make coroutines "native" and more clear.

You define a coroutine with the ``async`` keyword:

.. code-block:: python

   async def ping_server(ip):
        pass

When you call ``ping_server``, it doesn't run the code. what it does is return a coroutine, all set up and ready to go.

.. code-block:: ipython

    In [12]: cr = ping_server(5)

    In [13]: cr
    Out[13]: <coroutine object ping_server at 0x104d75620>

So How do you actually *run* the code in a coroutine?

``await a_coroutine``

It's kind of like yield (from generators), but instead it returns the next value from the coroutine, and pauses execution so other things can run.

``await`` suspends the execution (letting other code run) until the object called returns.

Or you can put it on the event loop with loop.ensure_future()

When you call await on an object, it needs to be an "awaitable" object: an object that defines an ``__await__()`` method which returns an iterator which is not a coroutine itself. Coroutines themselves are also considered awaitable objects.

Think of async/await as an API for asynchronous programming
-----------------------------------------------------------

async/await is really an API for asynchronous programming: People shouldn't think that async/await as synonymous with asyncio, but instead think that asyncio is a framework that can utilize the async/await API for asynchronous programming.

Future object
--------------

A Future object encapsulates the asynchronous execution of a callable -- it "holds" the code to be run later.

It also contains methods like:

* cancel()

  Cancel the future and schedule callbacks.

* done()

  Return True if the future is done.

* result()

  Return the result this future represents.


* add_done_callback(fn)

  Add a callback to be run when the future becomes done.

 * set_result(result)

   Mark the future done and set its result.

A coroutine isn't a future, but they can be wrapped in one by the event loop.

The Event Loop
--------------

The whole point of this to to pass events along to an event loop. So you can't really do anything without one.

The ``asyncio`` package provides an event loop:

The ``asyncio`` event loop can do a lot:

 * Register, execute, and cancel delayed calls (asynchronous functions)
 * Create client and server transports for communication
 * Create subprocesses and transports for communication with another program
 * Delegate function calls to a pool of threads

But the simple option is to use it to run coroutines:

.. code-block:: python

    import asyncio

    async def say_something():
        print('This was run by the loop')

    # getting an event loop
    loop = asyncio.get_event_loop()
    # run it:
    loop.run_until_complete(say_something())
    loop.close()

This is not a very interesting example -- after all, the coroutine only does one thing and exits out, so the loop simply runs one event and is done.

So let's see a slightly more interesting example:

.. code-block:: python

    import asyncio
    import datetime
    import random

    # using "async" makes this a coroutine:
    async def display_date(num, loop):
        # the event loop has a time() built in.
        end_time = loop.time() + 50.0 # we want it to run for 50 seconds.
        while True: # keep doing this until break
            print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
            if (loop.time() + 1.0) >= end_time:
                break
            await asyncio.sleep(random.randint(0, 5))


    loop = asyncio.get_event_loop()

    asyncio.ensure_future(display_date(1, loop))
    asyncio.ensure_future(display_date(2, loop))

    loop.run_forever()


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


References:

David Beazley: Concurrency from the ground Up.

He writes a full async client server from scratch before your eyes --
this guy can write code faster than most of us can read it...

https://youtu.be/MCs5OvhV9S4

David Beazley: asyncio:

https://youtu.be/ZzfHjytDceU

https://www.youtube.com/watch?v=lYe8W04ERnY













