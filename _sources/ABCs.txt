:orphan:

.. _abc:

##################################################
Abstract Base Classes and standard class protocols
##################################################

Other built in types (array, bytes, etc.,)

This topic under development!

Abstract Base Classes
=====================

Abstract Base Classes are a way to define the protocol of the standard
Python object types.

They were added to Python to formalize the "Duck Typing" approach is
some contexts. See PEP 3119 for the details:

https://www.python.org/dev/peps/pep-3119/

In OO languages, and "abstract" class is a class that has an interface,
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
in object is a list, or a tuple, or any other sequence type. what we care
about is if is a Any Sequence.

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



A digression
------------

"private" atttributes?

It's a common convention that a leading underscore means an attribute
that should only be accessed from within a class. Often used for
properties, for example:

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

But if you don't have doouble underscores:

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

``memoryview``s can represent different data types, and even
multi-dimensional arrays.

For more info:

https://docs.python.org/3/library/stdtypes.html#memoryview


