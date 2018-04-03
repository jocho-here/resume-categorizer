Resume Categorizer
===================
Resume Categorizer extracts full name, e-mail address, phone number, and major from resumes and creates EXCEL file

Core Technology
--------------
1. Uses [Google Vision](https://cloud.google.com/vision/) engine for optical character recognition (OCR) on resumes to extract texts out of resumes
2. Uses [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) and [Google NLP](https://cloud.google.com/natural-language/) engine for finding name entity
3. Uses [Clowder](https://clowder.ncsa.illinois.edu/) for data management (uploading, downloading, linking)

Tested on...
------------
- Ubuntu

Installation
------------
1. Install Python 2.x (tested with 2.7)
2. Set up a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for the Python
3. Boot up the virtual environment, and run `pip install -r requirements.txt` on the root of this project
4. Download Stanford CoreNLP Library and rename it to `stanford-corenlp`, then move the folder to the root of this project
5. [Set up the authentication for GCP](https://cloud.google.com/docs/authentication/getting-started) in your environment
  - Tested initially by setting an environment varialbe `GOOGLE_APPLICATION_CREDENTIALS` with the application credentials JSON file
6. Download Clowder server and rename it to `clowder`, then move the folder to the root of this project
  - Tested with the latest stable version (1.3.4)
  - Move the custom folder into clowder/
  - Set up [RabbitMQ](https://www.rabbitmq.com/download.html)
    - Install RabbitMQ
      - `sudo apt-get install rabbitmq-server` for Ubuntu
    - Get the latest Erlang (Follow the zero dependency Erlang RPM package for RabbitMQ)
    - To start RabbitMQ Management UI, `sudo rabbitmq-plugins enable rabbitmq_management`
    - [To allow guest/guest login](https://www.rabbitmq.com/access-control.html)
      - `sudo rabbitmqctl stop_app`
      - `sudo rabbitmqctl force_reset`
      - `sudo rabbitmqctl start_app`
      - `sudo service rabbitmq-server stop`
      - `sudo service rabbitmq-server start`
  - Set up MongoDB
    - Follow the [website](https://docs.mongodb.com/manual/tutorial/) for installation
    - To let mongodb server to start automatically, `systemctl enable mongod.service`

Work Flow
------------
1. Run the Clowder
  - run `./clowder/bin/clowder`
2. Simultaneously, run the Stanford CoreNLP
  - run `./run_stanford_nlp.sh`
3. Simultaneously, run the resume extractor
  - in extractor folder, run `python resume_extractor.py`
4. Scan the front pages of all of resumes you want to categorize
5. Upload the stack to the Clowder
6. Sit back and wait for the engine to categorize all the resumes
7. Once the categorizing is over, you will see a link on the page of the uploaded resume stack

TODO
-----------
1. Optimizations on locating names
2. Multi-threading
3. Use Docker
4. Add more details on Clowder installation and set up since it's complicated (or even ease that complication?)
5. What was up with SMTP server problem? (Fixed with [this](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postfix-as-a-send-only-smtp-server-on-ubuntu-16-04))
