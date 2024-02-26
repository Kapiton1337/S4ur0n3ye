from odf import text, teletype #pip install odfpy
from odf.opendocument import load

def parse_odt(file_path, keyword=None):
    doc = load(file_path)
    text_content = []

    for para in doc.getElementsByType(text.P):
        text_content.append(teletype.extractText(para))

    if keyword:
        text_content = [line for line in text_content if keyword in line]

    return '\n'.join(text_content)

#example
file_path = 'example.odt'
keyword = 'example'
parsed_text = parse_odt(file_path, keyword)
print(parsed_text)