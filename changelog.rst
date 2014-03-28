1.0.0
-----

* Change command-line handling of column names.
* Fix handling of broken pipes when passing output to commands like
  `head`.


0.4.0
-----

* Raise exception if header line does not contain delimiter
* Allow only one input file
* Add functional tests
* Documentation updates


0.3.2
-----

* Fix --remove-preheader and --only-delimited flags


0.3.1
-----

* Declare docopt as dependency instead of bundling
* Prepare for PyPI


0.3.0
-----

* Option to discard lines that don't contain the delimiter (similar
  cut's ``-s`` flag)
* Option to discard lines before the match line
* Option to  complement the matching fields set
* Don't print blank lines when no matches
* Better handling of incorrect match line numbers


0.2.0
-----

* Option to only return complete matches to name of the field
* Don't print headers multiple times if more than one file is used as
  input
* Deal with blank lines and empty searches better


0.1.0
-----

Initial release
