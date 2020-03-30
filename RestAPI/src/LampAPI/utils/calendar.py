from tika import parser

class Calendar:
    def __init__(self, pdf_stream):
        self.pdf = str(parser.from_buffer(pdf_stream)['content'])

    
