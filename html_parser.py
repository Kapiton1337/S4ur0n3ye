from file_parser import InformalParserInterface
from bs4 import BeautifulSoup  #pip install beautifulsoup4 lxml


class HtmlParser(InformalParserInterface):
    def check_file(full_file_name: str, target, is_regex: bool, ocr) -> bool:

        with open(full_file_name, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'lxml')

        text_content = soup.get_text().lower()

        #check target
        if not is_regex and target.lower() in text_content:
            return True
        if is_regex and target.search(text_content) != None:
            return True
        return False
