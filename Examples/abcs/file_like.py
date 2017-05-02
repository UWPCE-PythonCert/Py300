"""
Example of a ABC for a file-like object.

This example inpired by:

http://stackoverflow.com/questions/3450857/python-determining-if-an-object-is-file-like

The "trick" is that you may need only part of what makes a file file-like
 -- i.e. not **all ** it's methods.

If you need a complete implimentation, you can use one of the ABCS in the io module:

https://docs.python.org/3/library/io.html#class-hierarchy

If you only need one or two -- jsut call it and catch the AttributeError.

But if you need a handful, then this can be a useful way to get it.

https://docs.python.org/3/library/abc.html
"""

import abc
import io


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
            if (any("read" in B.__dict__ for B in inst.__mro__) and
                any("write" in B.__dict__ for B in inst.__mro__) and
                any("readlines" in B.__dict__ for B in inst.__mro__)
                ):
                return True
        return NotImplemented


# Using it
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

# Examples:

# pass it a string -- should raise an error:
# use_a_file("fred")

# pass it an open file -- it should be happy
with open("junk", 'a') as a_file:
    use_a_file(a_file)

# pass it a cStringIO object:
output = io.StringIO()
use_a_file(output)


# Making a new FileLike object:

class MyFileType(FileLike):

    def read(self):
        """
        read the contents of teh file and return it

        this dummy implimentation always returns the same thing.
        """
        return "The contents of the file\nNot much here"

# now try to use it

# it will raise an exception
# my_f = MyFileType()

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

# now try to use it

my_f = MyFileType()