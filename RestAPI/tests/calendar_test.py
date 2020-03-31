import PyPDF3

pdf = open('outline_prob.pdf', 'rb')
pdf_reader = PyPDF3.PdfFileReader(pdf)

page2 = pdf_reader.getPage(2).extractText()
print(page2.replace("\n"," "))

