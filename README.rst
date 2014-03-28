wcut - cut with words
=====================

wcut is intended to be very similar to the unix command line utility
cut, but with words instead.

For example, suppose you have a file (``feng-rpkm.txt``) with the
contents

::

  geneid,gname,rpkm
  666666,feng3,9999

With cut, you could run ``cut -d',' -f2 feng-rpkm.txt`` to get the
``gname`` column. This is easy if you only have a few fields. For a
larger number of fields, it gets annoying to count columns. With wcut,
you would run

::

  $ wcut -d',' feng-rpkm.txt gname

Similar to cut, the ``--complement`` (or ``-v``) flag will return all
the columns that do not match::

  $ wcut -d',' -v feng-rpkm.txt gname


If you wanted the ``rpkm`` and ``gname`` column, but in reverse order,
you could run

::

  $ wcut -d',' feng-rpkm.txt rpkm gname

See ``wcut --help`` for a full list of options.


Install
-------

wcut can be installed from PyPI using pip.

::

  $ pip install wcut


Issues
------

Please report any issues on `GitHub <https://github.com/kyleam/wcut>`_.
