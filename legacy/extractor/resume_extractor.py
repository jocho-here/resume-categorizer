"""Example extractor based on the clowder code."""

import logging
import subprocess
import socket
import os

import pyclowder.files
from pyclowder.extractors import Extractor

import resume_analyzer as analyzer

class WordCount(Extractor):
  """Count the number of characters, words and lines in a text file."""
  def __init__(self):
    Extractor.__init__(self)

    # add any additional arguments to parser
    # self.parser.add_argument('--max', '-m', type=int, nargs='?', default=-1,
    #                          help='maximum number (default=-1)')

    # parse command line and load default logging configuration
    self.setup()

    # setup logging for the exctractor
    logging.getLogger('pyclowder').setLevel(logging.DEBUG)
    logging.getLogger('__main__').setLevel(logging.DEBUG)

  # returns local ip
  def get_ip(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      s.connect(('10.255.255.255', 1))
      local_ip = s.getsockname()[0]
    except:
      local_ip = '127.0.0.1'
    finally:
      s.close()
    
    return local_ip 

  def process_message(self, connector, host, secret_key, resource, parameters):
    # Process the file and upload the results
    logger = logging.getLogger(__name__)
    inputfile = resource["local_paths"][0]
    file_id = resource['id']

    # Check out current resource info
    for i in resource:
      print(i + ':', resource[i])
    
    # Get the temporary hashed name of uploaded PDF stack
    name = inputfile.split('/')[2].split('.')[0]
    print('name: ', name)

    # Side note: I'm running subprocesses with stdout = 0 to print out logs to STDOUT.
    #            subprocess.STDOUT gave me -2, which is not STDOUT of linux

    # 0. Make new directory for new task
    subprocess.call(['mkdir', 'resources/' + name], stdout=0, stderr=0)
    print("Created resources/" + name)

    # 1. Make new directory for new resume stack
    subprocess.call(['mkdir', 'resources/' + name + '/pdf'], stdout=0, stderr=0)
    print("Created resources/" + name + '/pdf')
    
    # 2. Copy the uploaded PDF over
    subprocess.call(['cp', inputfile, 'resources/' + name + '/pdf/' + name + '.pdf'], \
                                                                      stdout=0, stderr=0)
    print("Copied " + inputfile + " over to " + 'resources/' + name + "/pdf/" + name + ".pdf")

    # 3. Separate the stacked PDF and convert them to JPEGs
    subprocess.call(['./resources/process_pdf.sh', name], stdout=0, stderr=0)
    print("Separated PDFs")
    print("Converted to JPEGs")

    # Upload JPEGs
    pdf_id_dict = {}
    for pdf_file in os.listdir('resources/' + name + '/png/'):
      file_dir = 'resources/' + name + '/png/' + pdf_file
      f_id = pyclowder.files.upload_to_dataset(connector, host, secret_key, resource['parent']['id'], file_dir)
      f_id = f_id.encode("utf-8")
      print("f_id: ", f_id)
      print("type(f_id): ", type(f_id))
      pdf_id_dict[pdf_file.replace('.png', '')] = f_id

    # 4. Run analyzer
    myip = self.get_ip()
    analyzer.start(name, pdf_id_dict, myip)
    print("Finished analyzing the resumes")

    # Upload result excel file
    new_f_id = pyclowder.files.upload_to_dataset(connector, host, secret_key, resource['parent']['id'], 'resources/' + name + '/' + name + '.xlsx')

    # Attach excel link
    result = ['http://' + myip + ':9000/files/' + str(new_f_id)]
    metadata = self.get_metadata(result, 'file', file_id, host)
    f_id = pyclowder.files.upload_metadata(connector, host, secret_key, file_id, metadata)

    # Upload metadata of the excel file
    with open('resources/' + name + '/' + name + '.csv', 'r') as f:
      result = f.readlines()
    metadata = self.get_metadata(result, 'file', new_f_id, host)
    f_id = pyclowder.files.upload_metadata(connector, host, secret_key, new_f_id, metadata)

if __name__ == "__main__":
  extractor = WordCount()
  extractor.start()
