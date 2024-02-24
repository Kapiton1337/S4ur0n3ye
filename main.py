import os
import asyncio

async def recursive_traversal(directory):
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith('.pdf'):
            print(entry.path)  # Выводим путь к файлу
        elif entry.is_dir():
            await recursive_traversal(entry.path)  # Рекурсивно обходим директорию асинхронно

# Пример использования
async def main():
    directory_path = 'Z:/Program Files (x86)/Steam'
    await recursive_traversal(directory_path)

asyncio.run(main())
