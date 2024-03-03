import asyncio
import logging
import os

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

async def main():
    await recursive_traversal("./Test",['txt', 'pdf'], "34511", 0, 0)

asyncio.run(main())
