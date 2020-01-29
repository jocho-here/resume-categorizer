from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import spacy
from spacy.matcher import Matcher

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


# Phone number extraction
phone_matcher = Matcher(nlp.vocab)

# input could be a list of patterns [pattern1, pattern2, ...]
pattern1 = [
    {"SHAPE": "ddd"}, {"ORTH": "-"}, {"SHAPE": "ddd"}, {"ORTH": "-"}, {"SHAPE": "dddd"}
]
pattern2 = [
    {"ORTH": "("}, {"SHAPE": "ddd"}, {"ORTH": ")"}, {"SHAPE": "ddd"}, {"ORTH": "-"},
    {"SHAPE": "dddd"}
]
pattern3 = [
    {"ORTH": "("}, {"SHAPE": "ddd"}, {"ORTH": ")"}, {"SHAPE": "ddd"}, {"SHAPE": "dddd"}
]
patterns = [
    pattern1, pattern2, pattern3
]

phone_matcher.add("PHONE_NUMBER", patterns)
matches = phone_matcher(doc)

phone_numbers = []
for match_id, start, end in matches:
    span = doc[start:end]
    phone_numbers.append(span.text)

print(phone_numbers)
