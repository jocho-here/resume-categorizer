# Example from geeksforgeeks
# https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
from PIL import Image 
import pytesseract 
from pdf2image import convert_from_path 

# Path of the pdf 
PDF_file = "test.pdf"
  
# Store all the pages of the PDF in a variable 
pages = convert_from_path(PDF_file) 

# Counter to store images of each page of PDF to image 
image_counter = 1

# Iterate through all the pages stored above 
for page in pages: 
    filename = "page_"+str(image_counter)+".jpg"
    page.save(filename, 'JPEG') 
    image_counter = image_counter + 1

filelimit = image_counter-1
outfile = "out_text.txt"

with open(outfile, "a") as f:
    for i in range(1, filelimit + 1): 
        filename = "page_"+str(i)+".jpg"
        text = str(((pytesseract.image_to_string(Image.open(filename))))) 
        text = text.replace('-\n', '')     
        f.write(text) 
