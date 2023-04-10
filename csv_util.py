import csv
import os


def writeToCsvFile(path,name,description):
    file_exists = os.path.exists(path)

    with open(path, 'a', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        if not file_exists:
            csv_writer.writerow(['Name', 'Description'])
        write_list = [name, description]
        csv_writer.writerow(write_list)
