import requests
from bs4 import BeautifulSoup
import csv

url = 'https://eda.ru/recepty'
headers = {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
           'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}

def get_html(url, params=''):
    r = requests.get(url, headers=headers, params=params)
    return r

def get_cuisine(result):
    if len(result) > 1:
        if 'кухня' in result[1].get_text():
            return result[1].get_text()
    else:
        return 'Не указано'

def get_type_menu(result):
    if len(result) == 2:
        if 'еда' in result[1].get_text() or 'диета' in result[1].get_text() or 'меню' in result[1].get_text():
            return result[1].get_text()
        else:
            return 'Любое'
    if len(result) >= 3:
        if 'еда' in result[2].get_text() or 'диета' in result[2].get_text() or 'меню' in result[2].get_text():
            return result[2].get_text()
        else:
            return 'Любое'
    else:
        return 'Любое'

def get_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='emotion-m0u77r')
    recepty = []
    for item in items:
        recepty.append(
            {
                'название': item.find('span', class_='emotion-1bs2jj2').get_text().replace('\xa0', ' '),
                'категория' : item.find_all('span', class_='emotion-1h6i17m')[0].get_text(),
                'кухня' : get_cuisine(item.find_all('span', class_='emotion-1h6i17m')),
                'вид меню' : get_type_menu(item.find_all('span', class_='emotion-1h6i17m')),
                'кол-во ингредиентов' : item.find('button', class_='emotion-d6nx0p').get_text(),
                'кол-во порций' : item.find('span', class_='emotion-tqfyce').get_text(),
                'время приготовления' : item.find('span', class_='emotion-14gsni6').get_text(),
                'кол-во сохранений' : int(item.find_all('span', class_='emotion-71sled')[0].get_text()),
                'кол-во лайков'  : int(item.find_all('span', class_='emotion-71sled')[1].get_text()),
                'кол-во дизлайков' : int(item.find_all('span', class_='emotion-71sled')[2].get_text()),
            }
        )
    return recepty

def save_file(items, name):
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['название', 'категория', 'кухня', 'вид меню', 'кол-во ингредиентов', 'кол-во порций', 'время приготовления',
                         'кол-во сохранений','кол-во лайков', 'кол-во дизлайков' ])
        for item in items:
            writer.writerow([item['название'], item['категория'], item['кухня'], item['вид меню'], item['кол-во ингредиентов'],
                             item['кол-во порций'], item['время приготовления'], item['кол-во сохранений'], item['кол-во лайков'], item['кол-во дизлайков']])

def parsing():
    food_info = []
    for page in range(1, 700):
        print(f'Парсим страницу {page}')
        html = get_html(url, params={'page': page})
        food_info.extend(get_info(html.text))
        save_file(food_info, 'food.csv')
    return food_info

parsing()
