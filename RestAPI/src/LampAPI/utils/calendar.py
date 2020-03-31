import PyPDF3 as parser
import io

class Calendar:
    def _filter_out_whitespace(self, pdf_string):
        white_space = ["  ", "\n", "\t", "    ", "   "]
        for ws in white_space:
            pdf_string = pdf_string.replace(ws, '')
        return pdf_string

    def __init__(self, pdf_stream):
        pdf_data = io.BytesIO(pdf_stream)
        pdf_reader = parser.PdfFileReader(pdf_data)
        
        text = ""
        for page_no in range(pdf_reader.numPages-1):
            text += pdf_reader.getPage(page_no).extractText()

        self.pdf = self._filter_out_whitespace(text)
        


    
