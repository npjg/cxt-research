#!/usr/bin/python

import sys
import argparse
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

        theAddress = theSplit[0][3:].strip()
        theBytes = theSplit[1].strip().split()
        theBytes +=  ["  "] * ((major_len*minor_len) - len(theBytes))
        theAscii = theSplit[2].lstrip()

        latex.append("  {} \\\\".format(
            " & ".join([theAddress, *theBytes, "\\verb│{}│".format(
                theAscii if args.with_unicode else re.sub(r'[^\x00-\x7F]','.', theAscii)
            )])))

    latex.append("\\end{tabular}\n")

    return latex

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="hex2latex", formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-U", "--with-unicode", action="store_true",
        help="Include Unicode characters in TeX file (requires XeTeX to compile)"
    )

    args = parser.parse_args()
    print("\n".join(parselines(sys.stdin.readlines())))
