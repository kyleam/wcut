wcut - cut with words
=====================

wcut is intended to be very similar to the unix command line utility
cut, but with words instead.

For example, suppose you have a file (``feng-rpkm.txt``) with the
contents::

  geneid,gname,rpkm
  666666,feng3,9999

With cut, you could run ``cut -d',' -f2 feng-rpkm.txt`` to get the
``gname`` column. This is easy if you only have a few fields. For a
larger number of fields, it gets annoying to count columns. With wcut,
you would run::

  $ wcut -d',' gname feng-rpkm.txt

If you wanted the ``rpkm`` and ``gname`` column, but in reverse order,
you could run::

  $ wcut -d',' rpkm,gname feng-rpkm.txt


Install
-------

Install

::

  $ pip install wcut

Install an editable version from the git repo

::

  $ git clone git@github.com:kyleam/wcut.git
  $ pip install -e wcut


Issues
------

Let me know if you have any problems with the program. Suggestions and
contributions are welcome.
