#!/bin/bash
# Bash script to zip the whole project in order to make it deriverable
# please make sure zip, pv and texlive are installed

OUTFILE="../EPF-1-Arnaiz-Casais.zip"


# compile the report (and save it to root folder)
echo "Compiling the report..."

latexmk -cd -shell-escape -pdf report/report.tex 

cp report/report.pdf .


# zip it (excluding useless stuff)
echo "Zipping..."
zip -r "$OUTFILE" . -x zip.sh report/\* \*.git\* img/\* venv/\* *.xml *.jar build/\* .vscode/\* LICENSE

# cleanup
echo "Cleaning up..."
rm report.pdf