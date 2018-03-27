Resume Categorizer
===================
Resume Categorizer extracts full name, e-mail address, phone number, and
 major from resumes and creates CSV file.

Pre-requisites
--------------

I would suggest using [virtual environment](https://virtualenv.pypa.io/en/stable/) if you are experiencing some 
problems while installing python packages  
- [Python 3.6.2](https://www.python.org/downloads/)  
- [Google NLP Python Library](https://cloud.google.com/python/apis)  
- [Google Vision Python Library](https://cloud.google.com/python/apis)  
- [Stanford CoreNLP Library](https://stanfordnlp.github.io/CoreNLP/download.html)  

Installation
------------
1. If you don't have latest Python 3, please download it from link above
2. For both Google Python libraries, you can get them through `pip install` (Please take a look at links above)
  - [Set up the authentication for GCP](https://cloud.google.com/docs/authentication/getting-started) in your environment
3. Download Stanford CoreNLP Library on this project directory as stanford-corenlp, witout version number
	- The file was more than 360MB so I did not want to put this on my repository

Process
------------
1. Seperate any stacked PDFs
	- For Mac or Ubuntu users, you can use [pdfseparate](https://superuser.com/questions/827462/how-can-i-split-a-pdf-file-into-single-pages-quickly-i-e-from-the-terminal-com) on Terminal
2. Save PDF files into each categorized folder in the resources folder (e.g. 'cs-resume' for computer science)
3. Run `./pdf_to_jpeg` from resources folder
4. Run `./run_stanford_nlp` from the home directory (Must have Stanford CoreNLP Library downloaded first)
(5-1. Run virtual environment before running python program if you have one)
5. Run `python resume-reader.py`

Example Result
-----------
filename, name, major, phone number, e-mail address  
cs-resume-1, Yayi Ning, computer science|statistics|management, (217) 904-2192, yning4@illinois.edu  
cs-resume-10, Haotian Jiang, computer science, (217)898-1307, hjiang13@illinois.edu  
cs-resume-11, Aafreen Lilly, computer science, 217-418-4080, aafreenlilly@gmail.com  
cs-resume-12, SAHIL GUPTA ntcrnhip, computer science, 217-979-2322, sjgupta2@illinois.edu  
cs-resume-13, ANIRUDH MANOJ, mathematics & computer science|statistics, (217) 722 7138, amanoi2@illinois.edu  
cs-resume-14, Archit Gupta, computer science|astronomy, (217)-402-4441, architgupta941@gmail.com  
cs-resume-15, Yanqing Ma (Marrie), computer science, , yma34@illinois.edu  
cs-resume-16, Yong Jin (YJ) Kim, computer science, (217) 377-3534, ykim164@illinois.edu  
cs-resume-17, Drew Zelac, computer science, (610) 500 4268,  
cs-resume-18, Chaeyun (Sarah) Jung, computer science|statistics, 217-714-7356, chaeyun2@illinois.edu  
cs-resume-19, Xiange (Shirley) Wang, mathematics & computer science, 217-904-5796, xwang287@illinois.edu  
cs-resume-2, Chase Engelbrecht, computer science, 815-656-0564, chasere2@illinois.edu  
cs-resume-20, SANSKRUTI MORE, mathematics & computer science, (217) 904-6139, SBMORE2@ILLINOIS.EDU  
cs-resume-3, Austin Ronghong Sun, computer science & astronomy, 408.796.9359, arsun2@illinois.edu  
cs-resume-4, RISHABH RAJAGOPALAN, computer science, (217) 649 3930, rishabh2@illinois.edu  
cs-resume-5, Ayush Ranjan, computer science|mathematics, +1 (217-305-1108, ID-avushi.2@illinois.edu  
cs-resume-6, Arkin Dharawat, mathematics, 650.995.2455, arkinrd2@illinois.edu  
cs-resume-7, Tanva Verma, computer science, 510-304-3150, tanyav2@illinois.edu  
cs-resume-8, MITCHELL B. WELLS, computer science, 636-322-8555, mitchell.b.wells@gmail.com  
cs-resume-9, SOPHIA YANG, undeclared|computer science, (630)-570-1868, sophiay2@illinois.edu  

TODO
-----------
1. Optimizations
2. Multi-threading
3. Time each entity extraction and optimize
