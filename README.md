# New Plan!
## Reason of starting from the scratch
As you can see, there's a folder here called "legacy".  That contains logics and codes I wrote for this open source resume categorizer previously.  That version 1 was working fine and was correctly categorizing resumes, generating CSV for HR to look at.  However, as you would know by reading its README, it's super complicated despite that we already had technologies to make them very simple.
That was 2017 and back when I had very little knowledge with Python.  I also didn't know how Docker works so containerizing the whole process wasn't my option.  I could learn, but I probably was not capable of understanding what Docker was.
Now it's 2020 and I finally have plenty of experience with Python, as well as Docker.  I decided to maintain this repository and realized that just setting this whole thing up would take years, trouble shooting even longer.
So I decided to start from scratch.  My goal is to make this repo usable with few commands and to dockerize.

## So far
1. Install poppler (for pdf2image)
2. Install python library pdf2image (https://github.com/Belval/pdf2image)
- Needed because pytesseract accepts images
3. Install tesseract (for pytesseract)
4. Install python library pillow (for pytesseract)
5. Install python library pytesseract
6. Install python library spacy
7. Install `en_core_web_sm` from spacy

## General Idea
- Need to have solution ready to be used by user with few commands
- Dockerize!

## Process
1. PDF to JPEG
- poppler & pdf2image
2. OCR on JPEG
- pytesseract
- This takes quite time.  I could use async job for this work.
3. Analyse the resulting text and populate the CSV file with found elements

## Things to think about
- Find a way to accept file from GUI
  - Replace RDBMS.  This is not a good solution.
- Which NLP to use?
  - StanfordNLP
    - Conservative, but industrial proven project
  - spaCy
    - New player!  Very hot project
- Used to use Google NLP to identify which text is what.  Hopefully there's a way to do this without Google :(
