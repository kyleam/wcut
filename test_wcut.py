import unittest
from io import StringIO

from wcut import match_fields, process_lines, write_fields


class TestCore(unittest.TestCase):

    def test_no_matching_fields(self):
        fields = ['f1', 'f2']
        searches = ['seal', 'parrot']
        self.assertEqual(list(match_fields(fields, searches)), [])

    def test_match_with_empty_field(self):
        fields = ['f1', 'f2']
        searches = ['']
        self.assertEqual(list(match_fields(fields, searches)), [])

    def test_match_case_sensitive(self):
        fields = ['Seal', 'PARROT']
        searches = ['seal', 'parrot']
        self.assertEqual(list(match_fields(fields, searches)), [])
        self.assertEqual(list(match_fields(fields, searches, ignore_case=True)),
                         [0, 1])

    def test_match_partial(self):
        fields = ['seal', 'parrot']
        searches = ['se', 'par']
        self.assertEqual(list(match_fields(fields, searches)), [0, 1])

    def test_match_wholename(self):
        fields = ['seal', 'parrot']
        searches = ['se', 'par']
        self.assertEqual(list(match_fields(fields, searches, wholename=True)),
                         [])
        self.assertEqual(list(match_fields(fields, fields, wholename=True)),
                         [0, 1])

    def test_match_with_repeated_fields(self):
        fields = ['seal', 'parrot', 'parrot']
        searches = ['seal', 'parrot']
        self.assertEqual(list(match_fields(fields, searches)), [0, 1, 2])

    def test_match_with_repeated_searches(self):
        fields = ['seal', 'parrot']
        searches = ['seal', 'parrot', 'parrot']
        self.assertEqual(list(match_fields(fields, searches)), [0, 1])

    def test_singlespace_delim(self):
        lines = [(1, 'c1 c2 c3'),
                 (2, '1 2 3')]
        expected_result = [['c1', 'c2', 'c3'],
                           ['1', '2', '3']]
        result = list(process_lines(lines, ' ', ['c1', 'c2', 'c3']))
        self.assertEqual(result, expected_result)

    def test_tab_delim(self):
        lines = [(1, 'c1\tc2\tc3'),
                 (2, '1\t2\t3')]
        expected_result = [['c1', 'c2', 'c3'],
                           ['1', '2', '3']]

        result = list(process_lines(lines, '\t', ['c1', 'c2', 'c3']))
        self.assertEqual(result, expected_result)

    def test_match_second_line_match(self):
        lines = [(1, 'not considered'),
                 (2, 'matched nomatch'),
                 (3, '1 2')]
        expected_result = [['matched',],
                           ['1',]]

        result = list(process_lines(lines, ' ', ['matched',],
                                    match_lineno=2))
        self.assertEqual(result, expected_result)

    def test_match_in_reverse_order(self):
        lines = [(1, 'c1 c2 c3'),
                 (2, '1 2 3')]
        expected_result = [['c2', 'c1'],
                           ['2', '1']]

        result = list(process_lines(lines, ' ', ['c2', 'c1']))
        self.assertEqual(result, expected_result)

    def test_lines_ends_with_blank_line(self):
        lines = [(1, 'c1 c2 c3'),
                 (2, '\n')]
        expected_result = [['c1', 'c2'],
                           '\n']

        result = list(process_lines(lines, ' ', ['c1', 'c2']))
        self.assertEqual(result, expected_result)

    def test_lines_with_blank_line_inside(self):
        lines = [(1, 'c1 c2 c3'),
                 (2, '\n'),
                 (3, '1 2 3')]
        expected_result = [['c1', 'c2'],
                           '\n',
                           ['1', '2']]

        result = list(process_lines(lines, ' ', ['c1', 'c2']))
        self.assertEqual(result, expected_result)

    def test_multisource_lines(self):
        lines = [(1, 'c1 c2 c3'),
                 (2, '1 2 3'),
                 (1, 'c1 c2 c3'),
                 (2, '4 5 6')]
        expected_result = [['c1', 'c2', 'c3'],
                           ['1', '2', '3'],
                           ['4', '5', '6']]

        result = list(process_lines(lines, ' ', ['c1', 'c2', 'c3']))
        self.assertEqual(result, expected_result)

    def test_multisource_lines_different_order(self):
        lines = [(1, 'c1 c2 c3'),
                 (2, '1 2 3'),
                 (1, 'c1 c3 c2'),
                 (2, '4 6 5')]
        expected_result = [['c1', 'c2', 'c3'],
                           ['1', '2', '3'],
                           ['4', '5', '6']]

        result = list(process_lines(lines, ' ', ['c1', 'c2', 'c3']))
        self.assertEqual(result, expected_result)

    def test_write_fields(self):
        ofh = StringIO()
        towrite = [['c1', 'c2'],
                   ['1', '2']]
        write_fields(ofh, towrite, ' ')
        result = ofh.getvalue()
        expected_result = 'c1 c2\n1 2\n'
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
