import itertools


def suppress_preheader_lines(lines, header):
    """Discard `lines` before `header`.

    Parameters
    ----------
    lines : iterable
        Provides line number (1-based) and line (str).
    header : int
    """
    return itertools.dropwhile(lambda line: line[0] < header,
                               lines)


def suppress_no_delim_lines(lines, delim):
    """Discard `lines` that do not contain `delim`.

    Parameters
    ----------
    lines : iterable
        Provides line number (1-based) and line (str).
    delim : str
    """
    for line in lines:
        if delim not in line[1]:
            continue
        yield line


class WcutError(Exception):
    pass


def extract_fields(lines, delim, searches, match_lineno=1, **kwargs):
    """Return generator of fields matching `searches`.

    Parameters
    ----------
    lines : iterable
        Provides line number (1-based) and line (str)
    delim : str
        Delimiter to split line by to produce fields
    searches : iterable
        Returns search (str) to match against line fields.
    match_lineno : int
        Line number of line to split and search fields

    Remaining keyword arguments are passed to `match_fields`.
    """
    keep_idx = []
    for lineno, line in lines:
        if lineno < match_lineno or delim not in line:
            if lineno == match_lineno:
                raise WcutError('Delimter not found in line {}'.format(
                    match_lineno))
            yield [line]
            continue

        fields = line.split(delim)
        if lineno == match_lineno:
            keep_idx = list(match_fields(fields, searches, **kwargs))
        keep_fields = [fields[i] for i in keep_idx]

        if keep_fields:
            yield keep_fields


def match_fields(fields, searches,
                 ignore_case=False, wholename=False, complement=False):
    """Return fields that match searches.

    Parameters
    ----------
    fields : iterable
    searches : iterable
    ignore_case, wholename, complement : boolean
    """
    if ignore_case:
        fields = [f.lower() for f in fields]
        searches = [s.lower() for s in searches]
    if wholename:
        match_found = _complete_match
    else:
        match_found = _partial_match

    fields = [(i, field) for i, field in enumerate(fields)]
    matched = []
    for search, (idx, field) in itertools.product(searches, fields):
        if not search:  ## don't return all fields for ''
            continue
        if match_found(search, field) and idx not in matched:
            matched.append(idx)

    if complement:
        matched = [idx for idx in list(zip(*fields))[0] if idx not in matched]

    return matched


def _complete_match(search, target):
    return search == target


def _partial_match(search, target):
    return search in target
