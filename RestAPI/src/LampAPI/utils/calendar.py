import PyPDF3 as parser
import io

class Calendar:
    def __init__(self, pdf_stream):
        self.pdf = ""
        pdf_data = io.BytesIO(pdf_stream)
        pdf_reader = parser.PdfFileReader(pdf_data)
        
        for page_no in range(pdf_reader.numPages-1):
            self.pdf += pdf_reader.getPage(page_no).extractText()
        
        

    
