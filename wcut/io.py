import fileinput


def get_lines(files):
    """Return generator with line number and line tuples for each file in
    `files`
    """
    for line in fileinput.input(files):
        yield fileinput.filelineno(), line


def write_fields(ofh, field_lines, delim):
    for fields in field_lines:
        ofh.write(delim.join(fields) + '\n')
