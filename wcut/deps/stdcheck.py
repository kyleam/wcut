import sys
import os
from source import add_sourceline


class stdin_check:
    def __init__(self, target, stdin_flags=['-']):
        if not target or target in stdin_flags:
            self.target = sys.stdin
        else:
            self.target = open(target, 'r')

    def __enter__(self):
        return self.target

    def __exit__(self, type, value, tb):
        if self.target is not sys.stdin:
            self.target.close()


class stdout_check:
    def __init__(self, target, stdout_flags=['-'],
                 source_line=True, safe=False, **kwargs):
        """Open `target` as either stdout if it is empty or in `stdout_flags`

        If `source_line` is True, adds information about source script
        to outfile.

        If `safe` is True, raises OSError if file exists

        `kwargs` are passed to `add_sourceline` decorator (and, as
        such, is only meaningful if `source_line` is True
        """
        if source_line:
            open_func = add_sourceline(open, **kwargs)
        else:
            open_func = open

        if not target or target in stdout_flags:
            self.target = sys.stdout
        else:
            if safe and os.path.exists(target):
                raise OSError('File {} already exists'.format(target))
            self.target = open_func(target, 'w')

    def __enter__(self):
        return self.target

    def __exit__(self, type, value, tb):
        if self.target is not sys.stdout:
            self.target.close()
