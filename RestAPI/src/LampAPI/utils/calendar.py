import PyPDF3 as parser
import io
import re
import nltk
import calendar

from datetime import datetime
from copy import deepcopy
from nltk.tokenize import sent_tokenize, word_tokenize

class PDF:
    def _extract_text(self, pdf_data):
        pdf_reader = parser.PdfFileReader(pdf_data)
        text = ""
        for page_no in range(pdf_reader.numPages-1):
            text += pdf_reader.getPage(page_no).extractText()
        return text
    
    def _filter_out_whitespace(self, pdf_string):
        pdf_string = pdf_string.replace("\n", '')

        white_space = ["\t", "    ", "   ", "  "]
        for ws in white_space:
            pdf_string = pdf_string.replace(ws, ' ')

        return pdf_string
    
    def __init__(self, pdf_stream=None, pdf_file_name=None):
        if(pdf_stream != None):
            pdf_data = io.BytesIO(pdf_stream)

        elif(pdf_file_name != None):
            assert type(pdf_file_name) == str
            pdf_data = open(pdf_file_name, 'rb')
        
        else:
            raise Exception()

        pdf_text = self._extract_text(pdf_data)

        self.text = self._filter_out_whitespace(pdf_text)
        self.sentances = nltk.sent_tokenize(self.text)


class DataScrubber:
    pattern_stubs = {
        "month abrev":r"(jan|feb|mar|apr|may|jun|jul|aug|sept|oct|nov|dec)",
        "month full":r"(january|february|march|april|may|june|july|august|september|october|november|december)"
    }
    month = r"({0}|{1})".format(
        pattern_stubs["month abrev"], 
        pattern_stubs["month full"]
    )
    assesments = r"(assignment|project|quiz|mid.term|final|lab|test)( \d)?"

    def _compress(self, matches):
        compressed_syllabus = []
        for group in matches:
            tmp = []
            index = ""
            for match in range(len(group)-1):
                if index.find(group[match]) == -1:
                    tmp.append(deepcopy(group[match]))
                    index = group[match]
            compressed_syllabus.append(deepcopy(tmp))
        return compressed_syllabus

    def _remove_noise(self, matches):
        for match_set in matches:
            for elem in match_set:
                if(not re.search(self.assesments, elem) and 
                    not re.search(self.month, elem)):
                    match_set.remove(elem)
        return matches
                
    def _post_process(self, matches):
        matches = self._compress(matches)
        matches = self._remove_noise(matches)
        return matches

    def find_matches(self, pdf_text):
        regx_pattern = r"""({0})( \S+)? ({1} \d)""".format(
            self.assesments, self.month)

        search_results = re.findall(regx_pattern, pdf_text.lower())
        if search_results != []:
            return self._post_process(search_results)
        else:
            return None


class Calendar:
    def __init__(self):
        self.calendar = {}
        dates = calendar.itermonthdates(2020, 5)
         

    def add_events(self, sllyabus):
        pass





    
