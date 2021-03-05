#!/usr/bin/python

import sys
import argparse
import re
from strip_ansi import strip_ansi

def parselines(lines, major_len=4, minor_len=4):
    latex = []
    fmt = "@{{}}c|*{{{}}}{{c@{{ }}}}c|c@{{}}".format(major_len*minor_len-1)

    for line in lines:
        if not args.with_ansi_colors:
            line = strip_ansi(line)

        line = line.replace('\n', '')
        if line == '':
            continue

        theSplit = re.split('│', line, maxsplit=3)

        theAddress = theSplit[0].strip()
        theBytes = theSplit[1].strip().split()
        theBytes +=  ["  "] * ((major_len*minor_len) - len(theBytes))
        theAscii = theSplit[2].lstrip()

        latex.append("  {} \\\\".format(
            " ﹠ ".join([theAddress, *theBytes, "\\texttt{{{}}}".format( # "\\verb│{}│".format(
                theAscii if args.with_unicode else re.sub(r'[^\x00-\x7F]','.', theAscii)
            )])))

    if args.with_ansi_colors:
        import subprocess
        res = subprocess.run(["ansifilter", "-L"], input="\n".join(latex).encode('utf-8'), capture_output=True, check=True)
        cells = res.stdout.decode("utf-8")
        cells = cells.split("\n")
        cells = "\n\n".join(cells[7:-3])
    else:
        cells = "\n".join(latex)

    tabular = "\\UseRawInputEncoding\n\\begin{{tabular}}{{{}}}\n{}\n\\end{{tabular}}\n".format(fmt, cells.replace("﹠", "&"))
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
