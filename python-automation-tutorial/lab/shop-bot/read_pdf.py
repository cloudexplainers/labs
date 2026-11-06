import sys

from pypdf import PdfReader

reader = PdfReader(sys.argv[1])
print(reader.pages[0].extract_text())
