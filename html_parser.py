#pip install beautifulsoup4

from bs4 import BeautifulSoup

def parse_html(file_path):
    text_content = ""

    with open(file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    text_content += soup.get_text(separator='\n')
    return text_content

def search_keyword(text, keyword):
    lines = text.split('\n')
    found_lines = [line.strip() for line in lines if keyword in line]
    return '\n'.join(found_lines)

#example
file_path = 'example.html'
keyword = 'example'
parsed_text = parse_html(file_path)
found_text = search_keyword(parsed_text, keyword)
print(found_text)
