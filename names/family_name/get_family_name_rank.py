import json
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

for page in tqdm(range(80)):
    url = f'https://myoji-yurai.net/prefectureRanking.htm?prefecture=%E5%85%A8%E5%9B%BD&page={page}'

    response = requests.get(url)
    contents = response.text
    parsed_contents = BeautifulSoup(contents)

    family_name_list = []

    simple_tables = parsed_contents.find_all('table', class_='simple')

    for table in simple_tables:
        tr_list = table.find_all('tr', class_='odd')
        if not tr_list:
            continue

        for tr in tr_list:
            td_list = tr.find_all('td')
            if not td_list[0] or not '位' in td_list[0].text:
                continue

            rank = td_list[0].text
            family_name = td_list[1].text
            count = td_list[2].text

            family_name_list.append({
                'rank': int(rank[:-1]),
                'family_name': family_name,
                'count': count
            })

    with open(f'family_name_page_{page}.json', 'w') as f:
        json.dump(family_name_list, f, ensure_ascii=False)
