
import re
from strip_ansi import strip_ansi

def parselines(lines, major_len=4, minor_len=4):
    latex = []
    fmt = "@{{}}c|*{{{}}}c|c@{{}}".format(major_len*minor_len)
    latex.append(r"\begin{{tabular}}{{{}}}".format(fmt))

    for line in lines:
        line = strip_ansi(line)

        theSplit = [spec.strip() for spec in re.split(' │', line, maxsplit=3)]
        # if len(theSplit) == 0:
            # continue

        theBytes = theSplit[1].split()
        theBytes +=  "" * ((major_len*minor_len) - len(theBytes))

        latex.append("  {} \\\\".format(" & ".join([theSplit[0], *theBytes, theSplit[2]])))

    latex.append(r"\end{tabular}")

    return latex
