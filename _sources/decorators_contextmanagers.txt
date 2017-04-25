:orphan:

.. _decorators:

###############################
Decorators and Context Managers
###############################


We touched decorators and context managers in the first quarter. I recommend you review that lecture.

http://uwpce-pythoncert.github.io/IntroToPython/session10.html

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



Scope
-----

Why do decorators have a function inside another function?

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

In addition to decorators, closures are also useful for callbacks.

.. code-block:: python


    In [14]: def my_callback(val):
        ...:     print("function my_callback was called with {0}".format(val))

    In [15]: def make_call(val, func):
        ...:     func(val)

    In [16]: for i in range(3):
        ...:     make_call(i, my_callback)

    function my_callback was called with 0
    function my_callback was called with 1
    function my_callback was called with 2
    

Definition of closures from Wikipedia:

Operationally, a closure is a record storing a function together with an environment: a mapping associating each free variable of the function (variables that are used locally, but defined in an enclosing scope) with the value or reference to which the name was bound when the closure was created. A closure—unlike a plain function—allows the function to access those captured variables through the closure's copies of their values or references, even when the function is invoked outside their scope.


Functools Library
-----------------

Memoize decorator we created in the first quarter is in Functools