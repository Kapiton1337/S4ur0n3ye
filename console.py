from argparse import ArgumentParser, Namespace
import logging
import os
import asyncio
import re
import time
import sys


from csv_parser import CsvParser
from html_parser import HtmlParser

from odt_parser import OdtParser
from pdf_parser import PdfParser
#from rtf_parser import RtfParser

Sauron = r"""      
 $$$$$$\   $$$$$$\  $$\   $$\ $$$$$$$\   $$$$$$\  $$\   $$\ $$$$$$$$\ $$\     $$\ $$$$$$$$\ 
$$  __$$\ $$  __$$\ $$ |  $$ |$$  __$$\ $$  __$$\ $$$\  $$ |$$  _____|\$$\   $$  |$$  _____|
$$ /  \__|$$ /  $$ |$$ |  $$ |$$ |  $$ |$$ /  $$ |$$$$\ $$ |$$ |       \$$\ $$  / $$ |      
\$$$$$$\  $$$$$$$$ |$$ |  $$ |$$$$$$$  |$$ |  $$ |$$ $$\$$ |$$$$$\      \$$$$  /  $$$$$\    
 \____$$\ $$  __$$ |$$ |  $$ |$$  __$$< $$ |  $$ |$$ \$$$$ |$$  __|      \$$  /   $$  __|   
$$\   $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |\$$$ |$$ |          $$ |    $$ |      
\$$$$$$  |$$ |  $$ |\$$$$$$  |$$ |  $$ | $$$$$$  |$$ | \$$ |$$$$$$$$\     $$ |    $$$$$$$$\ 
 \______/ \__|  \__| \______/ \__|  \__| \______/ \__|  \__|\________|    \__|    \________|

"""

parser = ArgumentParser(usage='\r      ' f'{Sauron}\nUsage: %(prog)s [OPTIONS]+ argument')

parser.add_argument('-t', dest="target", metavar="target", help='Word or phrase to search for')
parser.add_argument('--filetypes', nargs='*', default='pdf', help=' Filetypes to search for')
parser.add_argument('-r', '--regex', action='store_true', help='use this flag if "target" is a regular expression')
parser.add_argument("--fullpath", action='store_true', help="Displays the full path")
parser.add_argument('-d', '--directories', nargs='*', metavar='directory', help="Directories to search")
parser.add_argument('-f', '--files', dest="files", nargs='*', help="path to file/files")
parser.add_argument('--use_ocr', action='store_true', help='Use the OCR method to search for text in pdf images')

args: Namespace = parser.parse_args()






def argcheck():  
    supported_ext={"pdf", "odt", "csv", "html"}
    if (not args.target) or (not args.directories and not args.files):
        print("Error: No target and/or directory\n")
        parser.print_help()
        sys.exit()
    if args.files:
        for file in args.files:
            if not os.path.isfile(file):
                print(f"[!] {file} is not a file")
                sys.exit()  
    if args.directories:
        for dir_path in args.directories:
            if not os.path.isdir(dir_path):
                print(f"[!] {dir_path} is not a directory")
                sys.exit()   
    if args.filetypes:
        if type(args.filetypes) == list:
            for types in args.filetypes:
                if not (types in supported_ext):
                    print(f"[!] Error: {types} is not a supported file format")
                    print(f"[*] Supported file formats: {supported_ext}")
                    exit()
        else:
            if not (args.filetypes in supported_ext):
                    print(f"[!] Error: {args.filetypes} is not a supported file format")
                    print(f"[*] Supported file formats: {supported_ext}")
                    exit()
            

    #print(f"[*] File type: .{args.filetypes}")


extension_to_parser = {
    "pdf": PdfParser,
    "odt": OdtParser,
   # "rtf": RtfParser,
    "csv": CsvParser,
    "html": HtmlParser,
}





async def read_file(parser, file_path, target, is_regex, ocr):
    if parser.check_file(file_path, target, is_regex, ocr):
        print("[+] " + file_path)
    return 0


async def recursive_traversal(directory, extensions, target, is_regex, ocr):
    tasks = []
    for entry in os.scandir(directory):
        try:
            if entry.is_file() and entry.name.split(".")[-1] in extensions:
                ext = entry.name.split('.')[-1]  # Получаем расширение файла
                tasks.append(asyncio.create_task(
                    read_file(extension_to_parser[ext], entry.path, target, is_regex, ocr)))  # change pdf to ext
            elif entry.is_dir():
                await recursive_traversal(entry.path, extensions, target, is_regex,
                                          ocr)  # Рекурсивно обходим директорию асинхронно
        except Exception as e:
            logging.error('Error: %s' % e.message)
        await asyncio.gather(*tasks)

        # Пример использования


async def main():
    argcheck()
    print("[*] Process started")
    start_time = time.time()
    if args.regex:
        main_target = re.compile(args.target)
    else:
        main_target = args.target.lower()
    if args.use_ocr:
        print("[*] OCR model initialization")
        from ocr_parser import OCRParser  # Вынес сюда import, Инициализация -2 секунды
        print("[+] Initialization completed")
        ocr = OCRParser()
    else:
        ocr = None
    print("[*] Scanning files...")

    if args.directories:
        for directory_path in args.directories:
            await recursive_traversal(directory_path, args.filetypes, main_target, args.regex, ocr)
    elif args.files:
        for file in args.files:
            ext = file.split('.')[-1]  # Получаем расширение файла
            await read_file(extension_to_parser[ext], file, main_target, args.regex, ocr)

    print(f"[+] Done.\n[!]Execution time: {round(time.time() - start_time, 4)} seconds.")


asyncio.run(main())
