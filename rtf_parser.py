#pip install pyth
from file_parser import InformalParserInterface

class RtfParser(InformalParserInterface):
    def check_file(full_file_name: str, target, is_regex: bool, ocr) -> bool:
        with open(full_file_name, 'r') as file:
            rtf_content = file.read().lower()

        
        if not is_regex and target.lower() in rtf_content:
            return True
        if is_regex and target.search(rtf_content) != None:
            return True

        return False
