import requests
from bs4 import BeautifulSoup
import re
import os

pattern = 'http://az.lib.ru'
headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "stg_traffic_source_priority=4; stg_externalReferrer=https://www.google.com/; stg_last_interaction=Mon%2C%2008%20Apr%202024%2009:20:48%20GMT; stg_returning_visitor=Mon%2C%2008%20Apr%202024%2009:20:48%20GMT"
        }

seed = ["http://az.lib.ru/rating/litarea/index_3.shtml"]


def get_headers():
    return headers


def make_requests(url):
    try:
        response = requests.get(url=url, headers=headers, timeout=7)
        response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        print(f"Таймаут при запросе к {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return None


def create_soup(url):
    response = make_requests(url)
    if response is None:
        return None
    return BeautifulSoup(response.text, 'html.parser')


def retrieve_authors_urls(seed_url):
    soup = create_soup(seed_url)
    authors_urls = []
    seed_urls = soup.find_all('dl')
    for url in seed_urls:
        authors_urls.append(f"{pattern}{url.find('a').get('href')}")
    return authors_urls


def retrieve_texts_urls(author_url):
    soup = create_soup(author_url)
    if soup:
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
    return None


def get_text(text_url):
    soup = create_soup(text_url)
    if soup:
        div_justify = soup.find('div', align='justify')
        if div_justify is not None:
            return div_justify.text.strip()
        else:
            print(f"Внимание: не найден div с align='justify' на странице {text_url}")
            return None
    return None


def save_text_to_file(text, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(text.strip())


def main():
    for seed_url in seed:
        print(f"\nОбработка начального URL: {seed_url}")
        authors = retrieve_authors_urls(seed_url)
        print(f"Найдено авторов: {len(authors)}")
        auth_check = authors[500:620]
        print(f'Новое количество: {len(auth_check)}')

        for i, author_url in enumerate(auth_check):
            text_urls = retrieve_texts_urls(author_url)
            if text_urls:
                print(f"{i+1} Автор: {author_url}, найдено текстов: {len(text_urls)}")

                for text_url in text_urls:
                    text = get_text(text_url)
                    if text:
                        save_text_to_file(text,
                                          "./texts/collected_literary_texts.txt")
                        print(f"Обработана страница: {text_url}")
            continue
    print("Сбор текстов завершен.")


if __name__ == '__main__':
    main()


# def save_texts_to_file(texts, filename="collected_literary_texts.txt"):
#     with open(filename, 'w', encoding='utf-8') as f:
#         for text in texts:
#             f.write(text)
#             f.write("\n\n" + "="*80 + "\n\n")

#
# def save_texts_to_file(texts, filepath):
#     # Создаём директорию, если она не существует
#     os.makedirs(os.path.dirname(filepath), exist_ok=True)
#     # Открываем файл для записи с кодировкой utf-8
#     with open(filepath, 'w', encoding='utf-8') as f:
#         for text in texts:
#             f.write(text.strip())
#
# def dd():
#     # проверка на 200
#     return None
#
#
# # def prepare_environment(base_path=''):
# #     if base_path.exists():
# #         shutil.rmtree(base_path.parent)
# #         base_path.parent.mkdir()
# #         base_path.mkdir()
# #     else:
# #         base_path.parent.mkdir()
# #         base_path.mkdir()
#
#
# def main():
#     all_texts = []
#     for seed_url in seed:
#         print(f"\nОбработка начального URL: {seed_url}")
#         authors= retrieve_authors_urls(seed_url)
#         print(f"Найдено авторов: {len(authors)}")
#         auth_check = authors[:3]
#         print(f'Новое количество: {len(auth_check)}')
#
#         # for author in auth_check:
#         #     text_urls = retrieve_texts_urls(author)
#
#         for i, author_url in enumerate(auth_check):
#             text_urls = retrieve_texts_urls(author_url)
#             print(f"{i} Автор: {author_url}, найдено текстов: {len(text_urls)}")
#
#
#             for text_url in text_urls:
#                 text = get_text(text_url)
#                 if text:  # Добавляем только непустые тексты
#                     all_texts.append(text)
#                     print(f"Обработана страница: {text_url}")
#
#     save_texts_to_file(all_texts, "./texts/collected_literary_texts.txt")
#     print(f"Всего собрано текстов: {len(all_texts)}")
#
#     # author_url = 'http://az.lib.ru/a/andreew_l_n/'
#     # print(retrieve_texts_urls(author_url))
#     #
#     # seed_url = 'http://az.lib.ru/rating/litarea/index_3.shtml'
#     # print(retrieve_authors_urls(seed_url))
#
#
# if __name__ == '__main__':
#     main()
