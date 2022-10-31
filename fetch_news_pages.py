import requests
import datetime
import urllib.parse
import os
import sys
from lxml import html


EPOCH_START = datetime.date(2017, 1, 1)
EPOCH_END = datetime.date(2018, 1, 1)


def main():
    os.makedirs('./data', exist_ok=True)

    date_cursor = EPOCH_START
    dt = datetime.timedelta(days=1)

    all_links = []

    while date_cursor < EPOCH_END:
        url = 'http://www.fontanka.ru/fontanka/{:%Y/%m/%d}/all.html'.format(date_cursor)
        response = requests.get(url)

        if response.status_code != 200:
            print('Warning: GET {} returned {} code'.format(url, response.status_code), file=sys.stderr)
            continue

        tree = html.fromstring(response.content)
        links = tree.xpath('//div[contains(@class, "JRajd")]/div/a/@href')
    
        for link in links:
            if link.startswith('/') or 'www.fontanka.ru' in link:
                link = urllib.parse.urljoin('http://www.fontanka.ru/', link)
                all_links.append(link)
            else:
                print('Warning: {} link is external, skipping'.format(link), file=sys.stderr)

        print('{:%Y-%m-%d} done, total links: {}'.format(date_cursor, len(all_links)))
        date_cursor += dt

    with open('./data/links.txt', 'w') as f:
        f.write('\n'.join(all_links))


if __name__ == '__main__':
    main()