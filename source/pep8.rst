.. _pep8:

########################
Coding Style and Linting
########################

System Development with Python

- Maria McKinley

``mariak@mariakathryn.net``

pep-8
-----

Style Guide for Python

Defines a good baseline for your own local style guide

The 'rules' are just suggestions. From the document:

    most importantly: know when to be inconsistent -- sometimes the
    style guide just doesn't apply

important-pep-8-recommendations
-------------------------------

-  http://legacy.python.org/dev/peps/pep-0008/#tabs-or-spaces
-  Use 4 space indents. The tabs vs. spaces wars will likely never
   completely come to peaceful conclusion. But the Python community has
   standardized on 4 space indents. Unless you have compelling reasons
   not to, you should too.
-  Python 3 disallows mixing of tabs and spaces. With Python 2, you can
   run with the -tt flag which will force errors on mixed use of tabs
   and spaces.
-  Let your editor help you by having it insert 4 spaces for the tab
   key, turning on visible whitespace markers, and/or integrating a
   PEP-8 plugin

-  http://legacy.python.org/dev/peps/pep-0008/#maximum-line-length
-  Maximum line length of 79 characters
-  This is an easy one to let run away early. If 79 characters is too
   short, find a line length your team can agree on and stick to it as
   specified in PEP-8

pep-8-recommendations-continued
-------------------------------

-  http://legacy.python.org/dev/peps/pep-0008/#source-file-encoding
-  The default encoding in Python 2 is ASCII, in Python 3 it is UTF-8.
-  If you insert a non encodable character in a string literal, the
   interpreter will throw a SyntaxError when it reaches it.
-  To change the file encoding to UTF-8 for example, insert

   ::

       # coding: utf-8

   near the top of the file (see examples/encoding.py)



naming-conventions
------------------

-  variables, attributes, and modules names should be lowercase, with
   words separated by underscores
-  class names should be CamelCase, aka StudlyCaps
-  constants should be ALL CAPS

argument-conventions
--------------------

-  instance methods should have a first argument called self
-  class methods should have a first argument called cls
-  There's nothing magic about these names. You don't have to use this
   convention, but not adopting it will likely confuse future readers

imports
-------

-  `imports <http://legacy.python.org/dev/peps/pep-0008/#imports>`__
   should be near the top of the file
-  imports should be grouped in the following order, separated by a
   blank line:

   #. standard library imports
   #. related third party imports
   #. local application/library specific imports

-  avoid wildcard imports to keep the namespace clean for both humans
   and automated tools


public and non-public class members
-----------------------------------

When in doubt make an attribute non-public
A non-public attribute has two leading underscores and no trailing
underscores, which triggers Python's name mangling
property access should be cheap
add public names in a module to \_\_all\_\_
When comparing with singletons such as None, use "x is None", not "x ==
None".
`why? <http://jaredgrubb.blogspot.com/2009/04/python-is-none-vs-none.html>`__

tools-to-help
-------------

-  `PyChecker <http://pychecker.sourceforge.net/>`__ - searches for bugs
   and style issues. Not currently in PyPI, install from sourceforge
-  `pyflakes <https://pypi.python.org/pypi/pyflakes>`__ - searches for
   bugs, but without importing modules
-  `Pylint <http://www.pylint.org/>`__ - style guide, searches for bugs
-  `pep8 <https://pypi.python.org/pypi/pep8>`__ - tests conformance to
   PEP-8
-  `flake8 <https://pypi.python.org/pypi/flake8>`__ combines pyflakes,
   pep8, and mccabe, a code complexity analyzer

PyChecker
---------

Poor code example examples/Listing1.py was adapted from `Doug
Hellman <http://doughellmann.com/2008/03/01/static-code-analizers-for-python.html>`__

What can you spot as an error, bad practice, or poor style?

Now let's see what pychecker Listing1.py has to say about it

pylint
------

Interesting options:

::

    -d (msg ids), --disable=(msg ids)      Disable the messages identified in the messages table
    --generate-rcfile/--rcfile             Saves/restores a configuration

Now let's see what pylint Listing1.py has to say

Note the more verbose output, but did pychecker have any information not
contained in pylint?

pychecker identifies the incorrect use of self in a function

pyflakes
--------

Doesn't check style, just checks for functional errors

Similar to pychecker, but does not execute code

Now let's see what pyflakes Listing1.py has to say

What's the overlap in pyflakes' output versus the other two tools?

pycodestyle
-----------

used to be called "pep8"

Only checks style

Interesting options:

::

    --statistics         count errors and warnings
    --count              print total number of errors and warnings to standard error and set exit code to 1 if total is not null

Now let's see what pycodestyle Listing1.py has to say

What's the overlap in pep8's output versus the other two tools?

flake8
------

A tool which wraps pep8, pyflakes, and mccabe

`mccabe <http://nedbatchelder.com/blog/200803/python_code_complexity_microtool.html>`__
is a "microtool" written by Ned Batchelder (author of coverage) for
assessing `Cyclomatic
Complexity <http://en.wikipedia.org/wiki/Cyclomatic_complexity>`__

Interesting options:

::

    --max-complexity=N    McCabe complexity threshold

Now let's see what flake8 Listing1.py has to say

What's the overlap in flake8 output versus the other two tools?

analyzing-a-larger-codebase-in-the-wild
---------------------------------------

::

    pushd $HOME/virtualenvs/uwpce/lib/python2.7/site-packages

    flake8 django

    pylint django

code-analysis-tool-battle-royale
--------------------------------

::

    pychecker pylint
    pychecker flake8

    pylint pychecker
    pylint flake8

    flake8 $HOME/virtualenvs/uwpce/lib/python2.7/site-packages/pychecker/checker.py
    flake8 pylint

analysis-tool-summary
---------------------

-  There is no magic bullet that guarantees functional, beautiful code
-  Some classes of programming errors can be found before runtime
-  With the PEP-8 tools, it is easy to let rules such as line length
   slip by
-  It's up to you to determine your thresholds

