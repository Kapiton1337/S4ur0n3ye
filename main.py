import logging
import os
import asyncio
import random

from cvs_parser import CsvParser
from html_parser import HtmlParser
from odt_parser import OdtParser
from pdf_parser import PdfParser
from rtf_parser import RtfParser

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

async def recursive_traversal(tg, directory, extensions, target, is_regex, is_ocr):
        for entry in os.scandir(directory):
            try:
                if entry.is_file() and any(entry.name.endswith('.' + ext) for ext in extensions):
                    print("proccessing: " + entry.path)  # Выводим путь к файлу
                    ext = entry.name.split('.')[-1]  # Получаем расширение файла
                    tg.create_task(read_file(extension_to_parser["pdf"], entry.path, target, is_regex, is_ocr)) # change pdf to ext
                elif entry.is_dir():
                    await recursive_traversal(tg, entry.path, extensions, target, is_regex, is_ocr)  # Рекурсивно обходим директорию асинхронно
            except Exception as e:
                logging.error('Error: %s' %e.message) 



# Пример использования
async def main():
    async with asyncio.TaskGroup() as tg:
        directory_path = './'
        await recursive_traversal(tg, directory_path, ["pdf", "txt"], '1', False, False)


asyncio.run(main())