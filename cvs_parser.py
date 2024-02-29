from file_parser import InformalParserInterface
import csv 
import re

class CsvParser(InformalParserInterface):
    def check_file(full_file_name: str, target, is_regex: bool, ocr) -> bool:
        with open(full_file_name, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            for row in reader:
                row_text = ','.join(row)
                
                if not is_regex and target in row_text:
                    return True
                elif is_regex and target.search(row_text):
                    return True

        return False
