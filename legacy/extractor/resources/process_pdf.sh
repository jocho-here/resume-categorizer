#!/bin/bash
name=$1

cd resources/$name
#cd $name

echo Separating PDF Stack into numbered PDF files
cd "pdf"

# Separate a resume stack into individual resumes
pdfseparate $name".pdf" $name"-"%d.pdf
echo Completed separating the PDF stack
rm $name".pdf"
echo Removed the PDF stack

mkdir ../png
echo Created PNG folder

# Convert resume format from PDFs to PNGs for Google OCR
for pdf_f in *; do
	if [[ "$pdf_f" = *".pdf" ]]; then
		convert -flatten -density 500 $pdf_f -quality 100 ../png/${pdf_f%.*}.png
		echo Converted $pdf_f to PNG
	fi
done

cd ../..
