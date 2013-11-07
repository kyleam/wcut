import sys
import fileinput


class stdout_check:
    def __init__(self, target, stdout_flags=['-']):
        """Open `target` as stdout if it is empty or in `stdout_flags`
        """
        if not target or target in stdout_flags:
            self.target = sys.stdout
        else:
            self.target = open(target, 'w')

    def __enter__(self):
        return self.target

    def __exit__(self, type, value, tb):
        if self.target is not sys.stdout:
            self.target.close()


def get_lines(fname):
    """Return generator with line number and line for file `fname`
    """
    for line in fileinput.input(fname):
        yield fileinput.filelineno(), line.strip()


def write_fields(ofh, field_lines, delim):
    for fields in field_lines:
        ofh.write(delim.join(fields) + '\n')
