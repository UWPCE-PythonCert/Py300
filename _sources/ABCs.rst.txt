:orphan:

.. _abc:

##################################################
Abstract Base Classes and standard class protocols
##################################################

Other built in types (array, bytes, etc.,)

This topic under development!

Interfaces
==========

An "Interface" (for a class) is the set of attributes and methods available.

Python has traditionally used a very dynamic definition of interface:

"Duck typing"

If is quacks like a duck....

This is very flexible -- a class does not have to provide *everything*
that a given interface might require -- only the bit that is needed.

For instance  number of functions in the Python standard library act on
a "file-like object".

That means "an object that follows the file interface". However, it is
quite rare that any given function needs the entire interface -- maybe
it only needs to read something -- so only needs one method:

.. code-block:: python

    some_bytes = obj.read()

In this case, rather than checking if the object conforms to the file
interface, this is a great use case for EAFP:

"Easier to ask Forgiveness than Permission"

That is -- simply call ``.read()``, and catch the AttributError.

Or simply let it fail if there is no read() method.

Protocols
---------

"protocol" is essentially just another word for Interface. It tends to be
used when there is a bit more action -- such as the "Iterator Protocol".

The Iterator protocol specifies not just methods and attributes, but actions:

"A StopIteration Exception is raised when the iterator is exhausted"

But it's really just another word for the same thing. So in Python,
interfaces are talked about in (at least) for ways:

- Interface
- Protocol
- -like -- as in "file-like"
- generic name -- like "sequence"

Abstract Base Classes
---------------------

Sometimes it is nice to more formally define an interface.

Abstract Base Classes are a way to define a specific interface. In
particular, the the protocols of the standard Python object types.

They were added to Python to formalize the "Duck Typing" approach in
some contexts. See PEP 3119 for the details:

https://www.python.org/dev/peps/pep-3119/

In OO languages, an "abstract" class is a class that has an interface,
but no implementation. These are sometimes required by static OO languages
to provide a way to have more than one implementation of a given protocol.

In Python, they can be used as a way to know if a given object is what
you might be expecting -- is it a Sequence? a Mapping?

You can directly check if an object is a particular type:

.. code-block:: python

  In [117]: isinstance([1,2,3], list)
  Out[117]: True

  In [118]: isinstance([1,2,3], tuple)
  Out[118]: False

But that is not the "Python way"  -- we usually don't care if the passed
in object is a list, or a tuple, or any other sequence type. What we care
about is if is a Any Sequence (or maybe only any Iterable).

Enter ABCs:

.. code-block:: python

    from collections.abc import Sequence

    In [121]: isinstance([1,2,3,4], Sequence)
    Out[121]: True

    In [122]: isinstance((1,2,3,4), Sequence)
    Out[122]: True

But what if it needs to mutable?

.. code-block:: python

    In [123]: from collections.abc import MutableSequence

    In [124]: isinstance([1,2,3,4], MutableSequence)
    Out[124]: True

    In [125]: isinstance((1,2,3,4), MutableSequence)
    Out[125]: False

So Python

gotcha!
-------

One of the most common type errors seen in Python is the "sequence of
strings" vs "single string" confusion:

It is moderately common to write s function that acts on a bunch of
strings -- perhaps a bunch of filenames.

.. code-block:: python

    def do_something(filenames):
        """
        process a number of files.

        :param filenames: sequence of filenames to process
        """
        for name in filenames:
            print("processing:", name)
            with open(name) as the_file:
                process(the_file)

Pass it a list of strings, and all is good:

.. code-block:: ipython

    do_something(["name1", "name2", "third_name"])
    processing: name1
    processing: name2
    processing: third_name

But what if the user has only one file to process?

.. code-block:: ipython

    In [4]: do_something("a_single_name")
    processing: a
    processing: _
    processing: s
    processing: i
    processing: n
    processing: g
    processing: l
    processing: e
    processing: _
    processing: n
    processing: a
    processing: m
    processing: e

OOPS! -- this happens all too often.

Why?

Well, the function is expecting an iterable of strings that is can loop over.

But a string IS an iterable of strings! it iterates over the string,
yielding each letter. And a letter is simply a string that happens to
be of length-one.

So plain old duck-typing and EAFP doesn't work.

what about checking for a Sequence?

.. code-block:: python

    def do_something2(filenames):
        """
        process a number of files.

        :param filenames: sequence of filenames to process
        """
        if not isinstance(filenames, abc.Iterable):
            # put it in a list so the rest of the code is the same.
            filenames = [filenames]
        for name in filenames:
            print("processing:", name)

.. code-block::ipython

    In [6]: do_something2("name")
    processing: n
    processing: a
    processing: m
    processing: e

DARN! that didn't work -- of course, a string *is* Iterable.

So you need to do it the other way around: check for a string. But there
is not ABC for strings -- there is only one string object in Python, and
it's unlikely that a third party lib will write an alternate implementation.

So you check for string explicitly:

.. code-block:: python

    def do_something3(filenames):
        """
        process a number of files.

        :param filenames: sequence of filenames to process
        """
        if isinstance(filenames, str):
            # put it in a tuple so the rest of the code is the same.
            filenames = (filenames,)
        for name in filenames:
            print("processing:", name)

Ahh -- that works:

.. code-block:: ipython

    In [10]: do_something3("name")
    processing: name

    In [11]: do_something3(["name", "name2", "name3"])
    processing: name
    processing: name2
    processing: name3




Things you might do with ABCs
-----------------------------

(In order of likelihood)

* do an ``isinstance()`` check at the top of a function.

* create a class that conforms to one of the standard ABCs and register it.

* write an ABC that specifies a particular subset of an interface for your
  use-case

* write a full-fledged ABC for a whole new Interface.
  (very, very unlikely...)

Demo each of these...


Creating an object that matches an interface
---------------------------------------------

Let's say you write your own container that is a ``MutableSequence``.

How do you let others know that your object can be used anywhere a
``MutableSequence`` (or a ``Sequence``, or an ``Iterable``) can be used?

You can "register" your class with the ABC:

TODO!!!!


semi-ducktyping
---------------

If you need only a method or two from an object, then just use EAFP:
``file_like.read()`` for instance.

But what if you need a bunch of methods -- but not an explcite particular type?

This was brought up on SO:

http://stackoverflow.com/questions/3450857/python-determining-if-an-object-is-file-like

Alex Martelli's answer:

"""
... you need to determine which methods you need. To check for them, I
recommended defining your own FileLikeEnoughForMe abstract base class
with abstractmethod decorators, and checking the object with an isinstance
for that class.
"""

Here's an example:

How to write an ABC
-------------------

The abc module provides tools to help write an ABC.

Let's look at an example:

``Examples/abcs/file_like``

.. code-block:: python

    import abc

    # deriving from ABC makes it, well, an ABC :-)
    class FileLike(abc.ABC):

        @abc.abstractmethod
        def read(self):
            """read the contents of the file"""

        @abc.abstractmethod
        def write(self, text):
            """ write stuff to the file """

        @abc.abstractmethod
        def readlines(self):
            """read the lines of the file into a list"""

        @classmethod
        def __subclasshook__(cls, inst):
            if cls is FileLike:
                print(cls.__dict__.keys())
                if (any("read" in B.__dict__ for B in inst.__mro__) and
                    any("write" in B.__dict__ for B in inst.__mro__) and
                    any("readlines" in B.__dict__ for B in inst.__mro__)
                    ):
                    return True
            return NotImplemented

1) subclass from ABC to make it an ABC.

2) define the abstract methods you need -- the ``abc.abstractmethod`` decorator lets
   the ABC machinery know the method needs to be implimented by subclasses.

3) define __subclasshook__ -- this is the magic that lets isinstance() work
   for classes that you have not control over.

   It is called when isinstance() is called with this as the class. It then
   checks to see if all the methods expected are in the object passed in.

   There could certainly be more magic, but this is explicite, and you could
   add other logic if you really wanted to.

Using an ABC
------------

You use the ABC by passing it to isinstance:

.. code-block:: python

    def use_a_file(f):
        """
        Do some arbitrary thing with a file-like object

        :param f: an open file-like object
        """
        # check if we got the right thing
        if not isinstance(f, FileLike):
            raise TypeError("you must pass an open file-like object to use_a_file\n"
                            " A {} does not satisfy teh FileLike protocol".format(type(f))
                            )
        print("Hey -- I can use that! -- {}".format(type(f)))

This function will now work with any object that satisfies the ABC,
and raise a type error for any object that doesn't.

Examples:

.. code-block:: ipython

    In [23]: use_a_file("a string")
    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    <ipython-input-23-1da560af8e21> in <module>()
    ----> 1 use_a_file("a string")

    /Users/Chris/PythonStuff/UWPCE/Py300-Spring2017/Examples/abcs/file_like.py in use_a_file(f)
         60     if not isinstance(f, FileLike):
         61         raise TypeError("you must pass an open file-like object to use_a_file\n"
    ---> 62                         " A {} does not satisfy teh FileLike protocol".format(type(f))
         63                         )
         64     print("Hey -- I can use that! -- {}".format(type(f)))

    TypeError: you must pass an open file-like object to use_a_file
     A <class 'str'> does not satisfy teh FileLike protocol

Use it with a built-in actual file object:

.. code-block:: ipython

    In [24]: with open("junk", 'a') as a_file:
        ...:     use_a_file(a_file)
        ...:
    Hey -- I can use that! -- <class '_io.TextIOWrapper'>

Making your own implementation of FileLike:
-------------------------------------------

To make a File like object, you subclass from the ABC you defined.
And define the methods

.. code-block:: python

    class MyFileType(FileLike):

        def read(self):
            """
            read the contents of teh file and return it

            this dummy implimentation always returns the same thing.
            """
            return "The contents of the file\nNot much here"

now try to use it:

.. code-block:: ipython

    In [26]: my_f = MyFileType()
    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    <ipython-input-26-041b07f27f62> in <module>()
    ----> 1 my_f = MyFileType()

    TypeError: Can't instantiate abstract class MyFileType with abstract methods readlines, write

**OOPS** -- can't do that! That's what ``@abstractmethod`` does for you -- it requires that an implimentation be provided.

So let's do that:

.. code-block:: ipython

    class MyFileType(FileLike):

        def read(self):
            """
            read the contents of teh file and return it

            this dummy implimentation always returns the same thing.
            """
            return "The contents of the file\nNot much here"

        def write(self, content):
            """
            this just throws away the content...
            """
            pass

        def readlines(self):
            return ["The contents of the file\n","Not much here"]


and now it works:

.. code-block:: ipython

  In [28]: my_f = MyFileType()

and it can be used with our function:

.. code-block:: ipython

  In [29]: use_a_file(my_f)
  Hey -- I can use that! -- <class '__main__.MyFileType'>




A Digression
-------------

"private" attributes?

A private attribute is an attribute that is not part of the Interface
of the class.

While Python does not strictly have private attributes, It's a common
convention that a leading underscore means an attribute that should only
be accessed from within a class.

Often used for properties, for example:

.. code-block:: python

    class Circle():
        ...
        @property
        def diameter(self):
            return self._radius * 2

But there is a "stronger" way to "protect" an attribute -- double underscores:

.. code-block:: ipython

    In [129]: class Base():
         ...:     __private = "sneaky"
         ...:

    In [130]: Base.__dict__.keys()
    Out[130]: dict_keys(['_Base__private', '__module__', '__doc__', '__weakref__', '__dict__'])

note the "_Base" was added to the name.

But if you don't have double underscores:

.. code-block:: ipython

    In [131]: class Base():
         ...:     public = "wide open"
         ...:     __private = "sneaky"
         ...:

    In [132]: Base.__dict__.keys()
    Out[132]: dict_keys(['_Base__private', '__module__', '__doc__', 'public', '__weakref__', '__dict__'])

So what happens if you subclass? Does it get overridden?

.. code-block:: ipython

    In [134]: class Sub(Base):
         ...:     private = "oops! -- overridden?"
         ...:

    In [135]: Sub.__dict__.keys()
    Out[135]: dict_keys(['__module__', 'private', '__doc__'])

    In [136]: Sub.private
    Out[136]: 'oops! -- overridden?'

    In [137]: Sub._Base__private
    Out[137]: 'sneaky'

so using the double underscores assures that the attribute will not get
accidentally overridden in a subclass.

**Note:** if you now the name mangling, yu can still mess with it ...

**So should you do this?**

Usually not -- it turns out that in practice it's
rare for "private" attributes to get overidden accidentally. So this is
not a widely used practice.

Final Thoughts
--------------

* don't use ``isinstace`` and ABCs when EAFP will do -- simply make the call
  you need and catch the exception.

* Generally better to call ``isinstance`` on an ABC than a specific class

* Use the most general ABC you can -- i.e. "Iterable" rather than "Sequence"

* "Even with ABCs, excessive use of ``isinstance`` checks may be code smell"
  -- Luciana Ramalho (from "Fluent Python")

* ABCs mostly exist to support multiple implementations of the same interface:
  lists and tuples, multiple containers, etc.

* The only time you should write a custom ABC is part of a Framework that a
  lot of people are going to extend -- a very rare case!

Helpful write-ups:

https://dbader.org/blog/abstract-base-classes-in-python

http://stackoverflow.com/questions/3570796/why-use-abstract-base-classes-in-python


Other handy built-in sequences
==============================

Lists and tuples are very widely used in Python -- they give you a mutable
and an immutable sequence -- what else do you need?

There are some special case sequences:

array.array
-----------

The ``array`` module provides and array object -- a mutable sequence of
homogeneous simple numeric types.

``https://pymotw.com/3/array/``

The type must be declared when the array is created, and then it can only hold that type:

.. code-block:: ipython

    In [60]: import array

    In [61]: arr = array.array('i') # i is an integer type)

    In [62]: arr.extend((3,4,5))

    In [63]: arr
    Out[63]: array('i', [3, 4, 5])

    In [64]: arr.append(3.45)
    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    <ipython-input-64-b853b72c3c39> in <module>()
    ----> 1 arr.append(3.45)

    TypeError: integer argument expected, got float

**Why?**

``array`` supports a wide variety of types, stores the data far more
compactly, and inter operates better with raw binary data.

But ``numpy`` gives you all that, and a lot more -- so folks are more likely to
go to numpy if they really need these features.

Binary sequence types
---------------------

Another way to work with binary data is the ``bytes`` and ``bytearray`` objects.

``bytes``:
  an immutable sequence of integers in the range 0 <= x < 256.

``bytearray``:
  a mutable sequence of integers in the range 0 <= x < 256. It has most
  of the usual methods of mutable sequences, as well as most methods that
  the bytes type has

a ``byte`` is essentially the smallest unit of memory the computer can work with.
On virtually all modern hardware, a byte is 8 bits -- 2**8 == 256 -- so a single
byte is a value between 0 and 255.

You use bytes and bytearray objects to work with binary data -- usually you'll
know it if you need it.

But the most common use case is to deal with encoded text:

.. code-block:: ipython

    In [79]: text = "Not ASCII: \u0107 \u0398 \u03A3 \u03BB \uF4A9"

    In [80]: text
    Out[80]: 'Not ASCII: ć Θ Σ λ \uf4a9'

    In [81]: text = "Not ASCII: \u0107 \u0398 \u03A3 \u03BB"

    In [82]: text
    Out[82]: 'Not ASCII: ć Θ Σ λ'

    In [83]: b = text.encode('utf-8')

    In [84]: type(b)
    Out[84]: bytes

    In [85]: b
    Out[85]: b'Not ASCII: \xc4\x87 \xce\x98 \xce\xa3 \xce\xbb'

Note that the bytes in the ascii range display as text. This is an
artifact of the old days of C and Python2! where strings *were* byte arrays.

Python also has a literal for a bytes object -- that also uses text:

.. code-block:: ipython

    In [92]: b
    Out[92]: b'these are bytes'

But the individual elements are treats as integers:

.. code-block:: ipython

    In [93]: b[0]
    Out[93]: 116

    In [94]: list(b)
    Out[94]: [116, 104, 101, 115, 101, 32, 97, 114, 101, 32, 98, 121, 116, 101, 115]

Since bytes are often used for encoded text, they come with a ``decode`` method:

.. code-block:: ipython

    In [100]: b
    Out[100]: b'Not ASCII: \xc4\x87 \xce\x98 \xce\xa3 \xce\xbb'

    In [101]: b.decode('utf-8')
    Out[101]: 'Not ASCII: ć Θ Σ λ'

``memoryview``
--------------

A ``memoryview`` object is a wrapper around a bit of memory -- it allows you to
view an manipulate the data underlying some other object without copying it.

Mostly used for binary interchange between different extension data types:
like to pass data from a numpy array to an image, for instance:

.. code-block:: ipython

    In [108]: b = bytearray(b'abcdefg')

    In [109]: m = memoryview(b)

    In [110]: m
    Out[110]: <memory at 0x104759048>

    In [111]: len(m)
    Out[111]: 7

m and b now share the same memoroy block. So if I change m...

.. code-block:: ipython

    In [113]: m[2:4] = b'\x00\x00'

    In [114]: m
    Out[114]: <memory at 0x104759048>

    In [115]: b
    Out[115]: bytearray(b'ab\x00\x00efg')

b is changed as well.

``memoryview`` can represent different data types, and even
multi-dimensional arrays.

For more info:

https://docs.python.org/3/library/stdtypes.html#memoryview


