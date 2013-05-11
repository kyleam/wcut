"""Select fields by header keywords

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
      Any lines before this point are printed unless -r option is set.
      [default: 1]
  -r, --remove-preheader
      remove the lines before line N
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


def process_commandline(args):
    delim = args['--delimiter']
    ## strip quotes
    if delim.startswith('"') and delim.endswith('"'):
        delim = delim[1:-1]
    elif delim.startswith("'") and delim.endswith("'"):
        delim = delim[1:-1]
    ## this will work in both python 2 and 3
    delim = delim.encode('utf-8').decode('unicode-escape')
    args['--delimiter'] = delim

    args['WORDS'] = args['WORDS'].split(',')
    args['--line'] = int(args['--line'])
