#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Time-stamp: <2012-06-29 23:25:24 rsmith>
#
# To the extent possible under law, Roland Smith has waived all copyright and
# related or neighboring rights to kwclean.py. This work is published from the
# Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Remove the Date and Revision keyword contents from the standard input."""

import sys
import re

for line in sys.stdin:
    line = re.sub('\$Date.*\$', '$Date$', line)
    print re.sub('\$Revision.*\$', '$Revision$', line),
