import os
import pandas as pd

from bs4 import BeautifulSoup


def get_html(html_path):
    with open(html_path, 'r') as f:
        html = f.read()
    return html


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    container_content = soup.find_all('div', {'class': 'container content'})

    data_list = []

    for parent in container_content:
        list_resource = parent.find_all('li', {'class': 'resource'})
        for resource in list_resource:
            try:
                name = resource.find('a', {'class': 'website'}).text
            except AttributeError:
                continue

            try:
                website = resource.find('a', {'class': 'website'}).get('href')
            except AttributeError:
                website = None

            try:
                phone = resource.find(
                    'span', {'class': 'phone'}).text.encode('utf-8')
            except AttributeError:
                phone = None

            data_list.append(
                {'name': name, 'website': website, 'phone': phone})

    return pd.DataFrame(data_list)


def main():
    path = os.path.dirname(os.path.realpath(__file__))
    html = get_html(html_path=os.path.join(path, 'data', 'pagesource.html'))
    df = get_data(html=html)
    df.to_csv(os.path.join(path, 'results.csv'))


if __name__ == '__main__':
    main()
