import sys
import fileinput
from itertools import product


def match_fields(fields, searches, ignore_case=False, wholename=False):
    """Return a generator with fields that match searches

    Parameters
    ----------
    fields : iterable
    searches : iterable
    ignore_case, wholename : boolean
    """
    already_yielded = set()
    if ignore_case:
        fields = [f.lower() for f in fields]
        searches = [s.lower() for s in searches]
    if wholename:
        match_found = _complete_match
    else:
        match_found = _partial_match

    fields = [(i, field) for i, field in enumerate(fields)]
    for search, field in product(searches, fields):
        if not search:  ## don't return all fields for ''
            continue
        if match_found(search, field[1]) and field[0] not in already_yielded:
            yield field[0]
            already_yielded.add(field[0])


def _complete_match(search, target):
    return search == target


def _partial_match(search, target):
    return search in target


def get_lines(files):
    """Return generator with line number and line tuples for each file in
    `files`
    """
    for line in fileinput.input(files):
        yield fileinput.filelineno(), line


def process_lines(lines, delim, searches, match_lineno=1, **kwargs):
    """Return generator of fields matching `searches`

    Parameters
    ----------
    lines : iterable
        returns line number (1-based) and line (str)
    delim : str
        delimiter to split line by to produce fields
    searches : iterable
        returns search (str) to match against line fields
    match_lineno : int
        line number of line to split and search fields

    kwargs passed to `match_fields`
    """
    processed_matchline = False
    for lineno, line in lines:
        fields = line.strip().split(delim)
        if lineno < match_lineno:
            continue
        elif lineno == match_lineno:
            keep_fields = list(match_fields(fields, searches, **kwargs))
            if processed_matchline:
                ## already yielded header once, so don't repeat it for
                ## additional files
                continue
            processed_matchline = True
        yield [fields[i] for i in keep_fields]


def write_fields(ofh, field_lines, delim):
    for fields in field_lines:
        ofh.write(delim.join(fields) + '\n')
