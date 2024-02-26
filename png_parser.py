#pip install pytesseract pillow

import pytesseract
from PIL import Image

def parse_png(file_path):
    image = Image.open(file_path)

    recognized_text = pytesseract.image_to_string(image)

    return recognized_text

def search_keyword(text, keyword):
    lines = text.split('\n')
    found_lines = [line for line in lines if keyword in line]
    return '\n'.join(found_lines)

#example
file_path = 'example.png'
keyword = 'example'
parsed_text = parse_png(file_path)
found_text = search_keyword(parsed_text, keyword)
print(found_text)