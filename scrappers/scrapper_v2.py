import requests
from bs4 import BeautifulSoup
import re

# import headers pattern from .gitignore
pattern = 'http://az.lib.ru'
headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "stg_traffic_source_priority=4; stg_externalReferrer=https://www.google.com/; stg_last_interaction=Mon%2C%2008%20Apr%202024%2009:20:48%20GMT; stg_returning_visitor=Mon%2C%2008%20Apr%202024%2009:20:48%20GMT"
        }

seed_urls = []


def get_headers():
    return headers


def make_requests(url):
    response = requests.get(url=url, headers=headers)
    return response


def create_soup(url):
    return BeautifulSoup(make_requests(url).text, 'html.parser')


def retrieve_authors_urls(seed_url):
    soup = create_soup(seed_url)
    authors_urls = []
    seed_urls = soup.find_all('dl')
    for url in seed_urls:
        authors_urls.append(f"{pattern}{url.find('a').get('href')}")
    return authors_urls


def retrieve_texts_urls(author_url):
    soup = create_soup(author_url)
    body_dl = soup.find('dl')
    dls = body_dl.find_all('dl')

    text_urls = []
    for dl in dls:
        link = dl.find('a').get('href')
        if 'text' in link:
            if re.search(r'/./', link):
                text_urls.append(f'{pattern}{link}')
            else:
                text_urls.append(f'{author_url}{link}')

    return text_urls


# def get_text(text_url):
#     soup = create_soup(text_url)
#     text = soup.find('div', align='justify').text
#     return text

# def get_text(text_url):
#     soup = create_soup(text_url)
#     body = soup.find('div', align='justify')
#     body = body.find('xxx7')
#     # text = body.find_all('dd', recursive=False)
#     return body


def get_text(text_url):
    soup = create_soup(text_url)
    text = [dd for dd in soup.find_all('dd') if not dd.children()]
    return text


def dd():
    # проверка на 200
    return None


# def prepare_environment(base_path=''):
#     if base_path.exists():
#         shutil.rmtree(base_path.parent)
#         base_path.parent.mkdir()
#         base_path.mkdir()
#     else:
#         base_path.parent.mkdir()
#         base_path.mkdir()


def __main__():
    # for seed_url in seed_urls:
    #     authors= retrieve_authors_urls(seed_url)

    # for author in authors:
    #     text_urls = retrieve_texts_urls(author)

    # author_url = 'http://az.lib.ru/a/andreew_l_n/'
    # print(retrieve_texts_urls(author_url))
    # print('=============' * 100)
    # seed_url = 'http://az.lib.ru/rating/litarea/index_3.shtml'
    # print(retrieve_authors_urls(seed_url))
    print(get_text('http://az.lib.ru/a/andreew_l_n/text_0810.shtml'))


if __name__ == '__main__':
    __main__()
