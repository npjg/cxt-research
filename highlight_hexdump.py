#!/usr/bin/python

import sys
import argparse
import ast

def parselines(lines):
    # Assumes the input file only contains LaTeX tabular rows (the interior of the tabular environment), and that the format is [offset & byte1 & byte2 & ... & ascii]
    result = []
    for i, line in enumerate(lines):
        line = line.split("&")
        processed_line = []
        for j, byte in enumerate(line[1:-1]):
            spec = None
            for coord in args.coordinates:
                if (i, j) == coord[0]:
                    spec = coord
                    break

            processed_line.append((" \\cellcolor{{{}}}".format(spec[1] if len(spec) > 1 else args.default_color) if spec else "") + byte)

        result.append("&".join([line[0], *processed_line, line[-1]]))
                
    return ''.join(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="highlight_hexdump", formatter_class=argparse.RawTextHelpFormatter,
        description="Add highlighting to selected cells in dumps generated by the included hexdump.cfg"
    )

    parser.add_argument(
        "-i", "--input", default=None,
        help="The input TeX file, containing only the rows of a tabular."
    )

    parser.add_argument(
        "-c", "--coordinates", default="[]",
        help="A list of the cell coordinates of the input to highlight, in the format [(row, col), <color>]."
    )

    parser.add_argument(
        "-d", "--default_color", default="blue!25",
        help="The default color to use for coloring selected cell coordinates when a color is not provided in the coordinate."
    )

    parser.add_argument(
        "-H", "--highlight-ascii", default=False, action="store_true",
        help="In addition to highlighting the byte display, also hightlight the ASCII display."
    )

    lines = []

    args = parser.parse_args()
    args.coordinates = ast.literal_eval(args.coordinates)
    # print("Coordinates: {}\n".format(args.coordinates)) 
    if args.input:
        with open(args.input, 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    result = parselines(lines)
    print(result)