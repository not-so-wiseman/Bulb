import PyPDF3 as parser
import io
import re
import nltk
import calendar

from datetime import date, datetime
from copy import deepcopy
from nltk.tokenize import sent_tokenize, word_tokenize


import PyPDF3 as parser
import io
import re
import nltk
import calendar

from datetime import datetime

from copy import deepcopy
from nltk.tokenize import sent_tokenize, word_tokenize


class CalendarDate:
    def _abrev_month(self, month):
        month_abrev = {
            "Jan": 1,"Feb": 2,"Mar": 3,"Apr": 4,"May": 5,"Jun": 6,
            "Jul": 7,"Aug": 8,"Sep": 9,"Oct": 10,"Nov": 11,"Dec": 12
        }
        return month_abrev.get(month, None)

    def _full_month(self, month):
        month_full_name = {
            "January": 1,"Febuary": 2,"March": 3,"April": 4,"May": 5,"June": 6,
            "July": 7,"August": 8,"September": 9,"October": 10,"November": 11,"December": 12
        }
        return month_full_name.get(month, None)

    def __init__(self, date_and_month):
        month, day = date_and_month.split(" ")
        if(len(month) == 3):
            self.month = self._abrev_month(month.capitalize())
        else:
            self.month = self._full_month(month.capitalize())
        self.day = int(day)
        self.year = datetime.now().year
        self.date = datetime(self.year, self.month, self.day)

    def __repr__(self):
        return "<CalendarDate {}/{}/{}>".format(self.day, self.month, self.year)


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

    def _package(self, matches):
        filtered_matches = []
        for match_set in matches:
            package = {"Event":None, "Date":None}
            for elem in match_set:
                if(re.search(self.assesments, elem) != None):
                    package["Event"] = deepcopy(elem)
                elif(re.search(self.month, elem) != None):
                    package["Date"] = deepcopy(CalendarDate(elem))
            if(package["Event"] != None and package["Date"] != None):
                filtered_matches.append(package)
        return filtered_matches
 
    def _post_process(self, matches):
        matches = self._compress(matches)
        matches = self._package(matches)
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
    def _month(self, num):
        month_lookup = {
            1:"January", 2:"Febuary", 3:"March", 4:"April", 5:"May",
            6:"June", 7:"July", 8:"August", 9:"September", 10:"October",
            11:"November", 12:"December"
        }
        return month_lookup.get(num, "")

    def _return_event_template(self, name, calendar_date):
        assert type(calendar_date) == CalendarDate
        return {
            "Name": name, 
            "Year": calendar_date.year,
            "Month": self._month(calendar_date.month) ,
            "Day": calendar_date.day
        }

    def __init__(self):
        self.dates = {
        "1": [],"2": [],"3": [],"4": [],"5": [],"6": [],
        "7":[],"8":[],"9":[],"10": [],"11": [],"12": []
        }
        
    def _parse_data_stream(self, pdf):
        scrub = DataScrubber()

        matches = []
        for sent in pdf.sentances:
            match = scrub.find_matches(sent.lower())
            if match != None:
                matches += match
        return matches

    def _add_events(self, data_stream):
        for item in data_stream:
            name = deepcopy(item["Event"])
            calendar_date = deepcopy(item["Date"])
            month = str(calendar_date.month)
            self.dates[month].append(self._return_event_template(
                name, calendar_date
            ))

    def add_events_by_stream(self, data_stream):
        pdf = PDF(pdf_stream=data_stream)
        data_stream = self._parse_data_stream(pdf)
        self._add_events(data_stream)

    def add_events_by_file(self, file_name):
        pdf = PDF(pdf_file_name=file_name)
        data_stream = self._parse_data_stream(pdf)
        self._add_events(data_stream)

    def __repr__(self):
        return '<Calendar Object>'

    def __str__(self):
        return self.dates

    def __add__(self, other_cal):
        def sort_by_date(event):
            return int(event['Day'])

        months = self.dates.keys()

        for m in months:
            events = self.dates[m] + other_cal.dates[m]
            if events != []:
                events.sort(key=sort_by_date)
            self.dates[m] = events

        return self