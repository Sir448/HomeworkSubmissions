from PIL import Image
import textract
# import sys
from pdf2image import convert_from_path
import os
import PyPDF2


rootdir = 'D:\_UWHomeworkSubmissions'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        try:
            os.path.join(subdir, file)[26:].index('\\')
        except:
            if os.path.join(subdir, file)[-3:] == "pdf":
                pdf = os.path.join(subdir, file)
                # print(str(os.path.join(subdir, file))[26:-4])
                break


# pdf = "./1A/Test{}.pdf".format(input("PDF number?"))
# pdf = os.path.join(subdir, file)

# # pages = convert_from_path(pdf,dpi=500,poppler_path=r'C:\Program Files\poppler-0.68.0_x86\poppler-0.68.0\bin')

# # image_counter = 1

# # for page in pages:
# #     page.save("./Submit/page_{}.jpg".format(image_counter),'JPEG')
# #     image_counter+=1

# # filelimit = image_counter
upperLeft = 100
lowerRight = 150

# # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # for i in range(1,filelimit):
# #     img = Image.open("./Submit/page_{}.jpg".format(i))
# #     img = img.crop((400,400,x,x))
# #     img.save("./Submit/page_{}.jpg".format(i))
# #     text = str(((pytesseract.image_to_string(Image.open("./Submit/page_{}.jpg".format(i)),config='--psm 4'))))
# #     print(text)

pdfFileObj = open(pdf,'rb')
question = 1
startingPage = 0
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
num_pages = pdfReader.numPages
output = PyPDF2.PdfFileWriter()
for i in range(num_pages):
    page = pdfReader.getPage(i)
    text = page.extractText()
    text2 = ""
    for i in text:
        if ord(i) >= 48 and ord(i) <= 57:
            text2 += i
        elif i == '.':
            break
    # print("text2",text2)
    if len(text2) == 0:
        output.addPage(page)
        # print("test")
        continue
    if text2 != 1:
        with open("./Submit/{} Question#{}.pdf".format(pdf[26:-4],question),"wb") as out_f:
            output.write(out_f)
        question = int(text2)
        # print("question:",question)
        output = PyPDF2.PdfFileWriter()
    output.addPage(page)

with open("./Submit/{} Question#{}.pdf".format(pdf[26:-4],question),"wb") as out_f:
    output.write(out_f)






# while True:
#     output = PyPDF2.PdfFileWriter()
#     for i in range(startingPage,num_pages):
#         page = pdfReader.getPage(i)
#         text = page.extractText()
#         for i in text:
#             if ord(i) < 48 or ord(i) > 57:
#                 text = text[1:]
#             else:
#                 break
#         for i in range(len(text)):
#             if text[i] == '.':
#                 text[:i]
#                 break
#         if len(text) == 0:
#             output.addPage(page)
#             continue
#         startingPage = i
#         break
#     else:
#         with open("./Submit/test #{}.pdf".format(question),"wb") as out_f:
#             output.write(out_f)
#         break
#     with open("./Submit/test #{}.pdf".format(question),"wb") as out_f:
#         output.write(out_f)
#     question+=1



    
        
        # page.mediaBox.lowerRight = (lowerRight,page.cropBox.getUpperRight()[1] - lowerRight)
    # with open("./Submit/test.pdf","wb") as out_f:
    #     output.write(out_f)

# pages = convert_from_path("./Submit/test.pdf",dpi=500,poppler_path=r'C:\Program Files\poppler-0.68.0_x86\poppler-0.68.0\bin')
# pages[0].save("./Submit/test.jpg")

# img = Image.open(r'./Submit/test.jpg')
# img = img.convert('RGB')
# img.save(r'./Submit/test.pdf')

# pdfFile = PyPDF2.PdfFileReader(open("./Submit/test.pdf",'rb'))
# page = pdfFile.getPage(0)
# # img = Image.open("./Submit/test.pdf")
# text = page.extractText()
# for i in text:
#     if i == '!' or i == ' ':
#         text = text[1:]
# print(text)




        # if text == "" or int(text) == question:
        #     Question.addPage()