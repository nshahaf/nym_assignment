
from dataclasses import dataclass
from typing import List, Dict
import pdfplumber
import os
from datetime import datetime,date
import re

@dataclass
class TextualWord:
    x0: float
    x1: float
    text: str

@dataclass
class Chart:
    name: str
    dob: date
    has_valid_ekg: bool

    @property
    def age(self):
        birth_date = datetime.strptime(self.dob, "%d/%m/%Y")
        today = datetime.today()
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                age -= 1
        return age
    
PagesToWords = Dict[int, List[TextualWord]]

def get_pdfs_from_directory(directory_path):
    # Get all PDF files in the directory
    pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]
    pdf_files_with_paths = [os.path.join(directory_path, f) for f in pdf_files]  # Get full paths of the PDFs
    return pdf_files_with_paths

def pdf_to_dict(pdfplumber_pdf: pdfplumber.PDF) -> PagesToWords:
    pages_to_words = {}

    # Iterate over all pages in the PDF
    for page_num, page in enumerate(pdfplumber_pdf.pages):
        words = page.extract_words()  # Extract words from the page
        textual_words = []
        
        # Convert each extracted word to a TextualWord namedtuple
        for word in words:
            # Extract coordinates (x0, x1) and text from each word
            x0 = word['x0']
            x1 = word['x1']
            text = word['text']
            
            # Create a TextualWord object and add to the list for the current page
            textual_words.append(TextualWord(x0=x0, x1=x1, text=text))
        
        # Add the list of textual words to the dictionary, with page number as key
        pages_to_words[page_num] = textual_words

    return pages_to_words

def extract_chart_from_pdf(pdf):
    text = pdf.pages[0].extract_text()
    name = re.search(r"Patient Name: (.*)\n", text).group(1)
    dob = re.search(r"DOB: (.*)\n", text).group(1)
    match = re.search(r"EKG Results (.*)\n", text)
    if match:
        ekg = match.group(1).strip()
        if(ekg == 'valid'):
            is_valid_ekg = True
        else:
            is_valid_ekg = False
    return Chart(name, dob, is_valid_ekg)