import tika
from tika import parser

class Calendar:
    attempt_no = 0

    def __init__(self, pdf_stream):
        try:
            self.pdf = str(parser.from_buffer(pdf_stream)['content'])
        except RuntimeError:
            self.attempt_no += 1
            if self.attempt_no != 10:
                print("Attempt: {}\n".format(self.attempt_no))
                self.__init__(pdf_stream)
            else:
                print("Failed to connect to Tika server")

    
