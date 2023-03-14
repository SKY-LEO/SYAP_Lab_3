import string

import PySimpleGUI as sg
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

internal_urls = set()
external_urls = set()

main_menu = ("1. Задание Файлы\n ",
             "2. Задание Парсинг\n ",
             "0. Выход")


class File:
    def __init__(self, filename, filesize, filedate, num_of_access):
        self.filename = filename
        self.filesize = filesize
        self.filedate = filedate
        self.num_of_access = num_of_access


def task1():
    files = [File("text", 100, "14.03.2023", 1), File("laboratory_work", 1000, "01.03.2023", 10),
             File("history", 10, "11.03.2023", 5)]
    layout = [
        [sg.Text("Sort Files By:")],
        [sg.Checkbox("Alphabet", enable_events=True, key="alphabet")],
        [sg.Checkbox("Size", enable_events=True, key="size"), sg.InputText(key="file_size")],
        [sg.Checkbox("Number of access", enable_events=True, key="num_of_access"),
         sg.InputText(key="file_num_of_access")],
        [sg.Output(size=(100, 20), key="output")],
        [sg.Button("Exit")]
    ]  # определение компонентов, которые будут отображаться на сцене
    window = sg.Window('Files', layout)  # создание окна
    while True:
        event, values = window.read()  # получение данных о событиях и значениях объектов на сцене
        sorted_files = files
        window["output"].update(value="")
        if event in (sg.WIN_CLOSED, "Exit"): break
        if event == "alphabet":  # если сработало событие
            if window["alphabet"]:  # если значение чекбокса alphabet равно True
                window["size"].update(value=False)  # очищаем возможные галочки в других чекбоксах
                window["num_of_access"].update(value=False)  # очищаем возможные галочки в других чекбоксах
                sorted_files = sorted(files, key=lambda x: x.filename)  # сортировка
        if event == "size":
            if values["size"]:
                window["alphabet"].update(value=False)
                window["num_of_access"].update(value=False)
                sorted_files = filter(lambda x: x.filesize > int(values["file_size"]), files)
                sorted_files = sorted(sorted_files, key=lambda x: x.filesize)
        if event == "num_of_access":
            if values["num_of_access"]:
                window["alphabet"].update(value=False)
                window["size"].update(value=False)
                sorted_files = filter(lambda x: x.num_of_access > int(values["file_num_of_access"]), files)
                sorted_files = sorted(sorted_files, key=lambda x: x.num_of_access)
        for file in sorted_files:
            print(file.filename, file.filesize, file.filedate, file.num_of_access)
    window.close()


def is_valid(url):
    """
    Проверяет, является ли 'url' действительным URL
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def crawl(url, headers):
    """
    Сканирует веб-страницу и извлекает все ссылки.
    Вы найдете все ссылки в глобальных переменных набора external_urls и internal_urls.
    """
    print(f"[*] Проверена ссылка: {url}")
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href пустой тег
            continue
        # присоединяемся к URL, если он относительный (не абсолютная ссылка)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # удалить GET-параметры URL, фрагменты URL и т. д.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # недействительный URL
            continue
        if href in internal_urls:
            # уже в наборе
            continue
        if domain_name not in href:
            # внешняя ссылка
            if href not in external_urls:
                print(f"[!] Внешняя ссылка: {href}")
                external_urls.add(href)
            continue
        print(f"[*] Внутренняя ссылка: {href}")
        internal_urls.add(href)


def task2():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'DNT': '1'
    }
    url = "https://vk.com/sky_leo"
    url = "https://onliner.by"
    url = "https://bsuir.by"
    url = "https://belta.by"
    crawl(url, headers)
    print("[+] Итого внутренних ссылок:", len(internal_urls))
    print("[+] Итого внешних ссылок:", len(external_urls))
    print("[+] Итого URL:", len(external_urls) + len(internal_urls))
    domain_name = urlparse(url).netloc
    # сохраняем внутренние ссылки в файл
    with open(f"{domain_name}_internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)
    # сохраняем внешние ссылки в файл
    with open(f"{domain_name}_external_links.txt", "w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)

    soup = BeautifulSoup(requests.get(url, headers=headers).text, 'lxml')
    text = soup.getText().lower()
    gg = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~1234567890«–»"""
    for character in gg:
        text = text.replace(character, ' ')

    # text1 = text.translate(str.maketrans('', '', string.punctuation))
    text = text.split()
    # text = text.replace(string.punctuation, '')
    print(text)
    print(len(text))
    # print(text1)


def menu():
    while True:
        print("Список заданий:\n", "".join(main_menu))
        variant = input("Выберите задание: ")
        try:
            variant = int(variant)
        except ValueError:
            print("Введите целочисленное число!")
            continue
        if variant > len(main_menu) - 1 or variant < 0:
            print("Ошибка, введите число в заданном интервале!")
        else:
            match variant:
                case 1:
                    task1()
                case 2:
                    task2()
                case 0:
                    break
                case _:
                    print("Ошибка!")
                    return -1
    return 0


if __name__ == '__main__':
    menu()
