import asyncio
import logging
from pathlib import Path

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


async def recursive_traversal(directory, extensions, target, is_regex, is_ocr):
    tasks = []
    for entry in directory.iterdir():
        try:
            if entry.is_file() and entry.name.split('.')[-1] in extensions:
                print("proccessing: " + entry.path)  # Выводим путь к файлу
                #ext = entry.name.split('.')[-1]
                #tasks.append(asyncio.create_task(read_file(extension_to_parser[ext], entry.path, target, is_regex, is_ocr)))
            elif entry.is_dir():
                tasks.append(recursive_traversal(entry.path, extensions, target, is_regex,is_ocr)) # Рекурсивно обходим директорию асинхронно
        except Exception as e:
            logging.error('Error: %s' % e.message)
    await asyncio.gather(*tasks)


async def main():
    directory_path = 'Z:\Program Files (x86)\Steam'
    await recursive_traversal(directory_path, ["pdf", "txt"], '1', False, False)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
#asyncio.run(main())
