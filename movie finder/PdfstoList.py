import pdfplumber
from PyPDF2 import PdfFileReader
import os

docs = "MovieScripts"

# List all files in the directory
files = os.listdir(docs)

# Open each PDF file
for file in files:
    if file.endswith('.pdf'):
        myPDFpath = os.path.join(docs, file)
        with pdfplumber.open(myPDFpath) as myPDF:
            # Continue processing the PDF file
            pagelist = []
            for page in range(len(myPDF.pages)):
                currentPage = myPDF.pages[page]
                myText = currentPage.extract_text()
                thispage = myText.split()
                pagelist.append(thispage)
        # Save the result to a text file
        output_filename = os.path.splitext(file)[0] + '.txt'
        with open(output_filename, 'w', encoding='utf-8') as f:
            for page_text in pagelist:
                for item in page_text:
                    f.write("%s\n" % item)
        #print("File", file, "has been processed.")