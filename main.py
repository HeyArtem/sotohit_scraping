import requests
from curl_data import(
    url_sotohit,
    headers,
    cookies
)
import os
from bs4 import BeautifulSoup
import time
import random
import json
import csv


'''
Скрапинг сайта 
https://sotohit.ru/internet-magazin2/folder/apple-ipad
раздел планшеты
'''


def get_data():
    # создал объект ссесии
    sess = requests.Session()

    # запрос
    response = sess.get(url=url_sotohit, cookies=cookies, headers=headers)

    # если нет, то создаю директорию
    if not os.path.exists('data'):
        os.mkdir('data')

    # сохраняю страницу
    with open('data/index.html', 'w') as file:
        file.write(response.text)

    # инфоблок
    print(f"[INFO] page recorded")

    # читаю сохраненную стр.
    with open('data/index.html') as file:
        src = file.read()

    # создал объект BeautifulSoup
    soup = BeautifulSoup(src, 'lxml')
    
    # нашел последнюю страницу
    last_page = int(soup.find("ul", class_="shop2-pager").find_all('li')[-2].text)
    # print(last_page)

    # инфоблок
    print(f"[INFO] total number of pages: {last_page}")

    # переменна для записи данных в json
    all_data_json = []

    # переменная для записи данных в csv
    all_data_csv = []

    # генерирую ссылку на каждую страницу
    for pagination_page_count in range(0, last_page):
        pagination_page_url = f"https://sotohit.ru/internet-magazin2/folder/apple-ipad/p/{pagination_page_count}"

        # инфоблок
        print(f"[INFO] work with page №: {pagination_page_count + 1}")

        # запрос к каждой странице 
        response = sess.get(url=pagination_page_url, cookies=cookies, headers=headers).text

        # создал объект BeautifulSoup
        soup = BeautifulSoup(response, "lxml")
    
        # блок с карточками
        product_cards = soup.find_all("div", class_="shop2-product-item")
        
        # собираю информацию из карточек
        for card in product_cards:            
            card_name = card.find('div', class_='product-item-name').text.strip()
            card_description = card.find("div", class_="product-item-anonce").text.replace("\n", "")
            card_price = card.find("div", class_="price-current").text.replace("\n", "")
            card_link = f'https://sotohit.ru{card.find("div", class_="product-item-name").find("a").get("href")}'

            # print(f"Card name: {card_name}\nCard_description: {card_description}\nCard_price: {card_price}\nCard_link: {card_link}\n{20 * '-*-'}")

            # упаковываю данные для записи в json
            all_data_json.append(
                {
                    'card_name': card_name,
                    'card_description': card_description,
                    'card_price': card_price,
                    'card_link': card_link
                }
            )

            # упаковываю данные для записи в csv
            all_data_csv.append(
                [
                    card_name,
                    card_description,
                    card_price,
                    card_link
                ]
            )

            # пауза м.у. запросами к страницам
            time.sleep(random.randrange(2, 4))

    # инфоблок
    print(f"[INFO] data recording") 

    # записываю данные в csv
    with open("data/all_data.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'card_name',
                'card_description',
                'card_price',
                'card_link'
            )
        )
        writer.writerows(all_data_csv)        

    # записываю данные в json
    with open('data/all_data.json', 'w') as file:
        json.dump(all_data_json, file, indent=4, ensure_ascii=False)
    
    # инфоблок
    print(f"[INFO] code completed!")    


def main():
    get_data()


if __name__ == "__main__":
    main()
