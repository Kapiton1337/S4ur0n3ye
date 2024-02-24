from file_parser import InformalParserInterface
import fitz # install using: pip install PyMuPDF

class PdfParser(InformalParserInterface):
    def check_file(full_file_name: str, target, is_regex: bool, use_ocr) -> bool: # Target should be str or re.compile() result
        with fitz.open(full_file_name) as doc:
            text = ""
            for page in doc:
                text = page.get_text()
                if not is_regex and target in text:
                        return True
                if is_regex and target.search(text) != None:
                    return True
                imgs = page.get_images()
                for img in imgs:
                    if pdf_ocr(doc.extract_image(img[0])):
                         return True  
        return False


def pdf_ocr(img: dict) -> bool: # Заглушка https://pymupdf.readthedocs.io/en/latest/document.html#Document.extract_image
     return True
# PdfParser.check_file("123.pdf", "uioihj", False, True)