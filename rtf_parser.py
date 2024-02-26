#pip install pyth
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter

def parse_rtf(file_path):
    doc = Rtf15Reader.read(open(file_path, 'rb'))

    text_content = PlaintextWriter.write(doc).getvalue()
    
    return text_content

def search_keyword(text, keyword):
    lines = text.split('\n')
    found_lines = [line for line in lines if keyword in line]
    return '\n'.join(found_lines)

#example
file_path = 'example.rtf'
keyword = 'example'
parsed_text = parse_rtf(file_path)
found_text = search_keyword(parsed_text, keyword)
print(found_text)
