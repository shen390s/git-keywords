#!/usr/bin/env python3
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# $Date$
#
# To the extent possible under law, Roland Smith has waived all copyright and
# related or neighboring rights to kwset.py. This work is published from
# the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Fill the Date and Revision keywords from the latest git commit and tag and
   subtitutes them in the standard input."""

import fileinput
import os
import re
import subprocess


def gitdate():
    """Get the date from the latest commit in ISO8601 format.
    """
    args = ['git', 'log',  '-1', '--date=iso']
    outdata = subprocess.check_output(args, universal_newlines=True)
    outlines = outdata.splitlines()
    dline = [l for l in outlines if l.startswith('Date')]
    try:
        dat = dline[0][5:].strip()
        return ''.join(['$', 'Date: ', dat, ' $'])
    except IndexError:
        raise ValueError('Date not found in git output')


def gitrev():
    """Get the latest tag and use it as the revision number. This presumes the
    habit of using numerical tags. Use the short hash if no tag available.
    """
    args = ['git', 'describe',  '--tags', '--always']
    try:
        with open(os.devnull, 'w') as bb:
            r = subprocess.check_output(args, stderr=bb,
                                        universal_newlines=True)[:-1]
    except subprocess.CalledProcessError:
        return ''.join(['$', 'Revision', '$'])
    return ''.join(['$', 'Revision: ', r, ' $'])


def main():
    """Main program.
    """
    dre = re.compile(''.join([r'\$', r'Date:?\$']))
    rre = re.compile(''.join([r'\$', r'Revision:?\$']))
    currp = os.getcwd()
    if not os.path.exists(currp+'/.git'):
        print >> sys.stderr, 'This directory is not controlled by git!'
        sys.exit(1)
    date = gitdate()
    rev = gitrev()
    for line in fileinput.input():
        line = dre.sub(date, line)
        print(rre.sub(rev, line), end="")


if __name__ == '__main__':
    main()
