import sys
import fileinput
from itertools import product


def match_fields(fields, matches, ignore_case=False, **kwargs):
    already_yielded = set()
    if ignore_case:
        fields = [f.lower() for f in fields]
        matches = [m.lower() for m in matches]
    fields = [(i, field) for i, field in enumerate(fields)]
    for match, field in product(matches, fields):
        if match in field[1] and field[0] not in already_yielded:
            yield field[0]
            already_yielded.add(field[0])


def get_lines(files):
    for line in fileinput.input(files):
        yield fileinput.filelineno(), line


def process_lines(lines, match_lineno, words, delim, **kwargs):
    processed_matchline = False
    for lineno, line in lines:
        fields = line.strip().split(delim)
        if lineno < match_lineno:
            continue
        elif lineno == match_lineno:
            keep_fields = [f for f in match_fields(fields, words, **kwargs)]
            if processed_matchline:
                ## already yielded header once, so don't repeat it for
                ## additional files
                continue
            processed_matchline = True
        yield [fields[i] for i in keep_fields]


def write_fields(ofh, field_lines, delim):
    for fields in field_lines:
        ofh.write(delim.join(fields) + '\n')
