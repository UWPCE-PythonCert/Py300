:orphan:

.. _decorators:

###############################
Decorators and Context Managers
###############################


We touched decorators and context managers in the first quarter. I recommend you review that lecture.

http://uwpce-pythoncert.github.io/IntroToPython/session10.html


Decorators
**********

Because functions are first-class objects in Python, you can write functions 
that take functions as arguments and/or return functions as values and you 
can declare a function inside another function:

.. code-block:: python


    In [1]: def my_decorator(func):
       ...:      def inner():
       ...:   	     print('running inner')
       ...:      return inner
       ...:


    In [2]: def other_func():
       ...:     print('running other_func')

    In [3]: other_func()
    running other_func

    In [4]: other_func = my_decorator(other_func)

    In [5]: other_func()
    In [5]: running inner

    In [6]: other_func
    Out[6]: <function __main__.my_decorator.<locals>.inner>


Which is the same as:

.. code-block:: python
   

    In [7]: @my_decorator
       ...: def other_func():
       ...:      print('running other_func')
       ...:

    In [8]: other_func()
    running inner

    In [9]: other_func
    Out[9]: <function __main__.my_decorator.<locals>.inner>


Decorators have the power to replace the decorated function with a different one!


Import Time Vs. Run Time
------------------------

Decorators are run at import time:

Examples/decorators/play_with_imports.py


Let's make a decorator that finds the best price for a shirt.

Examples/decorators/shirt_price.py


Scope
-----

Why do decorators usually have a function inside another function?

Decorators are implemented using closures. Definition of closures from Wikipedia:

Operationally, a closure is a record storing a function together with an environment: a mapping associating each free variable of the function (variables that are used locally, but defined in an enclosing scope) with the value or reference to which the name was bound when the closure was created. A closure—unlike a plain function—allows the function to access those captured variables through the closure's copies of their values or references, even when the function is invoked outside their scope.


.. code-block:: python


    In [3]: def start_at(x):
       ...:     def increment_by(y):
       ...:	    return x + y
       ...:     return increment_by

    In [4]: closure_1 = start_at(3)

    In [5]: closure_2 = start_at(5)

    In [6]: closure_1(2)
    Out[6]: 5

    In [7]: start_at(2)(4)
    Out[7]: 6


Let's make this more explicit:

Example/decorators/play_with_scope.py

nonlocal declaration: allows you to flag a variable as a free variable even if it's immutable.


Callbacks
---------
In addition to decorators, closures are also useful for callbacks.

Callbacks are functions handed off to another function, so that they can call the handed off function once they are done running their own code. 

.. code-block:: python


    In [14]: def my_callback(val):
        ...:     print("function my_callback was called with {0}".format(val))

    In [15]: def make_call(val, func):
                 # do some cool stuff here, and then call the callback
        ...:     func(val)

    In [16]: for i in range(3):
        ...:     make_call(i, my_callback)

    function my_callback was called with 0
    function my_callback was called with 1
    function my_callback was called with 2
    

What if my decorated function uses unknown inputs?
--------------------------------------------------


.. code-block:: python


   def p_decorate(func):
       def func_wrapper(*args, **kwargs):
       	   return "<p>{0}</p>".format(func(*args, **kwargs))
       return func_wrapper


   @p_decorate
   def get_fullname(first_name, last_name):
       return first_name + last_name


Functools Library
-----------------

Single dispatch: 
 - create many functions that do the same sort of thing, but based on type
 - decorator determines type, and decides which function is run

https://docs.python.org/3/library/functools.html#functools.singledispatch

Memoize decorator we created in the first quarter is in Functools:

https://docs.python.org/3/library/functools.html#functools.lru_cache


Stacked Decorators
------------------


.. code-block:: python

    @dec1
    @dec2
    def my_fun():
        print('my_fun')

    translates to:
    def my_fun():
        print('my_fun')

    f = dec1(dec2(my_fun))


Parameterized Decorators
------------------------

The purpose of the outer function in the decorator is to receive the function to be decorated, adding
anything to scope that should be there before the decorated function is called.

The inner function runs the function being decorated, so its inputs are the same as the function being
decorated.

How do we add more input parameters to our decorator? Like this example from Django:


.. code-block:: python

   @register.filter(name='cut')
   def cut(value, arg):
       return value.replace(arg, '')


Add yet another function in scope:

.. code-block:: python

    def decorator(arg1, arg2):
        def real_decorator(function):
            def wrapper(*args, **kwargs):
                print("Congratulations.  You decorated a function that does something with %s and %s" % (arg1, arg2))
                function(*args, **kwargs)
            return wrapper
        return real_decorator


    @decorator("arg1", "arg2")
    def print_args(*args):
        for arg in args:
            print(arg)


Last example from: http://scottlobdell.me/2015/04/decorators-arguments-python/

Ideas for what to cover from "Fluent Python" by Luciano Ramalho, which I highly recommend.

Another great overview: https://dbader.org/blog/python-decorators

Context Managers
****************

Are kind of similar to decorators in function: they wrap a section of code so that some other code is run before and/or afterwards, and they can effect the code that is wrapped.

Decorators wrap functions.

Context managers wrap small sections of code.

Decorators are used for things like logging, enforcing access control and authentication, instrumentation and timing functions, rate-limiting, caching, etc. 

Context managers are used to make sure a resource is released or a previous state is restored after a code block

But, this is all fluid, and there are tools that are designed to be used as either a context manager or a decorator.

https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch


What makes a context manager:

- The with statement, designed to simplify the try/finally pattern. 
- Uses __enter__ and __exit__ for creating context manager

Therefore, just like for a try/finally block, keep the code in the context manager to the minimum that needs to be there.

Examples/decorators/context_manager.py


Contextlib Utilities
--------------------

https://docs.python.org/3/library/contextlib.html

especially check out:
https://docs.python.org/3/library/contextlib.html#examples-and-recipes


Remember Yield can be thought of as 'pause'

Having a try/finally (or a with block) around the yield is an unavoidable price of using @contextmanager, because you never know what the users of your context manager are going to do inside their with block.  - Leonardo Rochael
