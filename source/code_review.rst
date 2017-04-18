:orphan:

.. _code_review:

############
Code Reviews
############


Why code review
===============
As professional developers, we need to always be learning and improving.

Code review is one of the best tools for this.

Code review is like having a personal tutor.


Getting code ready for review
-----------------------------

- Write tests - if there are tests, much easier to make changes on the fly during review
- First draft is messy, refactor
- To get the most out of it, correct all that you can before review
- Expect advice and corrections, and learn from them!


Size of code
------------

- Code to review should be between 200 and 400 lines of code
- Code can, and often will, be part of a bigger project
- Code should be modular, so can look at one smallish piece:
   - and still be able to explain how it fits in the bigger project
   - and be able to explain what the smallish piece is doing in a few sentences


When/Why to review code
-----------------------

- Think your code is ready for production
- Have code working, but seems there is probably a better way
- Totally Stuck
- Having difficulty making it modular, can help you break large chunks into smaller chunks


What to look for
----------------

- readability
- 'pythonic'
- tests
- short functions/methods
- anything not clear
- logic issues


Types of code review
--------------------

- in person
- in-line comments
- using tools https://en.wikipedia.org/wiki/List_of_tools_for_code_review


When refactoring or doing code reviews in person
------------------------------------------------

Write a comment explaining what the code is doing and/or questions about the code

Then, if time permits you can jointly:

- work on making the code clearer
- run tests after changes
- goal to make it clear enough to get rid of the comment(s) that were added

Or do this yourself afterwards, as you would for written code reviews
