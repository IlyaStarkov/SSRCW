import requests
import os
import shutil
import pandas as pd
from bs4 import BeautifulSoup


class DirectoryStructure:
    def __init__(self, url, path=os.getcwd()):
        if url[-1] == '/':
            print("Удалите последнюю косую черту из адресса")
        else:
            os.chdir(path)
            self.r = requests.get(url)
            self.url = url
            self.path = path

    def __get_links(self):
        soup = BeautifulSoup(self.r.text.replace('\t', '').encode('utf-8'), 'lxml')
        links = soup.find_all("li")
        main_theme, theme, link = [], [], []
        label = ''
        for item in links:
            if item.attrs.get('class') is not None:
                label = item.string
            elif item.string != u"\xa0":
                main_theme.append(label)
                theme.append(item.string.replace('\xa0', ' '))
                link.append(self.url + item.find('a').get('href'))

        return pd.DataFrame({
                             'main_theme': main_theme,
                             'theme': theme,
                             'link': link
        })

    def __create_folder(self, name):
        try:
            os.mkdir(self.path + name)
        except FileExistsError:
            print("Директория уже создана")

    def create_directory(self):
        links = self.__get_links()
        label = ''
        for link in links.iloc:
            if label != link[0]:
                label = link[0]
                self.__create_folder("/" + label)
                self.__create_folder("/" + label + "/" + link[1])
            else:
                self.__create_folder("/" + label + "/" + link[1])

    def delete_directory(self, folder):
        if folder == 'all':
            try:
                """Возможная функция возвращающая глобальные темы статей"""

                links = self.__get_links()
                name_of_folders = []
                for link in links.iloc:
                    name_of_folders.append(link[0])
                """______________________________________"""

                for folder in set(name_of_folders):
                    shutil.rmtree(folder)
            except FileNotFoundError:
                return print('Такой папки не существует в данной директории')
        else:
            try:
                shutil.rmtree(folder)
            except FileNotFoundError:
                return print('Такой папки не существует в данной директории')

    def create_csv(self):
        name = 'head'
        self.__get_links().to_csv(path_or_buf=os.getcwd()+'\\'+name+'.csv',
                                  encoding="utf-8", sep=";", index=False)
