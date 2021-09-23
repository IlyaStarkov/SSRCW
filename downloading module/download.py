import requests
import os
from bs4 import BeautifulSoup
import shutil


class Download:
    def __init__(self, url):
        if url[-1] == '/':
            print("Удалите последнюю косую черту из адресса")
        else:
            self.r = requests.get(url)
            self.url = url

    def __get_links(self):
        soup = BeautifulSoup(self.r.text.replace('\t', '').encode('utf-8'), 'lxml')
        links = soup.find_all("li")
        end_list, label = [], ''
        for item in links:
            if item.attrs.get('class') is not None:
                label = item.string
            elif item.string != u"\xa0":
                end_list.append((label, item.string.replace('\xa0', ' '),
                                 self.url + item.find('a').get('href')))
        return end_list

    @staticmethod
    def __create_folder(name, directory=os.getcwd()):
        try:
            os.mkdir(directory + name)
        except FileExistsError:
            print("Директория уже создана")

    def create_directory(self):
        links = self.__get_links()
        label = ''
        for link in links:
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
                for link in links:
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
