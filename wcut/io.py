import fileinput


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



def get_lines(files, match_lineno=None):
    """
    Parameters
    ----------
    files : list of str
    match_lineno : None or int
        if given, lines before this are discared
    """
    linefunc = _get_lines
    if match_lineno:
        suppress_preheader_lines(linefunc, match_lineno)
    if delim:
        suppress_no_delim_lines(linefunc, delim)
    return linefunc(files)


def _get_lines(files):
    """Return generator with line number and line tuples for each file in
    `files`
    """
    for line in fileinput.input(files):
        yield fileinput.filelineno(), line.strip()


def suppress_preheader_lines(linefunc, match_lineno):
    def wrapped(files):
        for lineno, line in linefunc(files):
            if lineno < match_lineno:
                continue
            yield lineno, line
    return wrapped


def write_fields(ofh, field_lines, delim):
    for fields in field_lines:
        ofh.write(delim.join(fields) + '\n')
