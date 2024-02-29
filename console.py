from argparse import ArgumentParser, Namespace
import logging
import os
import asyncio
import re

from cvs_parser import CsvParser
from html_parser import HtmlParser
from ocr_parser import OCRParser
from odt_parser import OdtParser
from pdf_parser import PdfParser
from rtf_parser import RtfParser

parser = ArgumentParser(usage='\r      \n=== SauronEye for PDF ===\n\nUsage: %(prog)s [OPTIONS]+ argument')

parser.add_argument('-t', dest="target", metavar="target", help='Word or phrase to search for')
parser.add_argument('--filetypes', default='pdf', help=' Filetypes to search for')
parser.add_argument('-r', '--regex', action='store_true', help='use this flag if "target" is a regular expression')
parser.add_argument("--fullpath", action='store_true', help="Displays the full path")
parser.add_argument('-d', '--directories', nargs='*', metavar='directory', help="Directories to search")
parser.add_argument('-f', '--files', dest="files", nargs='*', help="path to file/files")
parser.add_argument('--use_ocr', action='store_true', help='Use the OCR method to search for text in pdf images')

args: Namespace = parser.parse_args()


def argcheck():  # модуль в разработке
    print(args)
    if (not args.target and not args.regex) or (not args.directories and not args.onefile):
        print("Error: No word and/or directory\n")
        parser.print_help()
        exit()


extension_to_parser = {
    "pdf": PdfParser,
    "odt": OdtParser,
    "rtf": RtfParser,
    "cvs": CsvParser,
    "html": HtmlParser,
}


async def read_file(parser, file_path, target, is_regex, ocr):
    if parser.check_file(file_path, target, is_regex, ocr):
        print(file_path)
    return 0


async def recursive_traversal(tg, directory, extensions, target, is_regex, ocr):
    for entry in os.scandir(directory):
        try:
            if entry.is_file() and entry.name.split(".")[-1] in extensions:
                print("proccessing: " + entry.path)  # Выводим путь к файлу
                ext = entry.name.split('.')[-1]  # Получаем расширение файла
                tg.create_task(
                    read_file(extension_to_parser[ext], entry.path, target, is_regex, ocr))  # change pdf to ext
            elif entry.is_dir():
                await recursive_traversal(tg, entry.path, extensions, target, is_regex,
                                          ocr)  # Рекурсивно обходим директорию асинхронно
        except Exception as e:
            logging.error('Error: %s' % e.message)

        # Пример использования


async def main():
    if args.regex:
        main_target = re.compile(args.target)
    else:
        main_target = args.target
    if args.use_ocr:
        ocr = OCRParser()
    else:
        ocr = None
    async with asyncio.TaskGroup() as tg:
        if args.directories:
            for directory_path in args.directories:
                await recursive_traversal(tg, directory_path, args.filetypes, main_target, args.regex, ocr)
        elif args.files:
            for file in args.files:
                ext = file.split('.')[-1]  # Получаем расширение файла
                read_file(extension_to_parser[ext], file, args.regex, ocr)


asyncio.run(main())
