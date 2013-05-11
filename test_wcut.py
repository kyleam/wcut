import pytest
from io import StringIO

from wcut import match_fields, process_lines, io, cli


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
    assert list(match_fields(digits, animals)) == []


def test_match_with_empty_field(digits):
    assert list(match_fields(digits, [''])) == []


def test_match_case_sensitive(animals):
    upper = [a.upper() for a in animals]
    assert list(match_fields(upper, animals)) == []
    assert list(match_fields(upper, animals, ignore_case=True)) == [0, 1]


def test_match_partial(animals):
    partial = [a[:2] for a in animals]
    assert list(match_fields(animals, partial)) == [0, 1]


def test_match_wholename(animals):
    partial = [a[:2] for a in animals]
    assert list(match_fields(animals, partial, wholename=True)) == []
    assert list(match_fields(animals, animals, wholename=True)) == [0, 1]


def test_match_with_repeated_fields(animals):
    repeat = animals + animals[-1:]
    assert list(match_fields(repeat, animals)) == [0, 1, 2]


def test_match_with_repeated_searches(animals):
    repeat = animals + ['parrot']
    assert list(match_fields(animals, repeat)) == [0, 1]


## delim


def test_delims(delim):
    expected = [['c1', 'c2', 'c3'], ['1', '2', '3']]
    lines = [(lineno, delim.join(line)) for lineno, line in enumerate(expected, 1)]
    result = list(process_lines(lines, delim, ['c1', 'c2', 'c3']))
    assert result == expected


## line skip


def test_match_second_line_match():
    lines = [(1, 'not considered'),
             (2, 'matched nomatch'),
             (3, '1 2')]
    expected_result = [['not considered'],
                       ['matched',],
                       ['1',]]

    result = list(process_lines(lines, ' ', ['matched',],
                                match_lineno=2))
    assert result == expected_result


## order change


def test_match_in_reverse_order():
    lines = [(1, 'c1 c2 c3'),
             (2, '1 2 3')]
    expected_result = [['c2', 'c1'],
                       ['2', '1']]

    result = list(process_lines(lines, ' ', ['c2', 'c1']))
    assert result == expected_result


## blank lines


def test_lines_ends_with_blank_line():
    lines = [(1, 'c1 c2 c3'),
             (2, '\n')]
    expected_result = [['c1', 'c2'],
                       ['\n']]

    result = list(process_lines(lines, ' ', ['c1', 'c2']))
    assert result == expected_result


def test_lines_with_blank_line_inside():
    lines = [(1, 'c1 c2 c3'),
             (2, '\n'),
             (3, '1 2 3')]
    expected_result = [['c1', 'c2'],
                       ['\n'],
                       ['1', '2']]

    result = list(process_lines(lines, ' ', ['c1', 'c2']))
    assert result == expected_result


## multiple inputs


def test_multisource_lines():
    lines = [(1, 'c1 c2 c3'),
             (2, '1 2 3'),
             (1, 'c1 c2 c3'),
             (2, '4 5 6')]
    expected_result = [['c1', 'c2', 'c3'],
                       ['1', '2', '3'],
                       ['4', '5', '6']]
    result = list(process_lines(lines, ' ', ['c1', 'c2', 'c3']))
    assert result == expected_result


def test_multisource_lines_different_order():
    lines = [(1, 'c1 c2 c3'),
             (2, '1 2 3'),
             (1, 'c1 c3 c2'),
             (2, '4 6 5')]
    expected_result = [['c1', 'c2', 'c3'],
                       ['1', '2', '3'],
                       ['4', '5', '6']]

    result = list(process_lines(lines, ' ', ['c1', 'c2', 'c3']))
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


def linegen(dummy, lines=None, linenos=None):
    if lines  is None:
        lines = ['# before header', 'c1 c2 c3', 'nodelim', '1 2 3']
    if linenos is None:
        linenos = range(1, len(lines) + 1)
    for lineno, line in zip(linenos, lines):
        yield lineno, line


def test_remove_preheader():
    func = io.suppress_preheader_lines(linegen, 2)
    results = list(func(None))
    expected = [(2, 'c1 c2 c3'), (3, 'nodelim'), (4, '1 2 3')]
    assert results == expected


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
