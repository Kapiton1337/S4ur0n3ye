import easyocr


class OCRParser:
    reader = None

    def __init__(self, lang_list=None):
        if lang_list is None:
            lang_list = ['ru', 'en']
        self.reader = easyocr.Reader(lang_list=lang_list,
                                     gpu=False,
                                     detect_network="craft",
                                     recog_network='standard',
                                     download_enabled=True,
                                     detector=True,
                                     recognizer=True,
                                     verbose=True,
                                     quantize=True,
                                     cudnn_benchmark=False)

    def pdf_ocr(self, img, target, is_regex: bool) -> bool:
        text = self.reader.readtext(img, detail=0, paragraph=True)
        text = "".join(text).lower()
        if not is_regex and target in text:
            return True
        if is_regex and target.search(text) is not None:
            return True
        return False
