import requests
import urllib.parse
import os
import sys
from lxml import html


def main():
    os.makedirs('./data', exist_ok=True)

    all_links = []

    pages = [i+1 for i in range(60)]

    for page in pages:

        url = f'https://www.fontanka.ru/cgi-bin/search.scgi?query=Мурино&sortt=date&fdate=2000-01-01&tdate=2022-10-31&offset={page}'
        response = requests.get(url)


        if response.status_code != 200:
            print('Warning: GET {} returned {} code'.format(url, response.status_code), file=sys.stderr)
            continue

        tree = html.fromstring(response.content)
        links = tree.xpath('//div[contains(@class, "CPop")]/div/a[contains(@class,"EHgf")=false]/@href')

        for link in links:
            if link.startswith('/') or 'www.fontanka.ru' in link:
                link = urllib.parse.urljoin('http://www.fontanka.ru/', link)
                all_links.append(link)
            else:
                print('Warning: {} link is external, skipping'.format(link), file=sys.stderr)

        print(f'{page} page done, total links: {len(all_links)}')

    with open('./data/links.txt', 'w') as f:
        f.write('\n'.join(all_links))

if __name__ == '__main__':
    main()