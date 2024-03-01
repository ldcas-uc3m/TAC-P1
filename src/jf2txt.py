# conversor de MT deterministas de JFLAP a https://turingmachinesimulator.com/
# uso: python jf2txt.py <MT.jff>
import xml.dom.minidom
import sys


# TODO: argparse


doc = xml.dom.minidom.parse(sys.argv[1])

states = {}
initial = []
final = []

out: str = ""

for st in doc.getElementsByTagName("state"):
    id = st.getAttribute("id")
    name = st.getAttribute("name")
    states[id] = name

    if st.getElementsByTagName("initial").length > 0:
        initial.append(name)
    if st.getElementsByTagName("final").length > 0:
        final.append(name)

machine_name = ".".join(sys.argv[1].split(".")[:-1])

out += f"name: {machine_name}\n"
out += f"init: {','.join(initial)}\n"
out += f"accept: {','.join(final)}\n"
out += "\n"


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
    rds = ",".join(str(v or "_") for k,v in sorted(read.items()))
    wrs = ",".join(str(v or "_") for k,v in sorted(write.items()))
    mvs = ",".join(mconv[v] for k,v in sorted(move.items()))

    out += f"{states[fr]},{rds}\n"
    out += f"{states[to]},{wrs},{mvs}\n"
    out += "\n"


# save

if len(sys.argv) > 2:
    file_name = sys.argv[2]
else:
    file_name = f"{machine_name}.txt"

with open(file_name, "+wt") as fd:
    fd.write(out.strip())

