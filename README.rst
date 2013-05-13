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

To install

::

  $ pip install -e git+https://github.com/kyleam/wcut.git@0.3.0#egg=wcut


Or

::

  $ git clone git@github.com:kyleam/wcut.git
  $ pip install -e wcut


If you're not using `virtualenv
<http://www.virtualenv.org/en/latest/>`_, you'll probably need elevated
permissions to do this.


Issues
------

Let me know if you have any problems with the program. Suggestions and
contributions are welcome.
