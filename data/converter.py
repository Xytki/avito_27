import csv
import json

import django


def converter(csv_file, json_file, model):
    result = []
    with open(csv_file, encoding='utf-8') as csv_f:
        for row in csv.DictReader(csv_f):
            record = {'model': model, "pk":row['id']}
            del row['id']

            if 'price' in row:
                row['price'] = int(row['price'])

            if 'is_published' in row:
                if row['is_published'] == "TRUE":
                    row['is_published'] = True
                else:
                    row['is_published'] = False

            record['fields'] = row
            result.append(record)

    with open(json_file, 'w', encoding='utf-8') as json_f:
        json_f.write(json.dumps(result, ensure_ascii=False))


converter('categories.csv', 'categories.json', 'ads.category')
converter('ads.csv', 'ads.json', 'ads.ad')