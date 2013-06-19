import pytest
from io import StringIO

from wcut import (match_fields, extract_fields,
                  suppress_preheader_lines, suppress_no_delim_lines,
                  io, cli)


@pytest.fixture
def animals():
    return ['seal', 'otter']

@pytest.fixture
def digits():
    return ['pinky', 'big']


@pytest.fixture(params=[' ', ',', '\t'])
def delim(request):
    return request.param


## field matching


def test_no_matching_fields(digits, animals):
    assert match_fields(digits, animals) == []


def test_match_with_empty_field(digits):
    assert match_fields(digits, ['']) == []


def test_match_case_sensitive(animals):
    upper = [a.upper() for a in animals]
    assert match_fields(upper, animals) == []
    assert match_fields(upper, animals, ignore_case=True) == [0, 1]


def test_match_partial(animals):
    partial = [a[:2] for a in animals]
    assert match_fields(animals, partial) == [0, 1]


def test_match_wholename(animals):
    partial = [a[:2] for a in animals]
    assert match_fields(animals, partial, wholename=True) == []
    assert match_fields(animals, animals, wholename=True) == [0, 1]


def test_match_with_repeated_fields(animals):
    repeat = animals + animals[-1:]
    assert match_fields(repeat, animals) == [0, 1, 2]


def test_match_with_repeated_searches(animals):
    repeat = animals + ['parrot']
    assert match_fields(animals, repeat) == [0, 1]


def test_match_search_with_complement(animals):
    assert match_fields(animals, ['otter'], complement=True) == [0]
    assert match_fields(animals, ['otter', 'seal'], complement=True) == []


## delim


def test_extract_fields_delims(delim):
    expected = [['c1', 'c2', 'c3'], ['1', '2', '3']]
    lines = [(lineno, delim.join(line)) for lineno, line in enumerate(expected, 1)]
    result = list(extract_fields(lines, delim, ['c1', 'c2', 'c3']))
    assert result == expected


## line skip


def test_extract_fields_match_second_line_match():
    lines = [(1, 'not considered'),
             (2, 'matched nomatch'),
             (3, '1 2')]
    expected_result = [['not considered'],
                       ['matched',],
                       ['1',]]

    result = list(extract_fields(lines, ' ', ['matched',],
                                match_lineno=2))
    assert result == expected_result


## order change


def test_extract_fields_match_in_reverse_order():
    lines = [(1, 'c1 c2 c3'),
             (2, '1 2 3')]
    expected_result = [['c2', 'c1'],
                       ['2', '1']]

    result = list(extract_fields(lines, ' ', ['c2', 'c1']))
    assert result == expected_result


## no matches


def test_extract_fields_no_matches():
    lines = [(1, 'c1 c2 c3'),
             (2, '1 2 3')]
    expected_result = []

    result = list(extract_fields(lines, ' ', ['notmatched']))
    assert result == expected_result


def test_extract_fields_no_matches_preheader():
    lines = [(1, 'preheader'),
             (2, 'c1 c2 c3'),
             (3, '1 2 3')]
    expected_result = [['preheader']]
    result = list(extract_fields(lines, ' ', ['notmatched'],
                                 match_lineno=2))
    assert result == expected_result


def test_extract_fields_no_matches_preheader_wronglineo():
    lines = [(1, 'preheader'), (2, 'c1 c2 c3'),
             (3, '1 2 3')]
    expected_result = [['preheader']]
    result = list(extract_fields(lines, ' ', ['c1'],
                                 match_lineno=1))
    assert result == expected_result


def test_extract_fields_match_lineno_toobig():
    lines = [(1, 'c1 c2 c3'),
             (2, '1 2 3')]
    ## treated as preheader
    expected_result = [[i[1]] for i in lines]
    result = list(extract_fields(lines, ' ', ['c1'],
                                 match_lineno=3))
    assert result == expected_result


def test_extract_fields_match_lineno_toosmall():
    lines = [(1, 'c1 c2 c3'),
             (2, '1 2 3')]
    expected_result = []
    result = list(extract_fields(lines, ' ', ['c1'],
                                 match_lineno=0))
    assert result == expected_result


## blank lines


def test_extract_fields_lines_ends_with_blank_line():
    lines = [(1, 'c1 c2 c3'),
             (2, '\n')]
    expected_result = [['c1', 'c2'],
                       ['\n']]

    result = list(extract_fields(lines, ' ', ['c1', 'c2']))
    assert result == expected_result


def test_extract_fields_lines_with_blank_line_inside():
    lines = [(1, 'c1 c2 c3'),
             (2, '\n'),
             (3, '1 2 3')]
    expected_result = [['c1', 'c2'],
                       ['\n'],
                       ['1', '2']]

    result = list(extract_fields(lines, ' ', ['c1', 'c2']))
    assert result == expected_result


## multiple inputs


def test_extract_fields_multisource_lines():
    lines = [(1, 'c1 c2 c3'),
             (2, '1 2 3'),
             (1, 'c1 c2 c3'),
             (2, '4 5 6')]
    expected_result = [['c1', 'c2', 'c3'],
                       ['1', '2', '3'],
                       ['4', '5', '6']]
    result = list(extract_fields(lines, ' ', ['c1', 'c2', 'c3']))
    assert result == expected_result


def test_extract_fields_multisource_lines_different_order():
    lines = [(1, 'c1 c2 c3'),
             (2, '1 2 3'),
             (1, 'c1 c3 c2'),
             (2, '4 6 5')]
    expected_result = [['c1', 'c2', 'c3'],
                       ['1', '2', '3'],
                       ['4', '5', '6']]

    result = list(extract_fields(lines, ' ', ['c1', 'c2', 'c3']))
    assert result == expected_result


## write fields


def test_write_fields():
    ofh = StringIO()
    towrite = [['c1', 'c2'],
               ['1', '2']]
    io.write_fields(ofh, towrite, ' ')
    result = ofh.getvalue()
    expected_result = 'c1 c2\n1 2\n'
    assert result == expected_result


## --remove-preheader


def test_remove_preheader_with_preheader():
    lines = [(1, 'preheader'),
             (2, '1 2 3')]
    result = list(suppress_preheader_lines(lines, 2))
    expected = [(2, '1 2 3')]
    assert result == expected


## --only-delimited


def test_remove_nodelim_with_nodelim():
    lines = [(1, 'nodelim'),
             (2, '1 2 3'),
             (3, 'and_no_delim')]
    result = list(suppress_no_delim_lines(lines, ' '))
    expected = [(2, '1 2 3')]
    assert result == expected


def test_remove_nodelim_when_all_have_delim():
    lines = [(1, '1 2 3'),
             (2, '3 4 5')]
    result = list(suppress_no_delim_lines(lines, ' '))
    expected = [(1, '1 2 3'), (2, '3 4 5')]
    assert result == expected


def test_remove_preheader_and_no_delim():
    lines = [(1, 'preheader'),
             (2, '1 2 3'),
             (3, 'nodelim')]
    lines = suppress_preheader_lines(lines, 2)
    lines = suppress_no_delim_lines(lines, ' ')
    result = list(lines)
    expected = [(2, '1 2 3')]
    assert result == expected


## process command line


@pytest.fixture
def args():
    defaults = {
        'WORDS': 'search1,search2',
        'FILE': None,
        '--delimiter': '" "',
        '--line': '1',
        '--help': False,
        '--remove-preheader': False,
        '--only-delimited': False,
        '--ignore-case': False,
        '--wholename': False,
        '-o': None,
    }
    return defaults


def test_process_commandline_double_quote_delim(args):
    cli.process_commandline(args)
    assert args['--delimiter'] == ' '


def test_process_commandline_single_quote_delim(args):
    args['--delimiter'] = "' '"
    cli.process_commandline(args)
    assert args['--delimiter'] == ' '


def test_process_commandline_tab_delim(args):
    args['--delimiter'] = '\\t'
    cli.process_commandline(args)
    assert args['--delimiter'] == '\t'


def test_process_commandline_words(args):
    cli.process_commandline(args)
    assert args['WORDS'] == ['search1', 'search2']
