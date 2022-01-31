import pandas as pd
from langdetect import detect
from tqdm import tqdm


articles = pd.read_csv('SSRCW/articles.csv', encoding='utf-8', sep=';')
language = []
for i in tqdm(articles.title):
    language.append(detect(i))
articles.language = language
articles.to_csv('articles.csv', encoding='utf-8', sep=";", index=False)
