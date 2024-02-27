import logging
import os
import asyncio

valid_extensions = ["pdf", "doc", "docx"]; #При необходимости добавить
def read_file(): #Заглушка, здесь должен быть парсер
    return 0

def form_validation(extension):
    for i in valid_extensions:
        if i == extension:
            return 1
    return 0

async def recursive_traversal(directory, extension):
    if not form_validation(extension):
        print("Invalid file format entered")
        return 0
    for entry in os.scandir(directory):
        try:
            if entry.is_file() and entry.name.endswith('.' + extension):
                    print(entry.path)  # Выводим путь к файлу
                    read_file()
            elif entry.is_dir():
                await recursive_traversal(entry.path, extension)  # Рекурсивно обходим директорию асинхронно
        except Exception as e:
            logging.error('Error: %s') %e.message



# Пример использования
async def main():
    directory_path = 'C:/Users/artpo/PycharmProjects/SauronEye'
    await recursive_traversal(directory_path, 'pdf')


asyncio.run(main())