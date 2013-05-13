import fileinput


def get_lines(files, match_lineno=None, delim=None):
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


def suppress_no_delim_lines(linefunc, delim):
    def wrapped(*args, **kwargs):
        for lineno, line in linefunc(*args, **kwargs):
            if delim not in line:
                continue
            yield lineno, line
    return wrapped


def write_fields(ofh, field_lines, delim):
    for fields in field_lines:
        ofh.write(delim.join(fields) + '\n')
