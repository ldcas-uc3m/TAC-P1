#!/bin/bash
# Bash script to zip the whole project in order to make it deriverable
# please make sure zip, pv and texlive are installed

OUTFILE="../MT02_3_Arnaiz_Casais.zip"


# generate data
echo "Building turing-machine-simulator/..."
cd turing-machine-simulator
make --silent
cd ..

echo "Performing tests..."
python3 src/test.py



# compile the report (and save it to root folder)
echo "Compiling the report..."
latexmk -cd -shell-escape -pdf report/report.tex 
cp report/report.pdf Memoria_MT_3_Arnaiz_Casais.pdf


# zip it (excluding useless stuff)
echo "Zipping..."
zip -r "$OUTFILE" . -x zip.sh report/\* \*.git\* img/\* *__pycache__/\* turing-machine-simulator/\* .venv/\* *.xml *.tm *.jar build/\* .vscode/\* LICENSE

# cleanup
echo "Cleaning up..."
rm Memoria_MT_3_Arnaiz_Casais.pdf