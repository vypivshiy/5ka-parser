# 5ka-parser
Парсер каталога товаров из сети супермаркетов Пятёрочка. Определяет ближайший супермаркет на основе ip адреса.

__С ip адресом отличным от RU работать не будет__

## Этот скрипт предоставляется "как есть", issue и pull request будут игнорироваться

# Requirements
requests

# Установка

```
git clone https://github.com/vypivshiy/5ka-parser
cd 5ka-parser
python3 main.py
```

# Ключи запуска
  -h, --help Вывести все доступные команды

  -st STORE_ID, --store-id STORE_ID ID магазина, откуда нужно достать каталог товаров. 
  По умолчанию определяет по IP адресу. В скрипт не входит ID всех супермаркетов данной сети.
 
 -o {csv,json}, --out {csv,json} Тип вывода данных. По умолчанию csv

  -n NAME, --name NAME  Имя файла (**без указания расширения**). По умолчанию out.{-o}

  -ow, --overwrite - Удалить старый файл и перезаписать. По умолчанию False

  -s, --split - Разбивка категорий товаров на отдельные файлы. Игнорирует флаг -n. По умолчанию False

  -d DELAY, --delay DELAY Задержка запросов. По умолчанию 1.0

# Пример вывода в csv
```csv
plu,name,image_small,prices.price_regular,prices.price_discount,prices.discount,promo.date_begin,promo.date_end,promo.mech,is_new,uom,step,average_rating,rates_count_in_period
3505362,Яйцо с игрушкой-сюрпризом Kinder Joy 20г,https://photos.okolo.app/product/1177262-main/320x320.jpeg,138.99,,,,,,False,шт,1.0,4.89,9515
3490518,Шоколад Ritter Sport Темный Цельный лесной орех 100г,https://photos.okolo.app/product/1176237-main/320x320.jpeg,122.99,,,,,,False,шт,1.0,4.91,4028
3490515,Шоколад Ritter Sport Молочный Цельный лесной орех 100г,https://photos.okolo.app/product/1176235-main/320x320.jpeg,122.99,,,,,,False,шт,1.0,4.94,28997
...
```
## Распространяется по лицензии MIT
