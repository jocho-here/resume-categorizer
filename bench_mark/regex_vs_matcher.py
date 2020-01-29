import re
import spacy

from spacy.matcher import Matcher
from time import time


# Customize this to see how your input affects the speed
text = "1. 111-222-3333, 2. (444) 555-6666, 3. (777) 888 9999"

# Spacy setup
nlp = spacy.load('en_core_web_sm')
doc = nlp(text)
phone_matcher = Matcher(nlp.vocab)
phone_numbers = []
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


# Timing matcher
matcher_phone_numbers = []
start_time = time()
matches = phone_matcher(doc)
matcher_time = time() - start_time

for match_id, start, end in matches:
    span = doc[start:end]
    matcher_phone_numbers.append(span.text)

print("\nResult:\n")
print(f"\tMatcher:\n\t\ttime:{matcher_time}\n")


# Timing regex
regex_phone_numbers = []
phone_filter = '(\+\d{1,2}\s)?\(?\d{3}\)?(\s?[.-]?\s?)\d{3}(\s?[.-]?\s?)\d{4}'
start_time = time()
matches = re.finditer(phone_filter, text)
regex_time = time() - start_time

for match in matches:
    regex_phone_numbers.append(match.group(0))

print(f"\tRegular Expression:\n\t\ttime:{regex_time}\n")
print(f"Matcher is faster than regex? {matcher_time < regex_time}\n")

result_match = True

for matcher_phone_number in matcher_phone_numbers:
    if matcher_phone_number not in regex_phone_numbers:
        result_match = False
        break

if result_match:
    print("results match")
    print(f"\tresult: {matcher_phone_numbers}\n")
else:
    print("results don't match")
    print(f"\tmatcher result: {matcher_phone_numbers}")
    print(f"\tregex result: {regex_phone_numbers}\n")
