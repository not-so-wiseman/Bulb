import tika
from tika import parser
pdf = parser.from_file('outline_v1_0.pdf')

print(pdf["content"])
