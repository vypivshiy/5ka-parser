import argparse
from collections.abc import MutableMapping
import csv
import json
from os.path import exists
from os import remove
from time import time, sleep
from typing import Union, Optional, Tuple, List

import requests


def _flatten_dict_gen(d, parent_key, sep):
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, sep=sep).items()
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '.') -> dict:
    return dict(_flatten_dict_gen(d, parent_key, sep))


class Parser:
    CATEGORIES = {"Шоколад_и_батончики": 1025,
                  "Драже": 1029,
                  "Мармелад_и_карамель": 1030,
                  "Кофе_3_в_1": 1034,
                  "Батарейки_и_лампочки": 1026,
                  "Аксессуары_для_телефонов": 1027,
                  "Молоко": 702,
                  "Яйца": 701,
                  "Сыр": 699,
                  "Йогурты": 705,
                  "Сливочное_масло_и_маргарин": 714,
                  "Сметана": 709,
                  "Творог": 711,
                  "Кефир,_кисломолочные_продукты": 707,
                  "Глазированные_сырки": 710,
                  "Десерты_и_коктейли": 704,
                  "Сгущённое_молоко": 715,
                  "Сливки": 712,
                  "Зелень,_салаты,_лук_и_чеснок": 834,
                  "Грибы": 846,
                  "Фрукты": 934,
                  "Ягоды_и_виноград": 848,
                  "Орехи,_сухофрукты_и_семечки": 871,
                  "Хлеб": 895,
                  "Пироги,_пирожки,_выпечка,_бисквиты": 892,
                  "Хлебцы": 900,
                  "Соломка,_крекеры,_хлебные_палочки": 896,
                  "Сухари": 894,
                  "Сушки,_баранки,_бублики": 897,
                  "Сухарики": 899,
                  "Сэндвичи_и_завтраки": 988,
                  "Супы_и_основные_блюда": 989,
                  "Салаты_и_закуски": 990,
                  "Тесто,_лапша,_пицца": 991,
                  "Птица": 729,
                  "Говядина": 721,
                  "Свинина": 723,
                  "Фарш": 726,
                  "Замороженное_мясо_и_птица": 611,
                  "Готовые_мясные_изделия": 487,
                  "Субпродукты_из_мяса_и_птицы": 724,
                  "Баранина": 720,
                  "Деликатесы_и_копчености": 717,
                  "Колбаса": 630,
                  "Мясные_деликатесы_и_заливное": 629,
                  "Сосиски,_сардельки,_шпикачки": 635,
                  "Пельмени": 608,
                  "Котлеты_и_наггетсы": 607,
                  "Блины": 604,
                  "Вареники_и_сырники": 605,
                  "Готовые_блюда": 606,
                  "Мороженое": 613,
                  "Овощи": 531,
                  "Пицца": 609,
                  "Тесто": 610,
                  "Ягоды": 603,
                  "Икра": 801,
                  "Крабовое_мясо_и_палочки": 809,
                  "Морепродукты": 810,
                  "Рыбные_закуски": 808,
                  "Соленая_рыба": 813,
                  "Сушеная_и_вяленая_рыба": 811,
                  "Замороженная_рыба_и_морепродукты": 615,
                  "Копченая_рыба": 812,
                  "Макароны": 920,
                  "Крупы": 921,
                  "Для_выпечки_и_кулинарии": 519,
                  "Соль": 987,
                  "Сахар_и_заменители": 521,
                  "Масло_растительное": 930,
                  "Майонез": 950,
                  "Соусы_и_заправки": 928,
                  "Специи_и_приправы": 931,
                  "Продукты_быстрого_приготовления": 926,
                  "Сухие_завтраки_и_мюсли": 876,
                  "Диетические_продукты": 913,
                  "Уксус_и_маринад": 932,
                  "Чипсы": 1018,
                  "Сухарики_и_гренки": 1022,
                  "Сушеная_рыба": 1021,
                  "Мясные_снеки": 1020,
                  "Попкорн_и_кукурузные_снеки": 1019,
                  "Семечки": 1041,
                  "Полезные_снеки": 1023,
                  "Варенье,_джем,_мед": 660,
                  "Восточные_сладости,_халва": 868,
                  "Зефир,_мармелад,_пастила": 869,
                  "Торты,_кексы,_рулеты_и_пирожные": 866,
                  "Шоколад_и_шоколадные_изделия": 858,
                  "Шоколадные_пасты": 859,
                  "Конфеты_и_наборы_конфет": 856,
                  "Круассаны": 863,
                  "Печенье,_пряники,_вафли": 860,
                  "Жевательная_резинка": 855,
                  "Кофе_в_зёрнах": 904,
                  "Растворимый_кофе": 907,
                  "Молотый_кофе": 906,
                  "Кофе_в_капсулах": 905,
                  "Чёрный_чай": 912,
                  "Зелёный_чай": 910,
                  "Травяной_чай": 908,
                  "Фруктовый_чай": 911,
                  "Чай_ассорти": 909,
                  "Какао_и_шоколад": 903,
                  "Цикорий": 1017,
                  "Вода": 737,
                  "Сладкая_газированная_вода": 740,
                  "Соки_и_нектары": 741,
                  "Холодный_чай": 742,
                  "Квас": 738,
                  "Морсы": 739,
                  "Растворимые_напитки": 733,
                  "Безалкогольное_пиво_и_вино": 736,
                  "Овощные_консервы": 642,
                  "Рыбные_консервы": 646,
                  "Мясные_консервы": 638,
                  "Горошек_и_кукуруза": 641,
                  "Фасоль": 645,
                  "Маслины_и_оливки": 643,
                  "Соленья": 1015,
                  "Фруктово-ягодные_консервы": 659,
                  "Детское_питание": 936,
                  "Подгузники_и_салфетки": 524,
                  "Купание_и_уход_за_кожей": 525,
                  "Товары_для_школы": 923,
                  "Для_новорождённых_и_мам": 529,
                  "Игры_и_игрушки": 528,
                  "Влажный_корм_для_собак": 581,
                  "Влажный_корм_для_кошек": 580,
                  "Товары_для_собак": 584,
                  "Товары_для_кошек": 583,
                  "Туалетная_бумага": 666,
                  "Бумажные_полотенца_и_салфетки": 665,
                  "Гигиена_рта": 676,
                  "Средства_для_душа": 664,
                  "Средства_для_волос": 668,
                  "Уход_за_кожей": 669,
                  "Бритвенные_станки_и_кассеты": 674,
                  "Ватные_диски_и_палочки": 667,
                  "Дезодоранты": 671,
                  "Другие_косметические_средства": 670,
                  "Подарочные_наборы": 672,
                  "Наборы_и_аксессуары": 663,
                  "Презервативы_и_гели": 679,
                  "Прокладки_и_тампоны": 677,
                  "Средства_для_бритья": 675,
                  "Подгузники_для_взрослых": 678,
                  "Маски": 1037,
                  "Антисептики": 1038,
                  "Антибактериальное_мыло": 1039,
                  "Антибактериальные_салфетки": 1040,
                  "Для_уборки": 546,
                  "Для_стирки": 573,
                  "Для_мытья_посуды": 568,
                  "Автотовары": 914,
                  "Ароматизаторы": 574,
                  "Бытовая_техника": 992,
                  "Бытовые_принадлежности": 543,
                  "Декор_для_дома": 548,
                  "Для_мебели_и_ковров": 569,
                  "Для_отдыха": 917,
                  "Для_посудомоечной_машины": 567,
                  "Для_приготовления_и_хранения": 566,
                  "Для_стекол_и_зеркал": 565,
                  "Кухонная_посуда": 563,
                  "Мешки_для_мусора": 561,
                  "Одежда_и_аксессуары": 924,
                  "Одноразовая_посуда": 560,
                  "Пакеты": 549,
                  "Пятновыводители": 559,
                  "Сад": 922,
                  "Сервировочная_посуда": 544,
                  "Средства_для_ухода_за_бельем_и_одеждой": 558,
                  "Средства_от_насекомых_и_грызунов": 557,
                  "Товары_для_ванной": 545,
                  "Товары_для_ремонта": 550,
                  "Уход_за_обувью": 553,
                  "Хранение_одежды": 547,
                  "Чистящие_средства": 551,
                  "Чистящие_средства_для_ванной_и_туалета": 571,
                  "Чистящие_средства_для_кухни": 570,
                  "Цветы_горшечные_и_срезанные": 556, }

    HEADERS = {"User-Agent":
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.105 "
                   "Safari/537.36",
               "Referer": "https://5ka.ru/rating/catalogue",
               "Sec-Fetch-Mode": "cors",
               "Accept": "application/json, text/plain, */*"}
    URL = "https://5ka.ru/api/v1/"
    DELAY = 1.0

    def __init__(self, default_store_id: Optional[Union[int, str]] = None):
        """

        :param default_store_id: ID магазина пятёрочки.
        По умолчанию вытаскивает автоматически на основе геолокации IP адреса
        """
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

        # определяет автоматически ближайший магазин по ip адресу запроса
        if not default_store_id:
            default_store_id = self.get_default_store_id

        self.session.headers.update({"X-User-Store": str(default_store_id)})

    def request(self, method: str, **kwargs) -> requests.Response:
        sleep(self.DELAY)
        return self.session.get(self.URL + method, **kwargs)

    def get_products(self,
                     category_id: Union[int, str],
                     *,
                     limit: int = 100,  # max 100
                     offset: int = 0,
                     rates_count_from: int = 30,
                     is_promo: bool = False,
                     rating_order: Optional[str] = "") -> dict:
        """
        :param rating_order:
        :param category_id: категория товара
        :param limit: кол-во объектов в json. Максимальное значение - 100
        :param offset: отступ
        :param rates_count_from:
        :param is_promo: по акции товар. По умолчанию False
        :return:

        item example:
            {
                "plu": 4000341,
                "name": "Продукт творожный Даниссимо Тропический манго и маракуйя 5.6% 130г",
                "image_small": "https://photos.okolo.app/product/1199737-main/320x320.jpeg",
                "prices": {
                    "price_regular": "64.99",
                    "price_discount": null,
                    "discount": null
                    },
                "promo": {
                    "date_begin": null,
                    "date_end": null,
                    "mech": null
            },
                "is_new": false,
                "uom": "шт",
                "step": "1.0",
                "average_rating": 4.92,
                "rates_count_in_period": 13683
    }
        """
        if limit > 100:
            limit = 100

        params = {"limit": limit, "offset": offset, "rates_count_from": rates_count_from,
                  "is_promo": is_promo,
                  "category": category_id,
                  "rating_order": rating_order}
        products = self.request("products", params=params)
        return products.json()

    def get_all_products(self) -> Tuple[List[dict], str]:
        for name, category_id in self.CATEGORIES.items():
            offset = 0
            items = []
            while True:
                item = self.get_products(category_id=category_id, offset=offset)["products"]
                if len(item) == 0:
                    break
                items.extend(item)
                offset += 100
            yield items, name

    @property
    def get_default_store_id(self) -> Union[int, str]:
        return self.request("compilation_data").json()["default_store_id"]


class Converter:

    @staticmethod
    def json(name: str, items: List):
        if len(items) == 0:
            return
        cache = []
        if exists(name):
            with open(name, "r") as f:
                cache = json.load(f)
        cache.extend(items)
        with open(name, "w") as f:
            json.dump(cache, f)

    @staticmethod
    def csv(name: str, items: List[dict]):
        if len(items) == 0:
            return
        if not exists(name):
            with open(name, "w") as f:
                writer = csv.writer(f)
                writer.writerow(flatten_dict(items[0]).keys())

        with open(name, "a") as f:
            writer = csv.writer(f)
            for item in items:
                item = flatten_dict(item)
                writer.writerow(item.values())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-st", "--store-id",
                        dest="STORE_ID",
                        type=str,
                        default="",
                        help="ID магазина. По умолчанию определяет по IP адресу")
    parser.add_argument("-o", "--out",
                        dest="OUT",
                        choices=("csv", "json"),
                        default="csv",
                        help="Тип расширения вывода. По умолчанию csv")
    parser.add_argument("-n", "--name",
                        type=str,
                        dest="NAME",
                        default="out",
                        help="Имя файла (без указания расширения). По умолчанию с именем out.{-o}")
    parser.add_argument("-ow", "--overwrite",
                        action="store_true",
                        dest="OVERWRITE",
                        default=False,
                        help="Заново переписать файл. По умолчанию False")
    parser.add_argument("-s", "--split",
                        action="store_true",
                        dest="SPLIT",
                        default=False,
                        help="Разбивка товаров по категориям на отдельные файлы. Игнорирует флаг -n. По умолчанию False")

    parser.add_argument("-d", "--delay",
                        type=float,
                        default=1.0,
                        help="Задержка запросов. По умолчанию 1.0")

    namespace = parser.parse_args()
    store_id_ = namespace.STORE_ID
    filename_ = f'{namespace.NAME}.{namespace.OUT}'

    p = Parser(default_store_id=store_id_)
    start = time()
    if namespace.OVERWRITE and exists(filename_):
        remove(filename_)
    for items_, name_ in p.get_all_products():
        print(name_, "collect", len(items_))
        if namespace.SPLIT:
            if namespace.OUT == "csv":
                Converter.csv(f'{name_}.{namespace.OUT}', items_)
            if namespace.OUT == "json":
                Converter.json(f'{name_}.{namespace.OUT}', items_)
        elif namespace.OUT == "csv":
            Converter.csv(filename_, items_)
        elif namespace.OUT == "json":
            Converter.json(filename_, items_)
    print(f"Done. Elapsed time: {round(time() - start)} seconds")
