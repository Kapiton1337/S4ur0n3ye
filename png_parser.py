from file_parser import InformalParserInterface
import pytesseract #pip install pytesseract Pillow
from PIL import Image
import re

class PngParser(InformalParserInterface):
    def check_file(full_file_name: str, target, is_regex: bool, use_ocr: bool) -> bool:
        if not use_ocr:
            return False 

        image = Image.open(full_file_name)
        
        text_content = pytesseract.image_to_string(image, lang='eng')
        
        if not is_regex and target in text_content:
            return True
        elif is_regex and re.search(target, text_content):
            return True

        return False
