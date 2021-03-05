#!/usr/bin/python

import sys
import argparse
import re
from strip_ansi import strip_ansi

def parselines(lines, major_len=4, minor_len=4):
    if args.with_ansi_colors:
        from ansi2html import Ansi2HTMLConverter
        conv = Ansi2HTMLConverter(latex=True, inline=True)
    else:
        conv = None

    latex = []
    fmt = "@{{}}c|*{{{}}}{{c@{{ }}}}c|c@{{}}".format(major_len*minor_len-1)

    for line in lines:
        if not conv: line = strip_ansi(line)

        line = line.replace('\n', '')
        if line == '':
            continue

        theSplit = re.split('│', line, maxsplit=3)

        # Bug in the screen reset code of strip_ansi. It should filter away just an m.
        theAddress = theSplit[0].strip()[3:]
        theBytes = [conv.convert(byte, full=False) if conv else byte for byte in  theSplit[1].strip().split()][:-1]
        theBytes +=  ["  "] * ((major_len*minor_len) - len(theBytes) - (0 if conv else 1))
        theAscii = theSplit[2].lstrip()
        if conv: theAscii = conv.convert(theAscii, full=False)
        if not args.with_unicode:
            theAscii = re.sub(r'[^\x00-\x7F]','.', theAscii)
        # theAscii = "".join(["\\verb│{}│".format(char) for char in theAscii])

        latex.append("  {} \\\\".format(" & ".join([theAddress, *theBytes, "\\texttt{{{}}}".format(theAscii)]))) # "\\verb│{}│".format(

    if args.with_ansi_colors:
        cells = conv.convert("\n".join(latex), full=False)
    else:
        cells = "\n".join(latex)

    tabular = "\\UseRawInputEncoding\n\\begin{{tabular}}{{{}}}\n{}\n\\end{{tabular}}\n".format(fmt, cells)
    return tabular

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="hex2latex", formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-U", "--with-unicode", action="store_true",
        help="Include Unicode characters in TeX file (requires XeTeX to compile)"
    )

    parser.add_argument(
        "-A", "--with-ansi-colors", action="store_true",
        help="Translate ANSI color codes into LaTeX colors (requires ansifilter to translate)"
    )

    args = parser.parse_args()
    print(parselines(sys.stdin.readlines()))
