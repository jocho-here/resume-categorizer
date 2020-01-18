from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import spacy

filename = 'test'
pdf_filename = f'{filename}.pdf'
img_filename = f'{filename}.jpg'
img = convert_from_path(pdf_filename)[0]
img.save(img_filename, 'JPEG')
ocr_result = pytesseract.image_to_string(Image.open(img_filename))
text = ocr_result.replace('\n', ' ')
nlp = spacy.load('en_core_web_sm')
doc = nlp(text)
result = [(w.text, w.pos_) for w in doc]
