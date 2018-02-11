import textract # Module for parsing the pdf as a text document
import os

# parses current directory and converts all pdfs to txt files

def pdf2txt():
    current_directory = os.getcwd()
    pdf_directory = current_directory + '/downloads'
    directory_files = os.listdir(pdf_directory)
    for file in directory_files[1:]:
        if file.endswith(".pdf"):
            print file
            text = textract.process(pdf_directory + '/'+file)
            with open(pdf_directory + '/' + file[:-4] + ' (converted)' + '.txt', 'wb') as f2:
                f2.write(text)