import csv

def parse_csv(file_path):
    data = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)

    return data

def search_keyword(data, keyword):
    found_rows = [row for row in data if any(keyword in cell for cell in row)]
    return found_rows

#example
file_path = 'example.csv'
keyword = 'example'
parsed_data = parse_csv(file_path)
found_rows = search_keyword(parsed_data, keyword)
for row in found_rows:
    print(row)
