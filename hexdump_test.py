#!/usr/bin/python

import hexdump_latex
import pprint

with open("dump.hex", 'r') as f:
    lines = f.readlines()
    with open("dump.tex", 'w') as g:
        g.write("\n".join(hexdump_latex.parselines(lines[:-1])))
