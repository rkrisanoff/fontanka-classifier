import requests
import os.path
import hashlib
import multiprocessing
import os
import sys
import tqdm
from lxml import html


def normalize_line(line):
    words = line.split()

    return ' '.join(words)


def normalize_text(text):
    lines = text.split('\n')
    normalized_lines = []

    for line in lines:
        line = line.strip()
        if line:
            normalized_lines.append(normalize_line(line))

    return ' '.join(normalized_lines)


def fetch_news_page(url):
    response = requests.get(url)

    if response.status_code != 200:
        print('Error: GET {} returned {} code'.format(url, response.status_code), file=sys.stderr)
        return

    tree = html.fromstring(response.content)
    title = ' '.join(tree.xpath('//h1[contains(@class, \'DVat\')]//text()'))
    content = "\n".join([p.text_content() for p in tree.xpath('//div[contains(@class, \'EPa9\')]/p')])
    category = ' '.join(tree.xpath('//div[contains(@class, \'DVrh\')]//text()'))

    title = title.strip()
    content = content.strip()
    category = category.strip()

    if not title:
        print('Warning: {} has no title'.format(url), file=sys.stderr)

    if not content:
        print('Error: {} has no content'.format(url), file=sys.stderr)
        return

    if not category:
        print('Error: {} has no category'.format(url), file=sys.stderr)
        return

    title = normalize_line(title)
    content = normalize_text(content)
    category = normalize_line(category)

    return url, title, category, content



def main():
    os.makedirs('./data/news', exist_ok=True)

    with open('./data/links.txt', 'r') as f:
        links = list(map(lambda s: s.strip(), f.readlines()))

    pool = multiprocessing.Pool(4)

    for res in tqdm.tqdm(pool.imap_unordered(fetch_news_page, links)):
        if res is not None:
            url, title, category, content = res
            filename = hashlib.sha1(url.encode('UTF-8')).hexdigest()
            with open('./data/news/' + filename + '.txt', 'w') as f:
                f.write(category + '\n')
                f.write(title + '\n')
                f.write(content)


if __name__ == '__main__':
    main()