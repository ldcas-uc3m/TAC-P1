#!/bin/bash
# Bash script to zip the whole project in order to make it deriverable
# please make sure zip and texlive are installed

OUTFILE="../MT_3_Arnaiz_Casais.zip"

[ -e $OUTFILE ] && rm $OUTFILE  # remove if exists already

# generate data
echo "Building turing-machine-simulator/..."
cd turing-machine-simulator
make --silent
cd ..

echo "Performing tests..."
source .venv/bin/activate
python3 src/test.py || exit

rm turing-machine-simulator/turing


# compile the report (and save it to root folder)
echo "Compiling the report..."
latexmk -cd -shell-escape -pdf report/report.tex 
cp report/report.pdf Memoria_MT_3_Arnaiz_Casais.pdf


# zip it (excluding useless stuff)
echo "Zipping..."
zip -q -r "$OUTFILE" . -x zip.sh report/\* \*.git\* img/\* *__pycache__/\* \*examples/\* .venv/\* *.xml *.tm *.jar build/\* .vscode/\* \*LICENSE

# cleanup
echo "Cleaning up..."
rm Memoria_MT_3_Arnaiz_Casais.pdf