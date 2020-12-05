import os
rootdir = 'D:\_UWHomeworkSubmissions'



for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        try:
            str(os.path.join(subdir, file))[26:].index('\\')
        except:
            if str(os.path.join(subdir, file))[-3:] == "pdf":
                pdf = os.path.join(subdir, file)
                # pdf = pdf[26:pdf.index(' ')]

                newDir = rootdir[2:] + "\\1A\\"+pdf[26:pdf.index(' ')]+"\\"+pdf[26:]
                # print(rootdir[2:])
                # print(pdf[26:pdf.index(' ')])
                # print(pdf[26:])
                print(pdf)
                print(newDir)
                os.rename(pdf[2:],newDir)
                break
            # print(type(os.path.join(subdir, file)))
            # print(os.path.join(subdir, file))


# test = "test"
# try:
#     print(test.index('\\'))
# except:
#     print("not found")


# print(len("D:\_UWHomeworkSubmissions"))