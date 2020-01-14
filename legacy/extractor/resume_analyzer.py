import re
import xlsxwriter
import io, os, sys
import unicodedata
from google.cloud import language
from google.cloud import vision
from stanfordcorenlp import StanfordCoreNLP

resource_dir = 'resources/'
major_block_dir = resource_dir + 'major_blocks.txt'
majors_dir = resource_dir + 'majors.txt'

stanford_host = 'http://localhost'
stanford_port = 9001

# major_blocks.txt contains possible signature blocks that would go
# with majors e.g. bachelors of science ...
def get_major_blocks():
  with open(major_block_dir, 'r') as f:
    content = f.readlines()

  return [x.strip() for x in content]

# majors.txt contains all the available majors offered at UIUC
def get_majors():
  with open(majors_dir, 'r') as f:
    content = f.readlines()

  return [x.strip().lower() for x in content]

# Extract major from the given lines of string
def extract_major(pdf_text_lines):
  major_blocks = get_major_blocks()
  uiuc_majors = get_majors()

  # Go through pdf_text_lines and find any matching majors
  # with their surroudning lines
  found_majors = []
  found_major_lines = []
  for i, line in enumerate(pdf_text_lines):
    for major in uiuc_majors:
      if major.replace(' ', '').lower().strip() in \
          line.replace(' and ',' & ').replace(' ','').lower().strip():
        found_majors.append(major)
        valid_lines = []

        if not i == 0:
          valid_lines.append(pdf_text_lines[i - 1])
        valid_lines.append(line)

        if not i == len(pdf_text_lines) - 1:
          valid_lines.append(pdf_text_lines[i + 1])
        found_major_lines.append(valid_lines)
	
  # FOR DEBUGGING
  print("FOUND MAJORS")
  print(found_majors)

  # With surrounding lines, validate each found major
  # Remove duplicate majors as well
  valid_majors = []
  for i, found_major in enumerate(found_majors):
    valid = False
    print("found major lines for (" + found_major + ")")
    print(found_major_lines[i])
    for found_major_line in found_major_lines[i]:
      for major_block in major_blocks:
        if major_block.lower().replace(' ','') in found_major_line.lower().replace(' ',''):
          valid = True
          break
      if valid:
        break
    if valid and found_major not in valid_majors:
      valid_majors.append(found_major)
    else:
      print(found_major + " is not valid major")
	
  # FOR DEBUGGING
  print("VALID MAJORS")
  print(valid_majors)

  # Find inclusive majors (e.g. computer science and astronomy in computer science & astronomy)
  final_majors = []
  for m_1 in valid_majors:
    inclusive = False
    for m_2 in valid_majors:
      if m_1 != m_2 and m_1 in m_2:
        inclusive = True 
        break
    if not inclusive:
      final_majors.append(m_1)

  # FOR DEBUGGING
  print(final_majors)
  print('')
  #return ''
  return final_majors

# Extract name from the given lines of string
def extract_name(pdf_text_lines):
  global sf_client
  global g_nlp_client

  possible_names = []

  # Filter lines that have length less than 3
  pdf_text_lines = [x for x in pdf_text_lines if len(x) > 3]
  pdf_text = ', '.join(pdf_text_lines)

  # Stanford NLP
  sf_entities = sf_client.ner(pdf_text)

  for entity in sf_entities:
    if entity[1] == 'PERSON' and len(entity[0]) > 3:
      possible_names.append(entity[0])

  # FOR DEBUGGING
  print('STANFORD')
  print(possible_names)
  g_list = []

  document = language.types.Document(content=pdf_text, type=language.enums.Document.Type.PLAIN_TEXT)
  g_entities = g_nlp_client.analyze_entities(document=document).entities

  for entity in g_entities:
    if entity.type == 1 and len(entity.name) > 3:
      # PERSON
      # Take its placement into account
      g_list.append(entity.name) # FOR DEBUGGING
      possible_names.append(entity.name)

  # FOR DEBUGGING
  print('GOOGLE')
  print(g_list)

  name_line = ''
  name_line_i = len(pdf_text_lines)

  scores = {}

  for poss_name in possible_names:
    for i, line in enumerate(pdf_text_lines):
      if poss_name.replace(' ', '').replace('.', '').isalpha() and poss_name[0].istitle() and poss_name in line:
        if line in scores.keys():
          scores[line] += 1
        else:
          scores[line] = 1
      if poss_name[0].isalpha() and poss_name[0].istitle() \
          and poss_name in line and name_line_i > i:
        name_line_i = i
        name_line = line

  # FOR DEBUGGING
  print('Score Board')
  print(scores)

  true_name = ''

  try:
    highest_score = scores[list(scores.keys())[0]]
  except:
    return 'unknown'

  tie = True
  highest_scored_line = list(scores.keys())[0]

  for key in scores.keys():
    if scores[key] != highest_score:
      tie = False
    if scores[key] > highest_score:
      highest_score = scores[key]
      highest_scored_line = key

  if not tie:
    digit = False
    for c in highest_scored_line:
      if c.isdigit():
        true_name = name_line
        digit = True
        break
    if not digit:
      true_name = highest_scored_line
  else:
    true_name = name_line

  if len(true_name) > 60:
    true_name = ''
    for entity in possible_names:
      for block in entity.split(' '):
        if block.lower() not in true_name.lower():
          true_name += block + ' '

  return true_name.strip()[:60]

# Extract phone number from pdf_text
def extract_phone(pdf_text):
  phone_result = re.search('(\+\d{1,2}\s)?\(?\d{3}\)?(\s?[.-]?\s?)\d{3}(\s?[.-]?\s?)\d{4}', pdf_text)
  phone = ''

  if phone_result:
    phone = phone_result.group(0)
    
  return phone

# Extract email address from pdf_text
def extract_email(pdf_text):
  email_result = re.search('([a-zA-Z0-9\-%_\+]+(\.[a-zA-Z0-9\-%_\+]+)*)@([a-zA-Z0-9\-]+)\.([a-zA-Z0-9\-]{2,})', pdf_text)
  email = ''

  if email_result:
    email = email_result.group(0)

  return email

# Perform OCR on resume using Google Vision API
def ocr_google(file_name):
  global curr_dir
  global g_vision_client

  with io.open(curr_dir + '/png/' + file_name, 'rb') as f:
    content = f.read()

  image = vision.types.Image(content=content)
  response = g_vision_client.text_detection(image=image)
  texts = response.text_annotations

  if len(texts) > 5:
    ocred_text = unicodedata.normalize('NFKD', texts[0].description).encode('ascii','ignore')
  else:
    ocred_text = ''

  # save to txt file
  with open(curr_dir + '/txt/' + file_name + '.txt', 'w') as f:
    f.write(ocred_text)

  return ocred_text

def save_to_excel(result_list):
  global temp_name

  # Save them into an excel file
  workbook = xlsxwriter.Workbook(curr_dir + '/' + temp_name + '.xlsx')
  worksheet = workbook.add_worksheet()
  r = 0
  c = 0

  for row in result_list:
    for item in row:
      worksheet.write(r, c, item)
      c += 1
    r += 1
    c = 0
  
  workbook.close()
  print("Finished writing an excel file")

  with open(curr_dir + '/' + temp_name + '.csv', 'w') as csv_f:
    for row in result_list:
      csv_f.write(str(row).replace('\'', '')[1:-1] + '\n')
  print("Finished writing an CSV file")

def init_services():
  global g_vision_client
  global sf_client
  global g_nlp_client

  print("Initializing Google Vision client")
  g_vision_client = vision.ImageAnnotatorClient()

  print("Initializing Google Language client")
  g_nlp_client = language.LanguageServiceClient()

  print("Initializing StanfordCoreNLP client")
  sf_client = StanfordCoreNLP(stanford_host, stanford_port, memory='8g')

# Starting Point of the program
def start(tmp_name, pdf_id_dict, local_ip):
  global curr_dir
  global temp_name

  link = 'http://' + local_ip + ':9000/files/'
  #link = 'http://127.0.0.1:9000/files/'

  # Directory where resumes are located at
  temp_name = tmp_name
  curr_dir = resource_dir + temp_name

  # FOR DEBUGGING
  #testing = ['cs-resume/14.jpeg','cs-resume/5.jpeg']

  # Our CSV Format
  result_list = [['filename', 'name', 'major', 'phone', 'email', 'file_link']]

  # ENABLE THIS PART If you want to save them to -txt folder
  # Check for the existence of directory
  if not os.path.exists(curr_dir + '/txt'):
    os.makedirs(curr_dir + '/txt')
  print('Created directory ' + curr_dir + '/txt')

  init_services()

  for resume_png in os.listdir(curr_dir + '/png'):
    #if (curr_dir + '/' + resume) in testing: # FOR DEBUGGING
    if '.png' in resume_png:
      file_name = resume_png.encode("utf-8").split('.')[0]
      print("file_name: " + file_name)

      # FOR DEBUGGING
      # Open OCRed text file
      #extracted_text = open(curr_dir + '/txt/' + file_name + '.txt', 'r').read()

      # Process
      #   OCR --> name -> major -> phone -> email
      extracted_text = ocr_google(resume_png)

      if len(extracted_text) > 10:
        t = extracted_text.split('\n')

        if len(t) >= 8:
          student_name = extract_name(extracted_text.split('\n')[:8])
        else:
          student_name = extract_name(extracted_text.split('\n'))

        possible_majors = extract_major(extracted_text.split('\n'))
        phone = extract_phone(extracted_text.replace('\n', ','))
        email = extract_email(extracted_text.replace('\n', ','))
        file_link = link + pdf_id_dict[file_name]

        result = [file_name, student_name, '|'.join(possible_majors), phone, email, file_link]

        # Append the result
        result_list.append(result)
        print('Completed processing ' + file_name)
      else:
        print(file_name + " is not really a resume")

  save_to_excel(result_list)
