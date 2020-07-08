import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    if r.ok:  # Сервер вернул код 200.
        return r.text
    print(r.status_code)


def write_csv(data):
    with open('catalog.csv', 'a') as file:
        writer = csv.writer(file)

        writer.writerow([
            data['model'],
            data['min_price'],
            data['max_price'],
            data['link']
        ])


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    notebooks = soup.find_all('div', class_="model-short-div list-item--goods-group ms-grp")
    for notebook in notebooks:
        try:                                            # Если значения нет, то записываем пустую строку.
            model = notebook.find_all('a')[0].text
        except:
            model = ''

        try:
            min_price = notebook.find_all('a')[1].find_all('span')[0].text
        except:
            min_price = ''

        try:
            max_price = notebook.find_all('a')[1].find_all('span')[1].text
        except:
            max_price = ''
        try:
            link = 'https://www.e-katalog.ru' + notebook.find_all('a')[0].get('href')
        except:
            link = ''

            data = {
                'model': model,
                'min_price': min_price,
                'max_price': max_price,
                'link': link
            }

            write_csv(data)


def main():
    url = "https://www.e-katalog.ru/list/298/acer/"
    for page_number in range(0, 5):  # Пагинатор по количеству страниц.
        get_page_data(get_html(url + str(page_number)))


if __name__ == '__main__':
    main()
