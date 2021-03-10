#!/usr/bin/python

import sys
import os
import argparse
import ast
import json
import subprocess
import shlex

HEXDUMP = "hexdump {} -s {} -n {} -f hexdump.cfg"

def parselines(lines, coordinates=None):
    # Assumes the input file only contains LaTeX tabular rows (the interior of
    # the tabular environment), and that the format is [offset & byte1 & byte2 &
    # ... & ascii]

    result = []
    for i, line in enumerate(lines):
        line = line.split("&")
        processed_line = []
        for j, byte in enumerate(line[1:-1]):
            spec = None
            for coord in coordinates:
                if coord.get("i") and coord.get("i") == i:
                    if coord.get("j") == j or coord.get("j") == None:
                        spec = coord
                        break

            processed_line.append((" \\cellcolor{{{}}}".format(spec.get("c", args.default_color)) if spec else "") + byte)

        result.append("&".join([line[0], *processed_line, line[-1]]))
                
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
        "-d", "--default_color", default="blue!25",
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