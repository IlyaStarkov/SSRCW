import requests
import pandas as pd
import os
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, url, head_csv):
        self.url = url
        self.head_csv = pd.read_csv(head_csv, encoding="1251", sep=';')

    def parse(self, theme, save_csv=False):
        df = self.head_csv
        thems_df = None
        if theme == 'all':
            pass
        elif df[df.theme == theme].main_theme.shape[0]:
            url = df[df['theme'] == theme].link.values[0]
            r = requests.get(url)
            soup = BeautifulSoup(r.text.replace('\t', '').encode('utf-8'), 'lxml')
            title, year, authors, link, vak, scopus, esci, rsci = [], [], [], [], [], [], [], []
            items = soup.find('ul', class_='list').find_all('li')
            for item in items:
                info_about_article = item.find("span").get_text().split('/')
                title.append(item.find('div', class_='title').get_text())
                year.append(int(info_about_article[0]))
                authors.append(info_about_article[1].split(','))
                link.append('https://cyberleninka.ru/' + item.find('a').get('href'))
                if item.find('div', class_='label vak') is not None:
                    vak.append(1)
                else:
                    vak.append(0)
                if item.find('div', class_='label scopus') is not None:
                    scopus.append(1)
                else:
                    scopus.append(0)
                if item.find('div', class_='label esci') is not None:
                    esci.append(1)
                else:
                    esci.append(0)
                if item.find('div', class_='label rsci') is not None:
                    rsci.append(1)
                else:
                    rsci.append(0)

                thems_df = pd.DataFrame({
                    'title': title,
                    'year': year,
                    'authors': authors,
                    'link': link,
                    'ВАК': vak,
                    'Scopus': scopus,
                    'ECSI': esci,
                    'RSCI': rsci
                })

            if save_csv:
                path = os.getcwd() + '\\' + df[df.theme == theme] \
                    .main_theme.values[0] + '\\' + theme

                thems_df.to_csv(path_or_buf=path + '\\' + theme + '.csv',
                                encoding="1251", sep=";", index=False)

            else:

                return thems_df

        else:

            return print('Такая тема не найдена')
