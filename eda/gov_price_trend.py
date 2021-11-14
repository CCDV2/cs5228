import matplotlib.pyplot as plt
import pandas as pd
import json
from typing import List
import os

gov_price_json_path = './data/gov_price.json'
if not os.path.exists(gov_price_json_path):
    df = pd.read_csv('./data/gov_price.csv')

    d = {}
    for i, (year, month, brand, model, price) in df.iterrows():
        try:
            brand = brand[6:].lower()
            model = model.lower()
            if brand not in d:
                d[brand] = {}
            if model not in d[brand]:
                d[brand][model] = {}
            d[brand][model][year * 12 + month] = price
        except Exception as e:
            print(i, e)
    d['others'] = {}
    with open(gov_price_json_path, 'w') as f:
        json.dump(d, f)
else:
    with open(gov_price_json_path, 'r') as f:
        d = json.load(f)


"""
for brand, models in d.items():
    print(f'Brand {brand} has {len(models)} models')
    for model, timelines in models.items():
        pass
"""
df = pd.read_csv('./data/train.csv')

with open('./data/brand_mapping.json', 'r') as f:
    brand_map = json.load(f)


def vague_match(s: str, patterns: List[str]):
    def to_words(s: str):
        s = s.replace('-', ' ').replace('(', ' ').replace(')', ' ')
        return s.split()

    def similarity(words, pattern):
        sim = 0
        for w in words:
            for p in pattern:
                if w in p:
                    sim += 1
                    break
        return sim

    words = to_words(s)
    words_patterns = [(to_words(p), i) for i, p in enumerate(patterns)]
    similarity = [(similarity(words, wp), wp, i) for wp, i in words_patterns]
    similarity.sort(reverse=True)
    print(f'match for {s}', *similarity[:5], sep='\n')

for i, row in df.iterrows():
    type_of_vehicle = row['type_of_vehicle']
    make = row['make']
    from_title = False
    if type(make) is float:
        from_title = True
        make = row['title'].split()[0].lower()
    model = row['model'].lower()
    if make in brand_map:
        make = brand_map[make]
    if not make in d:
        print(make, '' if not from_title else 'from title')
        continue
    if make == "others":
        continue
    title = row['title'].lower()
    vague_match(title, list(d[make].keys()))





