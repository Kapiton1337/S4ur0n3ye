from file_parser import InformalParserInterface
import fitz  # install using: pip install PyMuPDF


class PdfParser(InformalParserInterface):
    def check_file(full_file_name: str, target, is_regex: bool,
                   ocr=None) -> bool:  # Target should be str or re.compile() result
        with fitz.open(full_file_name) as doc:
            for page in doc:
                text = page.get_text().lower()
                if not is_regex and target in text:
                    return True
                if is_regex and target.search(text) is not None:
                    return True
                if ocr is None:
                    continue
                imgs = page.get_images()
                for img in imgs:
                    if ocr.pdf_ocr(doc.extract_image(img[0])['image'], target, is_regex):
                        return True
        return False

