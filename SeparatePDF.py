from __future__ import print_function
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

import time
import os
import io

import textract
from pdf2image import convert_from_path
import PyPDF2
from PIL import Image

import subprocess

print("Separate PDF running")

term = "1B"
timeLimit = 30 #In minutes

def twodigits(n):
    if n>=10:
        return n
    else:
        return "0"+str(n)

SCOPES = ['https://www.googleapis.com/auth/drive']
now = time.gmtime(time.time()-timeLimit*60)
rfc = "{}-{}-{}T{}:{}:{}+00:00".format(twodigits(now[0]),twodigits(now[1]),twodigits(now[2]),twodigits(now[3]),twodigits(now[4]),twodigits(now[5]))

rootdir = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists("Manual Download"):
    os.mkdir(os.path.join(rootdir,"Manual Download"))
    print("Manual Download directory created")
manual = len(os.listdir(os.path.join(rootdir,"Manual Download"))) != 0

if not manual:
    # All copied from google
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        print("Identified token")


    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print("Refreshing credentials")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)


    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(q = "modifiedTime > '{}' and mimeType = 'application/pdf'".format(rfc),
        pageSize=1, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found')
        exit()

    name = items[0]['name'][:-4]

else:
    name = os.listdir(os.path.join(rootdir,"Manual Download"))[0][:-4]
    print("Manual Download Detected")

course = name[:name.index(' ')]
pdf = os.path.join(rootdir,term,course,name)

print(name+".pdf")
    
# Makes directory if it doesn't exist
if(not os.path.exists(term)):
    os.mkdir(os.path.join(rootdir,term))
    print(term, "directory created")
if(not os.path.exists("{}/{}".format(term,course))):
    os.mkdir(os.path.join(rootdir,term,course))
    print(course, "directory created")
if(not os.path.exists("Submit")):
    os.mkdir(os.path.join(rootdir,"Submit"))
    print("Submit directory created")


# Downloads the pdf
if not manual:
    file_id = items[0]['id']
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO("./{}/{}/{}.pdf".format(term,course,name),'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
else:
    # Moves file if downloaded manually
    if os.path.exists("{}/{}/{}.pdf".format(term,course,name)):
        os.remove(os.path.join(rootdir,term,course,name+".pdf"))
        os.rename(os.path.join(rootdir,"Manual Download",name+".pdf"),os.path.join(rootdir,term,course,name+".pdf"))
        print("File replaced")
    else:
        print("File moved")
        os.rename(os.path.join(rootdir,"Manual Download",name+".pdf"),os.path.join(rootdir,term,course,name+".pdf"))

# Removes the previous pdfs of individual questions
for f in os.listdir(os.path.join(rootdir,"Submit")):
    os.remove(os.path.join(rootdir,"Submit",f))



# Finds the file path in the submissions folder
# Replaced because since I am downloading the file to a specific path, I already have the path
# Kept in case I want to revert later
# for subdir, dirs,  files in os.walk(rootdir):
#     for file in files:
#         pdf = os.path.join(subdir,file)
#         if pdf.rindex('\\') == len(rootdir) and pdf[-3:] == "pdf":
#             name = pdf[pdf.rindex('\\')+1:]
#             newDir = os.path.join(rootdir,"1A",course,name)
#             break
#     break


# Opens the pdf to read
pdfFileObj = open(pdf+".pdf",'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
num_pages = pdfReader.numPages
# Initializes variable for output
output = PyPDF2.PdfFileWriter()

newPage = True
question = -1

for i in range(num_pages):
    # Reads the text on the page
    page = pdfReader.getPage(i)
    text = page.extractText()
    # Creates a second variable with only the number of the question on the page
    text2 = ""
    for j in text:
        if ord(j) >= 48 and ord(j) <= 57:
            text2 += j
        elif j == '.':
            break
        elif len(text2) != 0:
            text2 = ""
            break
    else:
        text2 = ""
    if len(text2) != 0: #New question
        if i != 0 and question == -1: #There are pages that aren't questions yet, the forewords
            with open("./Submit/{} Foreword.pdf".format(name),"wb") as out_f:
                output.write(out_f)
            output = PyPDF2.PdfFileWriter()
        elif i != 0: #If it's not the first question, that means we just finished another question so we have to save that pdf and start a new one
            with open("./Submit/{} Question#{}.pdf".format(name,question),"wb") as out_f:
                output.write(out_f)
            output = PyPDF2.PdfFileWriter()
        question = int(text2)

    output.addPage(page) #Add page to the pdf

# Saves pdf for last question
with open("./Submit/{} Question#{}.pdf".format(name,question),"wb") as out_f:
    output.write(out_f)

pdfFileObj.close()
print("PDFs ready for submission")

subprocess.Popen('explorer "D:\_UWHomeworkSubmissions\Submit"')