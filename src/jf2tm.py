# conversor de MT deterministas de JFLAP a https://turingmachinesimulator.com/
# uso: python jf2tm.py <MT.jff>

# Autor: Diego Devesa
# CLI por Luis Daniel Casais Mezquida <https://github.com/ldcas-uc3m/>


import xml.dom.minidom
import pathlib
import argparse
import sys
import io



class JFLAPException(Exception):
    """
    Class representing a JFLAP JFF syntax error, or similar.
    """
    pass



def convert(file_path: str | io.TextIOWrapper | pathlib.Path, machine_name: str) -> str:
    """
    Converts a JFLAP Turing Machine file into the turingmachinesimulator format.

    :param file_path: Path of JFF file.
    :param name: Machine name.

    :return: Turing Machine in turingmachinesimulator format.

    :raises FileNotFoundError: File doesn't exist.
    :raises JFLAPException: Invalid JFF file.

    @author: Diego Devesa
    """

    if isinstance(file_path, pathlib.Path):
        doc = xml.dom.minidom.parse(str(file_path.absolute()))
    else:
        doc = xml.dom.minidom.parse(file_path)

    # check type
    if doc.getElementsByTagName("type")[0].firstChild.nodeValue != "turing":
        raise JFLAPException("Not a Turing Machine")

    states = {}
    initial = []
    final = []

    out: str = ""

    # states
    for st in doc.getElementsByTagName("state"):
        id = st.getAttribute("id")
        name = st.getAttribute("name")
        states[id] = name

        if st.getElementsByTagName("initial").length > 0:
            initial.append(name)
        if st.getElementsByTagName("final").length > 0:
            final.append(name)

    out += f"name: {machine_name}\n"
    out += f"init: {','.join(initial)}\n"
    out += f"accept: {','.join(final)}\n"
    out += "\n\n"


    # transitions
    for tr in doc.getElementsByTagName("transition"):
        # <from>5</from>
        # <to>5</to>
        fr = tr.getElementsByTagName("from")[0].firstChild.nodeValue
        to = tr.getElementsByTagName("to")[0].firstChild.nodeValue

        read = {}
        write = {}
        move = {}

        # <read tape="1">1</read>
        for e in tr.getElementsByTagName("read"):
            tape = e.getAttribute("tape") or 0
            val = e.firstChild and e.firstChild.nodeValue
            read[int(tape)] = val

        # <write tape="1">1</write>
        for e in tr.getElementsByTagName("write"):
            tape = e.getAttribute("tape") or 0
            val = e.firstChild and e.firstChild.nodeValue
            write[int(tape)] = val

        # <move tape="1">R</move>
        for e in tr.getElementsByTagName("move"):
            tape = e.getAttribute("tape") or 0
            val = e.firstChild and e.firstChild.nodeValue
            move[int(tape)] = val

        mconv = {
            "L": "<",
            "R": ">",
            "S": "-"
        }
        rds = ",".join(str(v or "_") for _, v in sorted(read.items()))
        wrs = ",".join(str(v or "_") for _, v in sorted(write.items()))
        mvs = ",".join(mconv[v] for _, v in sorted(move.items()))

        out += f"{states[fr]},{rds}\n"
        out += f"{states[to]},{wrs},{mvs}\n"
        out += "\n"

    return out.strip()



##########
# PARSER #
##########
parser = argparse.ArgumentParser(
    description="Converts a JFLAP Turing Machine file into the https://turingmachinesimulator.com format.",
)

parser.add_argument(
    "file",
    help="Input file (JFALP Turing Machine JFF file).",
    type=argparse.FileType('r'),
)

parser.add_argument(
    "-o", "--output",
    help="Output to specified file. If no file is specified, it will be saved as <file_name>.txt.",
    nargs="?",
    default=sys.stdout,
    metavar="OUTPUT_FILE",
    type=argparse.FileType('w'),
    required=False
)



if __name__ == "__main__":
    args = parser.parse_args()

    input_file = pathlib.Path(args.file.name)

    machine_name = ".".join(input_file.name.split(".")[:-1])

    try:
        output = convert(args.file, machine_name)
    except JFLAPException as e:
        parser.exit(f"Invalid JFF file: {e}")

    # save
    if args.output:
        args.output.write(output)
    else:
        with open(pathlib.Path(f"{input_file.parent}/{machine_name}.txt"), "+wt") as fd:
            fd.write(output)