from downloading.struct import DirectoryStructure
from downloading.parser import Parser

URL = 'https://cyberleninka.ru'


struct = DirectoryStructure(URL)
parser = Parser(URL, 'head.csv')
struct.create_directory()
struct.create_csv()
df = parser.head_csv
save_list = []

for theme in df.theme:     # Цикл будет работать около 38 часов.

    save = parser.parse(theme, 250, 15, True)   # В случае ошибки, сохраняем успешно загруженные данные
    save_list.append(save)
