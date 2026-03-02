import requests
from bs4 import BeautifulSoup
import re

def get_results(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    # Используем lxml для скорости
    soup = BeautifulSoup(response.text, 'lxml')

    for element in soup.find_all(['div', 'p', 'b']):
        clean_text = " ".join(element.get_text().split()).replace('\xad', '')
        
        if 'Вариант № ' in clean_text:
            match = re.search(r'Вариант № (.*?):', clean_text)
            if match:
                variant_num = match.group(1)
        if "Вы набрали" in clean_text:
            # Если нашли нужную строку, вырезаем данные и выходим из цикла
            match = re.search(r'Вы набрали (.*?) из', clean_text)
            if match:
                score_text = match.group(1)

    wrong_tasks = []
    for table in soup.find_all('table'):
        header_tag = table.find_previous('b')
        name = ''
        if header_tag:
            name = " ".join(header_tag.get_text().split()).replace('\xad', '')
        if 'Тестовая часть' in name or 'Развернутая часть' in name :
            for row in table.find_all('tr'):
                data = []
                for column in row.find_all('td'):
                    data.append(column.text)
                if data and data[0].isnumeric() and data[-2].split()!=data[-1].split():
                    wrong_tasks.append(data[0])

    return str(variant_num), str(score_text), ', '.join(wrong_tasks)