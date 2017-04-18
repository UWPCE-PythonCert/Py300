.. _packaging:

-------------------------
Building Your Own Package
-------------------------

The very basics of what you need to know to make your own package.

.. toctree::
   :maxdepth: 2

Why Build a Package?
====================

.. rst-class:: left

  There are a bunch of nifty tools that help you build, install and
  distribute packages.

  Using a well structured, standard layout for your package makes it
  easy to use those tools.

  Even if you never want to give anyone else your code, a well
  structured package eases development.

What is a Package?
--------------------

**A collection of modules**

* ... and the documentation

* ... and the tests

* ... and any top-level scripts

* ... and any data files required

* ... and a way to build and install it...

Python packaging tools:
------------------------

The ``distutils``::

    from distutils.core import setup

Getting klunky, hard to extend, maybe destined for deprication...

But it gets the job done -- and it does it well for the simple cases.

``setuptools``: for extra features

``pip``: for installing packages

``wheel``: for binary distributions

Where do I go to figure this out?
-----------------------------------

This is a really good guide:

Python Packaging User Guide:

https://packaging.python.org/en/latest/

**Follow it!**

And a sample project here:

https://github.com/pypa/sampleproject

(this has all the complexity you might need...)

And a couple good references:

https://blog.ionelmc.ro/2014/05/25/python-packaging/


This is a python package that helps you build a python package:

https://github.com/ionelmc/cookiecutter-pylibrary
https://blog.ionelmc.ro/2014/05/25/python-packaging/

https://cookiecutter.readthedocs.io/en/latest/
https://github.com/audreyr/cookiecutter


Packages, modules, imports, oh my!
----------------------------------

Before we get started on making your own package -- let's remind
ourselves about packages and modules, and importing....

**Modules**

A python "module" is a siingle namespace, with a collection of values:

  * functions
  * constants
  * class definitions
  * really any old value.

A module usually coresponds to a single file: ``something.py``


**Packages**

**Importing**

You usually import a module like this:

.. code-block:: python

  import something



**``import *``**

``_all__``

import as

relative imports
----------------

Relative imports were added with PEP 328:

https://www.python.org/dev/peps/pep-0328/

The final version is described here:

https://www.python.org/dev/peps/pep-0328/#guido-s-decision

This gets confusing! There is a good discussion on Stack Overflow here:

http://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time

Relative imports allow you to refer to other modules relative to where the existing module is in the package hierachy, rather than in the while thing. For instance, with the following pacakge structure::

  package/
      __init__.py
      subpackage1/
          __init__.py
          moduleX.py
          moduleY.py
      subpackage2/
          __init__.py
          moduleZ.py
      moduleA.py

You can do (in ``moduleX.py``):

.. code-block:: python

  from .moduleY import spam
  from . import moduleY
  from ..subpackage1 import moduleY
  from ..subpackage2.moduleZ import eggs
  from ..moduleA import foo
  from ...package import bar
  from ...sys import path

Similarly to *nix shells:

"." means "the current package"

".." means "the package above this one"

Note that you have to use the "from" form when using relative imports.

**Caveats:**

* you can only use relative imports from within a package

* you can not use relative imports from the interpreter

* you can not use reltaive imports from a top-level script


The alternative is to always use absolute imports:

.. code-block:: python

  from package.subpackage import moduleX
  from package.moduleA import foo

Advantages of relative imports:

* Package does not have to be installed

* You can move things around, and not much has to change

Advantages of absolute imports:

* explicit is better than implicit
* imports are the same regardless of where you put the package
* imports are the same in package code, command line, tests, scripts, etc.

There is debate about which is the "one way to do it" -- a bit unpythonic, but you'll need to make your own decision.


sys.modules
-----------

.. code-block:: ipython

  In [4]: type(sys.modules)
  Out[4]: dict

  In [6]: sys.modules['textwrap']
  Out[6]: <module 'textwrap' from '/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/textwrap.py'>

  In [10]: [var for var in vars(sys.modules['textwrap']) if var.startswith("__")]
  Out[10]:
  ['__spec__',
   '__package__',
   '__loader__',
   '__doc__',
   '__cached__',
   '__name__',
   '__all__',
   '__file__',
   '__builtins__']

you can access the module through the modules dict:

In [12]: sys.modules['textwrap'].__file__
Out[12]: '/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/textwrap.py'

Which is the same as:

.. code-block:: ipython

  In [13]: import textwrap

  In [14]: textwrap.__file__
  Out[14]: '/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/textwrap.py'

  In [15]: type(textwrap)
  Out[15]: module

  In [16]: textwrap is sys.modules['textwrap']
  Out[16]: True

So, more or less, when you import a module, the interpreter:

* Looks to see if the module is already in ``sys.modules``.

* If it is, it binds a name to the existing module in the current
  module's namespace.

* If it isn't:
 - A module object is created
 - The code in the file is run
 - The module is added to sys.modules
 - The module is added to the current namespace.

Implications of module import process:
--------------------------------------

* The code in a module only runs once per program run.
* Importing a module again is cheap and fast.
* Every place your code imports a module it gets the *same* object
  - You can use this to share "global" state where you want to.

* If you change the code in a module while the program is running -- the
  change will **not** show up, even if re-imported.
   - That's what ``reload()`` is for.






Basic Package Structure:
------------------------

::

    package_name/
        bin/
        CHANGES.txt
        docs/
        LICENSE.txt
        MANIFEST.in
        README.txt
        setup.py
        package_name/
              __init__.py
              module1.py
              module2.py
              test/
                  __init__.py
                  test_module1.py
                  test_module2.py


.. nextslide::

``CHANGES.txt``: log of changes with each release

``LICENSE.txt``: text of the license you choose (do choose one!)

``MANIFEST.in``: description of what non-code files to include

``README.txt``: description of the package -- should be written in reST (for PyPi):

(http://docutils.sourceforge.net/rst.html)

``setup.py``: distutils script for building/installing package.


.. nextslide::

``bin/``: This is where you put top-level scripts

  ( some folks use ``scripts`` )

``docs/``: the documentation

``package_name/``: The main pacakge -- this is where the code goes.

``test/``: your unit tests. Options here:

Put it inside the package -- supports ::

     $ pip install package_name
     >> import package_name.test
     >> package_name.test.runall()

Or keep it at the top level.

The ``setup.py`` File
----------------------

Your ``setup.py`` file is what describes your package, and tells the distutils how to pacakge, build and install it

It is python code, so you can add anything custom you need to it

But in the simple case, it is essentially declarative.


``http://docs.python.org/3/distutils/``


.. nextslide::

::

  from setuptools import setup

  setup(
    name='PackageName',
    version='0.1.0',
    author='An Awesome Coder',
    author_email='aac@example.com',
    packages=['package_name', 'package_name.test'],
    scripts=['bin/script1','bin/script2'],
    url='http://pypi.python.org/pypi/PackageName/',
    license='LICENSE.txt',
    description='An awesome package that does something',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.1.1",
        "pytest",
    ],
 )

``setup.cfg``
--------------

``setup.cfg`` provides a way to give the end user some ability to customise the install

It's an ``ini`` style file::

  [command]
  option=value
  ...

simple to read and write.

``command`` is one of the Distutils commands (e.g. build_py, install)

``option`` is one of the options that command supports.

Note that an option spelled ``--foo-bar`` on the command-line is spelled f``foo_bar`` in configuration files.


Running ``setup.py``
---------------------

With a ``setup.py`` script defined, the distutils can do a lot:

* builds a source distribution (defaults to tar file)::

    python setup.py sdist
    python setup.py sdist --format=zip

* builds binary distributions::

    python setup.py bdist_rpm
    python setup.py bdist_wininst

(other, more obscure ones, too....)

But you probably want to use wheel for binary disributions now.

.. nextslide::

* build from source::

    python setup.py build

* and install::

    python setup.py install

setuptools
-----------

``setuptools`` is an extension to ``distutils`` that provides a number of extensions::

    from setuptools import setup

superset of the ``distutils setup``

This buys you a bunch of additional functionality:

  * auto-finding packages
  * better script installation
  * resource (non-code files) management
  * **develop mode**
  * a LOT more

http://pythonhosted.org//setuptools/

wheels
-------

Wheels are a new binary format for packages.

http://wheel.readthedocs.org/en/latest/

Pretty simple, essentially an zip archive of all the stuff that gets put
in

``site-packages``

Can be just pure python or binary with compiled extensions

Compatible with virtualenv.

.. nextslide::

Building a wheel::

  python setup.py bdist_wheel

Create a set of wheels (a wheelhouse)::

	# Build a directory of wheels for pyramid and all its dependencies
	pip wheel --wheel-dir=/tmp/wheelhouse pyramid

	# Install from cached wheels
	pip install --use-wheel --no-index --find-links=/tmp/wheelhouse pyramid

``pip install packagename`` will find wheels for Windows and OS-X.

``pip install --no-use-wheel`` avoids that.

PyPi
-----

The Python package index:

https://pypi.python.org/pypi

You've all used this -- ``pip install`` searches it.

To upload your package to PyPi::

  python setup.py register

  python setup.py sdist bdist_wheel upload


http://docs.python.org/2/distutils/packageindex.html


Under Development
------------------

Develop mode is *really* *really* nice::

  python setup.py develop

or::

  pip install -e ./

It puts links into the python installation to your code, so that your package is installed, but any changes will immediately take effect.

This way all your test code, and client code, etc, can all import your package the usual way.

No ``sys.path`` hacking

Good idea to use it for anything more than a single file project.

(requires ``setuptools``)

Running tests
-------------

It can be a good idea to set up yoru tests to be run from ``setup.py``

So that you (or your users) can:

.. code-block:: bash

  $ pip install .
  $ python setup.py test

Do do this, you need to add a ``test_suite`` stanza in setup.py.

**nose**

.. code-block:: python

  setup (
      # ...
      test_suite = 'nose.collector'
  )

**pytest**

.. code-block:: python

  setup(
    #...,
    setup_requires=['pytest-runner', ...],
    tests_require=['pytest', ...],
    #...,
  )

And create an alias into setup.cfg file::

  [aliases]
  test=pytest

https://pytest.org/latest/goodpractices.html#integrating-with-setuptools-python-setup-py-test-pytest-runner

**unittest**

.. code-block:: python


  test_suite="tests"

(does py3 unittest have this??)


Handling the version number:
----------------------------

One key rule in software (and ANY computer use!):

Never put the same information in more than one place!

With a python package, you want:

.. code-block:: python

  import the_package

  the_package.__version__

To return the version string -- something like:

"1.2.3"

But you also need to specify it in the ``setup.py``:

.. code-block:: python

  setup(name='package_name',
        version="1.2.3",
        ...
        )

Not Good.

My solution:

Put the version in the package __init__

__version__ = "1.2.3"

In the setup.py, you could import the package to get the version number
... but it not a safe practice to import you package when installing
it (or building it, or...)

So: read the __version__ string yourself::

.. code-block:: python

  def get_version():
      """
      Reads the version string from the package __init__ and returns it
      """
      with open(os.path.join("capitalize", "__init__.py")) as init_file:
          for line in init_file:
              parts = line.strip().partition("=")
              if parts[0].strip() == "__version__":
                  return parts[2].strip().strip("'").strip('"')
      return None





Semantic Versioning
-------------------

Another note on version numbers.

The software development world (at least the open-source one...) has
established a standard for what version numbers mean, known as semantic
versioning. This is helpful to users, as they can know what to expect
they upgrade.

In short, with a x.y.z version number:

x is the major version -- it could mean changes in API, major features, etc.

  - Likely to to be incompatible with previous versions

y is the minor version -- added features, etc, but backwards compatible.

z is the "bugfix" version -- fixed bugs, should be compatible.

FIXME: link to good semantic versioning reference.


Tools to help:
--------------

Tox:

https://tox.readthedocs.io/en/latest/

Versioneer:

https://github.com/warner/python-versioneer


Getting Started
----------------

For anything but a single-file script (and maybe even then):

1. Create the basic package structure

2. Write a ``setup.py``

3. ``python -m pip install -e .``

4. Put some tests in ``package/test``

5. ``py.test`` or ``nosetests``


LAB
---

* Create a small package

  - package structure

  - ``setup.py``

  - ``python setup.py develop``

  - ``at least one working test``


* If you are ready -- it can be the start of your project package.

(otherwise you may start with the silly code in ``Examples/capitalize``)





