from itertools import product


def extract_fields(lines, delim, searches, match_lineno=1, **kwargs):
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
    keep_idx = []
    for lineno, line in lines:
        if lineno < match_lineno or delim not in line:
            yield [line]
            continue

        fields = line.split(delim)
        if lineno == match_lineno:
            keep_idx = list(match_fields(fields, searches, **kwargs))
            if processed_matchline:
                ## already yielded header once, so don't repeat it for
                ## additional files
                continue
            processed_matchline = True
        keep_fields = [fields[i] for i in keep_idx]

        if keep_fields:
            yield keep_fields


def match_fields(fields, searches,
                 ignore_case=False, wholename=False, complement=False):
    """Return fields that match searches

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
    for search, (idx, field) in product(searches, fields):
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
