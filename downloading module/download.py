import requests
from bs4 import BeautifulSoup
import os


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
