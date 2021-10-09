import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm
import time

def main(
    url='https://onemotoring.lta.gov.sg/content/onemotoring/home/buying/upfront-vehicle-costs/open-market-value--omv-.html', 
    save_path='./data/gov_price.csv',
    year_range=[2002, 2022],
    ):
    results = []
    for year in tqdm(range(*year_range)):
        r = requests.get(url, params={'year': year})
        soup = BeautifulSoup(r.text, 'html.parser')
        y = soup.find(attrs={'class': 'yearList'})
        for month, month_data in enumerate(y.find_all(attrs={'class': 'monthList'})):
            month = month + 1
            for brand in month_data.find_all(attrs={'class': 'brandList'}):
                b = brand['id']
                for model, price in zip(
                    brand.find_all(attrs={'class': re.compile('^modelList')}),
                    brand.find_all(attrs={'class': re.compile('^averageOmvList')})
                ):
                    m = model['value']
                    p = price['value']
                    assert p[:2] == 'S$'
                    p = p[2:].replace(',', '')
                    results.append((year, month, b, m, p))
        time.sleep(1)
    df = pd.DataFrame(results, columns=['year', 'month', 'brand', 'model', 'price'])
    df.to_csv(save_path, index=False, encoding='utf-8')


if __name__ == '__main__':
    main()