import requests
import requests.exceptions
from bs4 import BeautifulSoup
import json

# persons_urls_lists = []
# for i in range(0, 760, 20):
#     url = f'https://www.bundestag.de/ajax/filterlist/en/members/453158-453158?limit=20&noFilterSet=true&offset={i}'
#
#     #Генерирую опрос и собираю все ссылки на страницы людей
#     req = requests.get(url)
#     result = req.content
#     #Извлекаю данные из страниц
#     soup = BeautifulSoup(result, 'lxml')
#     persons = soup.find_all(class_= 'bt-open-in-overlay')
#
#     for person in persons:
#         person_page_url = person.get('href')
#         persons_urls_lists.append(person_page_url)
#
# with open('persons_url_list.txt', 'a') as file:
#     for line in persons_urls_lists:
#         file.write(f'{line}\n')


with open('persons_url_list.txt') as file:
    lines = [line.strip() for line in file.readlines()]

    database_dict = []

    counter = 0

    for line in lines:
        req = requests.get(line)
        result = req.content

        soup = BeautifulSoup(result, 'lxml')
        person = soup.find(class_='bt-biografie-name').find('h3').text
        person_name_party = person.strip().split(',')
        person_name = person_name_party[0]
        person_party = person_name_party[1].strip()

        social_networks = soup.find_all(class_='bt-link-extern')

        social_networks_urls = []
        for link in social_networks:
            social_networks_urls.append(link.get('href'))

        database = {
            'person_name': person_name,
            'party_name': person_party,
            'social_networks': social_networks_urls
        }
        # Для наглядности
        counter += 1
        print(f'№{counter}:{line} is done')
        database_dict.append(database)

        with open('database.json', 'w') as json_file:
            json.dump(database_dict, json_file, indent=4)
