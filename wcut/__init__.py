from wcut import _version
from wcut._core import get_lines, match_fields, process_lines, write_fields

__fullversion__, __version__ = _version.get_version()

_script_doc = """\
Select fields by header keywords

Usage: wcut [options] WORDS [FILE]...

Arguments:
  WORDS
      comma-separated keyword list
  FILE
      read from stdin if not present or -

Options:
  -h, --help
      print help message
  -l, --line=N
      line N (1-based) of file to match WORDS against.
      Any lines before this point are discarded.
      [default: 1]
  -d, --delimiter=DELIM
      [default: " "]
  -i, --ignore-case
  -w, --wholename
      don't allow partial matches for keywords
  -o OUTFILE

Example:
  $ echo "cat hat bat\\n1 2 3\\n4 5 6" | wcut hat,cat
  hat cat
  2 1
  5 4
"""
