# New Plan!

## So far
1. Install poppler (for pdf2image)
2. Install python library pdf2image (https://github.com/Belval/pdf2image)
- Needed because pytesseract accepts images
3. Install tesseract (for pytesseract)
4. Install python library pillow (for pytesseract)
5. Install python library pytesseract

## General Plan
- Need to have solution ready to be used by user with few commands
- Dockerize!

## Things to think about
- Find a way to accept file from GUI
  - Replace RDBMS.  This is not a good solution.
- Which NLP to use?
  - StanfordNLP
    - Conservative, but industrial proven project
  - spaCy
    - New player!  Very hot project
- Used to use Google NLP to identify which text is what.  Hopefully there's a way to do this without Google :(
