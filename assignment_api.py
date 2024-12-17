
from utils import get_pdfs_from_directory, pdf_to_dict, extract_chart_from_pdf
import pdfplumber


if __name__ == "__main__":
    # pdf files in a directory.
    pdf_files = get_pdfs_from_directory("./pdfs")
    charts = []
    
    # For each PDF [chart1.pdf, chart2.pdf, chart3.pdf]
    for pdf_file in pdf_files: 
        pdf = pdfplumber.open(pdf_file)    
        textual_dict = pdf_to_dict(pdf)
        # print(textual_dict)  
        chart = extract_chart_from_pdf(pdf)
        print (f'Patient Name: {chart.name}, DOB: {chart.dob}, Age: {chart.age}, Valid EKG: {chart.has_valid_ekg}')
        charts.append(chart)
        
