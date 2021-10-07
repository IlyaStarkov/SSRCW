from downloading.struct import DirectoryStructure
from downloading.parser import Parser

URL = 'https://cyberleninka.ru'


struct = DirectoryStructure(URL)
parser = Parser(URL, 'head.csv')
struct.create_directory()
struct.create_csv()
df = parser.head_csv
for theme in df.theme:
    parser.parse(theme, True)
