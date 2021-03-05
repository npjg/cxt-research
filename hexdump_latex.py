#!/usr/bin/python

import sys
import re
from strip_ansi import strip_ansi

def parselines(lines, major_len=4, minor_len=4):
    latex = []
    fmt = "@{{}}c|*{{{}}}{{c@{{ }}}}c|c@{{}}".format(major_len*minor_len-1)
    latex.append("\\UseRawInputEncoding\n\\begin{{tabular}}{{{}}}".format(fmt))

    for line in lines:
        line = strip_ansi(line).replace('\n', '')
        if line == '':
            continue

        theSplit = re.split(' │', line, maxsplit=3)

        theBytes = theSplit[1].strip().split()
        theBytes +=  ["  "] * ((major_len*minor_len) - len(theBytes))

        latex.append("  {} \\\\".format(
            " & ".join([
                theSplit[0][3:].strip(),
                *theBytes,
                "\\verb│{}│".format(re.sub(r'[^\x00-\x7F]','.', theSplit[2])[1:])
            ])))

    latex.append("\\end{tabular}\n")

    return latex

if __name__ == "__main__":
    print("\n".join(parselines(sys.stdin.readlines())))
