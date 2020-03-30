import PyPDF2
from tika import parser


#pdf = io.BytesIO(request.content)
pdf = parser.from_file("outline_v1_0.pdf")
#pdf = str(pdf).encode('utf-8', errors='ignore')
print(pdf['content'])