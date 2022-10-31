import os
import re
import tqdm
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import nltk



nltk.download('stopwords')



stemmer = SnowballStemmer('russian')
stop_words = set(stopwords.words('russian'))

mapping = {
    'Водитель Петербурга Live': 'Авто',
    'Водитель Петербурга': 'Авто',
    'Водитель Петербурга.Live': 'Авто',
    'Бизнес в кризис': 'Бизнес',
    'Бизнес-трибуна': 'Бизнес',
    'Доктор Питер': 'Здоровье и красота',
    '47новостей из Ленинградской Области': 'Город',
    'Афиша Plus': 'Афиша',
    'Большое интервью': 'Интервью',
    'ЗЕНИТУ 90 ЛЕТ': 'Спорт',
    'Итоги недели с Андреем Константиновым': 'Авторские новости',
    'Итоги недели с Константиновым': 'Авторские новости',
    'Квадрат': 'Недвижимость',
    'Лахта центр': 'Строительство',
    'Охта центр': 'Недвижимость',
    'Новости компаний': 'Бизнес',
    'Федор Погорелов': 'Спорт',
    'Мужчина и женщина': 'Личная жизнь',
    'Материнский инстинкт': 'Личная жизнь',
    'Точка опоры': 'Общество',
    'Год N300': 'Город',
    'Доброе дело': 'Благотворительность',
    'Адвита': 'Благотворительность',
    'Кино': 'Культура',
    'Книги': 'Культура',
    'Культурный поводырь': 'Культура',
    'Музыка': 'Культура',
    'Театральная гостиная': 'Культура',
    'Театры': 'Культура',
    'Очевидец': 'Происшествия',
    'Профессионал': 'Работа'
}

allowed = {
    'Авто',
    'Афиша',
    'Бизнес',
    'Благотворительность',
    'Власть',
    'Выборы',
    'Город',
    'Деньги',
    'Домашний очаг',
    'Дороги',
    'Доступная среда',
    'ЖКХ',
    'Здоровье и красота',
    'Культура',
    'Личная жизнь',
    'Недвижимость',
    'Общество',
    'Работа',
    'Спорт',
    'Строительство',
    'Теракты',
    'Технологии',
    'Туризм',
    'Финансы'
}

mapping_lower = dict(map(lambda p: (p[0].lower(), p[1].lower()), mapping.items()))
allowed_lower = set(map(lambda s: s.lower(), allowed))


def clean_tokenize_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]+', '', text)
    tokens = text.split()

    cleaned_tokens = []
    for token in tokens:
        if token.isdigit():
            cleaned_tokens.append('@number')
        elif token not in stop_words and len(token) > 2:
            cleaned_tokens.append(stemmer.stem(token))

    return cleaned_tokens


def clean_category(text):
    text = text.lower().strip()

    adv_suffix = 'публикуется на правах рекламы'

    while text.endswith(adv_suffix):
        text = text[:-len(adv_suffix)].strip()

    text = text.strip()

    if text in mapping_lower:
        text = mapping_lower[text]

    if text in allowed_lower:
        return text

    return


def process_file(filename):
    with open('./data/news/' + filename, 'r') as f:
        category = f.readline().strip()
        content = f.read().strip()

    category = clean_category(category)

    if category is None:
        return

    content = clean_tokenize_text(content)

    with open('./data/cleaned/' + filename, 'w') as f:
        f.write(category + '\n')
        f.write(' '.join(content))


def main():
    os.makedirs('./data/cleaned', exist_ok=True)
    news_files = os.listdir('./data/news')
    for file in tqdm.tqdm(news_files):
        process_file(file)


if __name__ == '__main__':
    main()