from PIL import Image
import textract
from pdf2image import convert_from_path
import os
import PyPDF2


rootdir = os.path.dirname(os.path.abspath(__file__))

# Removes the previous pdfs of individual questions
for f in os.listdir(os.path.join(rootdir,"Submit")):
    os.remove(os.path.join(rootdir,"Submit",f))


# Finds the file path in the submissions folder
for subdir, dirs,  files in os.walk(rootdir):
    for file in files:
        pdf = os.path.join(subdir,file)
        if pdf.rindex('\\') == len(rootdir) and pdf[-3:] == "pdf":
            name = pdf[pdf.rindex('\\')+1:]
            newDir = os.path.join(rootdir,"1A",name[:name.index(' ')],name)
            break
    break


# Opens the pdf to read
pdfFileObj = open(pdf,'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
num_pages = pdfReader.numPages
# Initializes variable for output
output = PyPDF2.PdfFileWriter()

question = 1

for i in range(num_pages):
    # Reads the text on the page
    page = pdfReader.getPage(i)
    text = page.extractText()
    # Creates a second variable with only the number of the question on the page
    text2 = ""
    for i in text:
        if ord(i) >= 48 and ord(i) <= 57:
            text2 += i
        elif i == '.':
            break
    # print("text2",text2)

    if len(text2) == 0: #If there is no number on the page, add to the current question
        output.addPage(page)
        continue
    if text2 != 1: #If it's not the first question, that means we just finished another question so we have to save that pdf and start a new one
        with open("./Submit/{} Question#{}.pdf".format(name,question),"wb") as out_f:
            output.write(out_f)
        question = int(text2)
        # print("question:",question)
        output = PyPDF2.PdfFileWriter()
    output.addPage(page) #Add page to the new pdf

# Saves pdf for last question
with open("./Submit/{} Question#{}.pdf".format(name,question),"wb") as out_f:
    output.write(out_f)

pdfFileObj.close()

# Moves the file to where it should be
os.rename(pdf,newDir)
