import logging
import os
import asyncio
import random

from cvs_parser import CsvParser
from html_parser import HtmlParser
from odt_parser import OdtParser
from pdf_parser import PdfParser
from rtf_parser import RtfParser

valid_extensions = ["pdf", "doc", "docx"]; #При необходимости добавить

extension_to_parser = {
    "pdf": PdfParser,
    "odt": OdtParser,
    "rtf": RtfParser,
    "cvs": CsvParser,
    "html": HtmlParser,
}


async def read_file(parser, file_path, target, is_regex, is_ocr): 
    if parser.check_file(file_path, target, is_regex, is_ocr):
        print(file_path)
    return 0


def form_validation(extension):
    for i in valid_extensions:
        if i == extension:
            return 1
    return 0

async def recursive_traversal(tg, directory, extension, target, is_regex, is_ocr):
        if not form_validation(extension):
            print("Invalid file format entered")
            return 0
        for entry in os.scandir(directory):
            try:
                if entry.is_file() and entry.name.endswith('.' + extension): # and extension_to_parser[...]!=None ?
                        print("proccessing: " + entry.path)  # Выводим путь к файлу
                        tg.create_task(read_file(extension_to_parser["pdf"], entry.path, target, is_regex, is_ocr)) # change pdf to ext
                elif entry.is_dir():
                    await recursive_traversal(tg, entry.path, extension, target, is_regex, is_ocr)  # Рекурсивно обходим директорию асинхронно
            except Exception as e:
                logging.error('Error: %s' %e.message) 



# Пример использования
async def main():
    async with asyncio.TaskGroup() as tg:
        directory_path = './'
        await recursive_traversal(tg, directory_path, 'pdf', '1', False, False)


asyncio.run(main())