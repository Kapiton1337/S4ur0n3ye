
from argparse import ArgumentParser, Namespace
import sys
import os
import logging
import asyncio
# from file_parser import InformalParserInterface
import fitz # install using: pip install PyMuPDF



parser = ArgumentParser(usage='%(prog)s [OPTIONS]+ argument', epilog='=== SauronEye for PDF ===')


parser.add_argument('-v', '--version', action="version", version='%(prog)s 0.3')
parser.add_argument('-t', dest="target", metavar="target" ,  help='Word or phrase to search for')
parser.add_argument('--filetypes', default='pdf', help=' Filetypes to search for')
parser.add_argument('-r', '--regex',action='store_true', help='use this flag if "target" is a regular expression' )
parser.add_argument("-fullpath",action='store_true', help="Displays the full path") 
parser.add_argument('-d', '--directories', nargs='*', metavar='directory', help="Directories to search")
parser.add_argument('-f', '--files', dest="files", nargs='*', help="path to file/files")
parser.add_argument('--use_ocr',action='store_true', help='Use the OCR method to search for text in pdf images' )

args: Namespace= parser.parse_args()

def argcheck(): # модуль в разработке 
    print(args)
    if (not args.target and not args.regex) or (not args.directories and not args.onefile):
        print("Error: No word and/or directory\n")
        parser.print_help()
        exit()

    
valid_extensions = ["pdf", "doc", "docx"]
def form_validation(extension):
    for i in valid_extensions:
        if i == extension:
            return 1
    return 0


class InformalParserInterface:
    def check_file(full_file_name: str, target, is_regex: bool, use_ocr: bool) -> bool:
        pass


class PdfParser(InformalParserInterface):
    def check_file(full_file_name: str, target, is_regex: bool, use_ocr: bool) -> bool: # Target should be str or re.compile() result
        with fitz.open(full_file_name) as doc:
            text = ""
            for page in doc:
                text = page.get_text()
                if not is_regex and target in text:
                        return True
                if is_regex and target.search(text) != None:
                    return True
                if not use_ocr:
                     continue
                imgs = page.get_images()
                for img in imgs:
                    if pdf_ocr(doc.extract_image(img[0]), target, is_regex):
                         return True  
        return False


def pdf_ocr(img: dict, target, is_regex: bool) -> bool: # Заглушка https://pymupdf.readthedocs.io/en/latest/document.html#Document.extract_image
     return True




async def recursive_traversal(directory, extension):
    if not form_validation(extension):
        print("Invalid file format entered")
        return 0
    for entry in os.scandir(directory):
        try:
            if entry.is_file() and entry.name.endswith('.' + extension):

                    if PdfParser.check_file(entry.path, args.target, args.regex, args.use_ocr): # переменные передаются через опции --regex --use_ocr
                        if args.fullpath:
                            print(os.path.abspath(entry.path))
                            
                        else:
                            print(entry.path)


            elif entry.is_dir():
                await recursive_traversal(entry.path, extension)  # Рекурсивно обходим директорию асинхронно
        except Exception as e:
            logging.error('Error: %s') %e.message


        
# Пример использования
async def main():
    if args.directories:
        for path_to_dir in args.directories:
            await recursive_traversal(path_to_dir, args.filetypes)
    # elif args.files:               
    #     for file in args.files:
    #         d[]
    # ======= Добавить (Андрей)


argcheck()
asyncio.run(main())

print("Process done.")



 
    
