#!/usr/bin/python

import sys
import os
import argparse
import ast
import json
import subprocess
import shlex

HEXDUMP = "hexdump {} -s {} -n {} -f hexdump.cfg"

def coordcompare(a, coord):
    if isinstance(coord, list) and len(coord) == 2:
        return a in range(coord[0], coord[1] + 1)
    elif isinstance(coord, int):
        return a == coord
    else:
        raise ValueError("Unknwon coordinate type")

def addcellcolor(color, elt):
    return  " \\cellcolor{{{}}} {}".format(color, elt)

def parselines(lines, coordinates=None):
    # Assumes the input file only contains LaTeX tabular rows (the interior of
    # the tabular environment), and that the format is [offset & byte1 & byte2 &
    # ... & ascii]

    result = []
    for i, line in enumerate(lines):
        line = line.split("&")
        if len(line) == 1:
            continue

        addr = line[0]
        bytes = line[1:17]
        chars = ["\\verb|{}|".format(letter) for letter in line[17:33]]

        for j, byte in enumerate(bytes):
            spec = None
            for coord in coordinates:
                if coordcompare(i, coord.get("i")):
                    if coord.get("j") == None or coordcompare(j, coord.get("j")):
                        spec = coord
                        break

            if spec:
                bytes[j] = addcellcolor(spec.get("c", args.default_color), bytes[j])
                if args.highlight_ascii:
                    chars[j] = addcellcolor(spec.get("c", args.default_color), chars[j])


        result.append("&".join([addr, *bytes, *chars]) + "\\\\")
                
    return '\n'.join(result)

def parsedump(dump):
    try:
        lines = subprocess.run(
            shlex.split(
                HEXDUMP.format(dump["f"], dump.get("s", "0x00"), dump.get("n", "0x00"))
            ), check=True, capture_output=True
        ).stdout.decode("utf-8").split('\n')
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode("utf-8"))
        raise

    name = "{}-{}-{}-{}".format(
        dump["t"],
        os.path.splitext(os.path.basename(dump["f"]))[0],
        dump.get("s", "0x00"),
        dump.get("n", "0x00")
    )

    for n, perm in enumerate(dump["p"]):
        with open(os.path.join(args.outputdir, "{}.{}.tex".format(name, n)), 'w') as o:
            o.write(parselines(lines, coordinates=perm))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="highlight_hexdump", formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "input", help="Configuration JSON"
    )

    parser.add_argument(
        "-o", "--outputdir", default="", help="Output directory"
    )

    parser.add_argument(
        "-d", "--default_color", default="blue!40",
        help="The default color to use for coloring selected cell coordinates when a color is not provided in the coordinate."
    )

    parser.add_argument(
        "-H", "--highlight-ascii", default=False, action="store_true",
        help="In addition to highlighting the byte display, also hightlight the ASCII display."
    )

    args = parser.parse_args()
    with open(args.input) as inf:
        config = json.load(inf)
        for dump in config:
            parsedump(dump)
