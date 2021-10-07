import requests
import pandas as pd
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"


class Parser:
    def __init__(self, url, head_csv):
        self.url = url
        self.head_csv = pd.read_csv(head_csv, encoding="1251", sep=';')

    @staticmethod
    def __get_pages_counts(soup):
        return int(soup.find('ul', class_='paginator')
                       .find('a', class_="icon")
                       .get('href')
                       .split('/')[-1])

    @staticmethod
    def __get_content(soup):
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

        return title, year, authors, link, vak, scopus, esci, rsci

    def parse(self, theme, save_csv=False):
        df = self.head_csv
        thems_df = None

        if df[df.theme == theme].main_theme.shape[0]:
            title, year, authors, link, vak, scopus, esci, rsci = [], [], [], [], [], [], [], []
            url = df[df['theme'] == theme].link.values[0]
            r = requests.get(url)
            start_soup = BeautifulSoup(r.text.replace('\t', '').encode('utf-8'), 'lxml')

            for page in tqdm(range(self.__get_pages_counts(start_soup))):
                r = requests.get(url, headers={USER_AGENT}, params={'page': page})
                soup = BeautifulSoup(r.text.replace('\t', '').encode('utf-8'), 'lxml')
                content = self.__get_content(soup)
                title += content[0]
                year += content[1]
                authors += content[2]
                link += content[3]
                vak += content[4]
                scopus += content[5]
                esci += content[6]
                rsci += content[7]

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
                                encoding='utf-8', sep=";", index=False)

            else:

                return thems_df

        else:

            return print('Такая тема не найдена')
