from file_parser import InformalParserInterface
from odf import text, teletype #pip install odfpy
from odf.opendocument import load

class OdtParser(InformalParserInterface):
    def check_file(full_file_name: str, target, is_regex: bool, ocr) -> bool:
        odt_file = load(full_file_name)
        all_text = ""
        for paragraph in odt_file.getElementsByType(text.P):
            all_text += teletype.extractText(paragraph)

        # Проверка содержимого без использования OCR
        if not is_regex and target in all_text:
            return True
        if is_regex and target.search(all_text) != None:
            return True

        # OCR не применим к ODT напрямую, так как это текстовый формат
        return False
