"""Select fields by header keywords

Usage: wcut [options] WORDS FILE

Arguments:
  WORDS
      Comma-separated keyword list to match against columns
  FILE
      This will be read from stdin if not present or "-".

Options:
  -h, --help
      Print help message.
  -V, --version
  -l, --line=N
      Line N (1-based) of file to match WORDS against.
      Any lines before this point are printed unless -r option is set.
      [default: 1]
  -v, --complement
      Complement the set of fields matched by WORDS.
  -r, --remove-preheader
      Remove the lines before line N.
  -s, --only-delimited
      Do not print lines not containing delimiters.
      This has no effect on lines before line N.
  -d, --delimiter=DELIM
      [default: " "]
  -i, --ignore-case
  -w, --wholename
      Do not allow partial matches for keywords.
  -o OUTFILE

Example:
  $ echo "cat hat bat\\n1 2 3\\n4 5 6" | wcut hat,cat
  hat cat
  2 1
  5 4
"""


def process_commandline(args):
    delim = args['--delimiter']
    ## Strip quotes.
    if delim.startswith('"') and delim.endswith('"'):
        delim = delim[1:-1]
    elif delim.startswith("'") and delim.endswith("'"):
        delim = delim[1:-1]
    ## This should work in both python 2 and 3.
    delim = delim.encode('utf-8').decode('unicode-escape')
    args['--delimiter'] = delim

    args['WORDS'] = args['WORDS'].split(',')
    args['--line'] = int(args['--line'])
