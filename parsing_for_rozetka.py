import time, requests, re
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup


def get_html(URL):
    html = requests.get(URL)
    return html.text


def get_ads(html):
    mas = []
    soup = BeautifulSoup(html, "lxml")
    link = soup.find('div', id="content").find_all('div', class_='product-name')
    for i in link:
        href = i.find('a').get("href")
        mas.append(href)
    return mas


def write_text(text):
    f = open('rozetka.xml', 'a', encoding='UTF-8')
    f.write(text)


def edit(text):
    s = text.replace('&', '&amp;')
    s2 = s.replace('"', '&quot;')
    s3 = s2.replace('«', '&quot;')
    s4 = s3.replace('»', '&quot;')
    s5 = s4.replace('>', '&gt;')
    s6 = s5.replace('<', '&lt;')
    s7 = s6.replace("'", '&apos;')
    return s7


def f_dlina(name):
    if name.find(" 0,3 м ") >= 1:
        return '300'
    if name.find(" 1 м ") >= 1:
        return '1000'
    if name.find(" 0,5 м ") >= 1:
        return '500'

def f_dlina2(name):
    if name.find(" 0,3 м ") >= 1:
        return '<param name="Высота, мм">300</param>\n'
    if name.find(" 1 м ") >= 1:
        return '<param name="Высота, мм">1000</param>\n'
    if name.find(" 0,5 м ")>= 1:
        return '<param name="Высота, мм">500</param>\n'
    else: return " "


def truba(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")
        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению


        img = soup.find_all('a', class_='thumbnail')
        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'
        name = soup.find('h1').text

        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) >1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        diametr = name.split('D')[1][:4]


        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = soup.find('div', class_="readmore").find_all('p')[1].text + '<br><br>' + \
              soup.find('div', class_="readmore").find_all('p')[3].text + '<br><br>' + \
              soup.find('div', class_="readmore").find_all('p')[5].text

        strk = '<offer id=' + '"' + str(article ) + '"' + ' available="true">' + '\n\
<url>' + i + '</url>\n\
<price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
<categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + description + ']]></description>\n' \
                + '<param name="Диаметр, мм">' + str(diametr)[1:] + ' мм' + '</param>\n' \
                + '<param name="Высота, мм">' + f_dlina(name) + '</param>\n' \
                + '<param name="Материал">Нержавеющая сталь</param>\n' \
                + '<param name="Количество стенок">Одностенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Элемент дымохода">Труба</param>\n' \
'<param name="Производитель">Фабрика ZIG</param>\n\
<param name="Страна-производитель товара">Украина</param>\n\
</offer>\n\n'
        write_text(strk2)
        print(strk2)


def angle(text):
    if text.find(" 45 ") >= 1:
        return '45'
    if text.find(" 90 ") >= 1:
        return '90'
    if text.find(" 87 ") >= 1:
        return '87'
    if text.find(" 45° ") >= 1:
        return '45'
    if text.find(" 90° ") >= 1:
        return '90'
    if text.find(" 87° ") >= 1:
        return '87'

def element(text):
    if text.find("Тройник ") >= 1:
        return 'Тройник'
    if text.find("Отвод ") >= 1:
        return 'Отвод'
    if text.find("Ревизия ") >= 1:
        return 'Ревизия'
    if text.find("Регулятор ") >= 1:
        return 'Регулятор тяги'
    if text.find("Грибок ") >= 1:
        return 'Грибок'
    if text.find("Флюгер ") >= 1:
        return 'Флюгер'
    if text.find("Волпер ") >= 1:
        return 'Волпер'
    if text.find("Окончание ") >= 1:
        return 'Окончание'
    if text.find("Переход ") >= 1:
        return 'Переход'
    if text.find("Крыза ") >= 1:
        return 'Крыза'
    if text.find("Окапник ") >= 1:
        return 'Окапник'
    if text.find("Конус ") >= 1:
        return 'Конус'
    if text.find("Подставка ") >= 1:
        return 'Подставка напольная'

    if text.find("Скоба ") >= 1:
        return 'Скоба'
    if text.find("Кольцо ") >= 1:
        return 'Кольцо'
    if text.find("Хомут ") >= 1:
        return 'Хомут'
    if text.find("Лейка ") >= 1:
        return 'Лейка'
    if text.find("Дека ") >= 1:
        return 'Дека'
    if text.find("Розетта ") >= 1:
        return 'Розетта'



def otvod(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")

        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        try:
            img = soup.find_all('a', class_='thumbnail')
        except:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'

        name = soup.find('h1').text
        diametr = name.split('D')[1][:4]
        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) >1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        # description = edit(text[0].text)
        description = soup.find('div', class_="readmore").find_all('p')[2].text + '<br><br>' + \
                      soup.find('div', class_="readmore").find_all('p')[4].text + '<br><br>' + \
                      soup.find('div', class_="readmore").find_all('p')[7].text
        strk = '<offer id=' + '"' + str(article) + '"' + ' available="true">' + '\n\
<url>' + i + '</url>\n\
<price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
<categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + description + ']]></description>\n'\
                + '<param name="Материал">Нержавеющая сталь</param>\n' \
                + '<param name="Количество стенок">Одностенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Диаметр, мм">' + str(diametr)[1:] + '</param>\n' \
                + '<param name="Угол поворота">' + angle(name) + '</param>\n' \
                + '<param name="Элемент дымохода">' + element(name) + '</param>\n' \
                + '<param name="Производитель">Фабрика ZIG</param>\n\
<param name="Страна-производитель товара">Украина</param>\n\
</offer>\n\n'
        write_text(strk2)
        print(strk2)

def revizii(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")

        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        try:
            img = soup.find_all('a', class_='thumbnail')
        except:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'

        name = soup.find('h1').text
        diametr = name.split('D')[1][:4]
        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) > 1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        # description = edit(text[0].text)
        description = soup.find('div', class_="readmore").find_all('p')[2].text + '<br><br>' + \
                      soup.find('div', class_="readmore").find_all('p')[4].text
        strk = '<offer id=' + '"' + str(article) + '"' + ' available="true">' + '\n\
    <url>' + i + '</url>\n\
    <price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
    <categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + description + ']]></description>\n' \
                + '<param name="Материал">Нержавеющая сталь</param>\n' \
                + '<param name="Количество стенок">Одностенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Диаметр, мм">' + str(diametr)[1:] + '</param>\n' \
                + '<param name="Элемент дымохода">' + element(name) + '</param>\n' \
                + '<param name="Производитель">Фабрика ZIG</param>\n\
    <param name="Страна-производитель товара">Украина</param>\n\
    </offer>\n\n'
        write_text(strk2)
        print(strk2)

def elementy_okonchanij(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")

        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        try:
            img = soup.find_all('a', class_='thumbnail')
        except:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'

        name = soup.find('h1').text
        diametr = name.split('D')[1][:4]
        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) > 1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        # description = edit(text[0].text)
        description = soup.find('div', class_="readmore").find_all('p')[2].text + '<br><br>' + \
                      soup.find('div', class_="readmore").find_all('p')[4].text
        strk = '<offer id=' + '"' + str(article) + '"' + ' available="true">' + '\n\
    <url>' + i + '</url>\n\
    <price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
    <categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + description + ']]></description>\n' \
                + '<param name="Материал">Нержавеющая сталь</param>\n' \
                + '<param name="Количество стенок">Одностенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Диаметр, мм">' + str(diametr)[1:] + '</param>\n' \
                + '<param name="Элемент дымохода">' + element(name) + '</param>\n' \
                + '<param name="Производитель">Фабрика ZIG</param>\n\
    <param name="Страна-производитель товара">Украина</param>\n\
    </offer>\n\n'
        write_text(strk2)
        print(strk2)

def volpery(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")

        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        try:
            img = soup.find_all('a', class_='thumbnail')
        except:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'

        name = soup.find('h1').text
        diametr = name.split('D')[1][:4]
        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) > 1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = edit(text[0].text)
        strk = '<offer id=' + '"' + str(article) + '"' + ' available="true">' + '\n\
    <url>' + i + '</url>\n\
    <price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
    <categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + description + ']]></description>\n' \
                + '<param name="Материал">Нержавеющая сталь</param>\n' \
                + '<param name="Количество стенок">Одностенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Диаметр, мм">' + str(diametr)[1:] + '</param>\n' \
                + '<param name="Элемент дымохода">' + element(name) + '</param>\n' \
                + '<param name="Производитель">Фабрика ZIG</param>\n\
    <param name="Страна-производитель товара">Украина</param>\n\
    </offer>\n\n'
        write_text(strk2)
        print(strk2)


def material(text):
    if text.find(" н/н ")>= 1:
        return 'Нержавеющая сталь/Нержавеющая сталь'
    if text.find(" нерж/нерж ")>= 1:
        return 'Нержавеющая сталь/Нержавеющая сталь'
    if text.find(" н/оц ")  >= 1:
        return 'Нержавеющая сталь/Оцинкованная сталь'
    if text.find(" нерж/оцинк ")  >= 1:
        return 'Нержавеющая сталь/Оцинкованная сталь'


def truba_dvux_sten(URL):

    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")

        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        try:
            img = soup.find_all('a', class_='thumbnail')
        except:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'

        name = soup.find('h1').text
        diametr = name.split('/')
        diametr = diametr[0][-3:] + '/' + diametr[1][:3]
        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) > 1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        # description = edit(text[0].text)
        description = soup.find('div', class_="readmore").find_all('p')[2].text + '<br><br>' + \
                      soup.find('div', class_="readmore").find_all('p')[4].text
        strk = '<offer id=' + '"' + str(article) + '"' + ' available="true">' + '\n\
    <url>' + i + '</url>\n\
    <price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
    <categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + description + ']]></description>\n' \
                + '<param name="Материал">' + material(name) + '</param>\n' \
                + '<param name="Количество стенок">Двустенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Угол поворота">' + angle(name) + '</param>\n' \
                + '<param name="Диаметр, мм">' + str(diametr) + '</param>\n' \
                + '<param name="Элемент дымохода">' + element(name) + '</param>\n' \
                + '<param name="Производитель">Фабрика ZIG</param>\n\
    <param name="Страна-производитель товара">Украина</param>\n\
    </offer>\n\n'
        write_text(strk2)
        print(strk2)

def truba_dvux_sten_2(URL):

    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")

        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        try:
            img = soup.find_all('a', class_='thumbnail')
        except:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'

        name = soup.find('h1').text
        diametr = name.split('/')
        diametr = diametr[0][-3:] + '/' + diametr[1][:3]
        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) > 1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = edit(text[0].text)
        # description = soup.find('div', class_="readmore").find_all('p')[2].text + '<br><br>' + \
        #               soup.find('div', class_="readmore").find_all('p')[4].text
        strk = '<offer id=' + '"' + str(article) + '"' + ' available="true">' + '\n\
    <url>' + i + '</url>\n\
    <price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
    <categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + description + ']]></description>\n' \
                + '<param name="Материал">' + material(name) + '</param>\n' \
                + '<param name="Количество стенок">Двустенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Диаметр, мм">' + str(diametr) + '</param>\n' \
                + '<param name="Элемент дымохода">' + element(name) + '</param>\n' \
                + '<param name="Производитель">Фабрика ZIG</param>\n\
    <param name="Страна-производитель товара">Украина</param>\n\
    </offer>\n\n'
        write_text(strk2)
        print(strk2)

def truba_dvux_sten_3(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")

        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        try:
            img = soup.find_all('a', class_='thumbnail')
        except:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'

        name = soup.find('h1').text
        diametr = name.split('/')
        diametr = diametr[0][-3:] + '/' + diametr[1][:3]
        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) > 1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = edit(text[0].text)
        # description = soup.find('div', class_="readmore").find_all('p')[2].text + '<br><br>' + \
        #               soup.find('div', class_="readmore").find_all('p')[4].text
        strk = '<offer id=' + '"' + str(article) + '"' + ' available="true">' + '\n\
    <url>' + i + '</url>\n\
    <price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
    <categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + description + ']]></description>\n' \
                + '<param name="Материал">' + material(name) + '</param>\n' \
                + '<param name="Количество стенок">Двустенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Диаметр, мм">' + str(diametr) + '</param>\n' \
                + '<param name="Элемент дымохода">Подставка настенная</param>\n' \
                + '<param name="Производитель">Фабрика ZIG</param>\n\
    <param name="Страна-производитель товара">Украина</param>\n\
    </offer>\n\n'
        write_text(strk2)
        print(strk2)




def truba_dvux_sten_1m(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")
        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        img = soup.find_all('a', class_='thumbnail')
        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'
        name = soup.find('h1').text

        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) > 1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        diametr = name.split('/')
        diametr = diametr[0][-3:] + '/' + diametr[1][:3]

        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = soup.find('div', class_="readmore")
        # description = soup.find('div', class_="readmore").find_all('p')[1].text + '<br><br>' + \
        #               soup.find('div', class_="readmore").find_all('p')[3].text + '<br><br>' + \
        #               soup.find('div', class_="readmore").find_all('p')[5].text

        strk = '<offer id=' + '"' + str(article) + '"' + ' available="true">' + '\n\
    <url>' + i + '</url>\n\
    <price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
    <categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + str(description) + ']]></description>\n' \
                + '<param name="Диаметр, мм">' + str(diametr) + ' мм' + '</param>\n' \
                + '<param name="Высота, мм">1000</param>\n'  \
                + '<param name="Материал">' + material(name) + '</param>\n' \
                + '<param name="Количество стенок">Одностенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Элемент дымохода">Труба</param>\n' \
                  '<param name="Производитель">Фабрика ZIG</param>\n\
                  <param name="Страна-производитель товара">Украина</param>\n\
                  </offer>\n\n'
        write_text(strk2)
        print(strk2)


def truba_dvux_sten_0_5m(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")
        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        img = soup.find_all('a', class_='thumbnail')
        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'
        name = soup.find('h1').text

        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) > 1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        diametr = name.split('/')
        diametr = diametr[0][-3:] + '/' + diametr[1][:3]

        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = soup.find('div', class_="readmore")
        # description = soup.find('div', class_="readmore").find_all('p')[1].text + '<br><br>' + \
        #               soup.find('div', class_="readmore").find_all('p')[3].text + '<br><br>' + \
        #               soup.find('div', class_="readmore").find_all('p')[5].text

        strk = '<offer id=' + '"' + str(article) + '"' + ' available="true">' + '\n\
    <url>' + i + '</url>\n\
    <price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
    <categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + str(description) + ']]></description>\n' \
                + '<param name="Диаметр, мм">' + str(diametr) + ' мм' + '</param>\n' \
                + '<param name="Высота, мм">500</param>\n'  \
                + '<param name="Материал">' + material(name) + '</param>\n' \
                + '<param name="Количество стенок">Одностенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Элемент дымохода">Труба</param>\n' \
                  '<param name="Производитель">Фабрика ZIG</param>\n\
                  <param name="Страна-производитель товара">Украина</param>\n\
                  </offer>\n\n'
        write_text(strk2)
        print(strk2)


def truba_dvux_sten_0_3m(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")
        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        img = soup.find_all('a', class_='thumbnail')
        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'
        name = soup.find('h1').text

        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) > 1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        diametr = name.split('/')
        diametr = diametr[0][-3:] + '/' + diametr[1][:3]

        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = soup.find('div', class_="readmore")
        # description = soup.find('div', class_="readmore").find_all('p')[1].text + '<br><br>' + \
        #               soup.find('div', class_="readmore").find_all('p')[3].text + '<br><br>' + \
        #               soup.find('div', class_="readmore").find_all('p')[5].text

        strk = '<offer id=' + '"' + str(article) + '"' + ' available="true">' + '\n\
    <url>' + i + '</url>\n\
    <price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
    <categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + str(description) + ']]></description>\n' \
                + '<param name="Диаметр, мм">' + str(diametr) + ' мм' + '</param>\n' \
                + '<param name="Высота, мм">300</param>\n'  \
                + '<param name="Материал">' + material(name) + '</param>\n' \
                + '<param name="Количество стенок">Одностенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Элемент дымохода">Труба</param>\n' \
                  '<param name="Производитель">Фабрика ZIG</param>\n\
                  <param name="Страна-производитель товара">Украина</param>\n\
                  </offer>\n\n'
        write_text(strk2)
        print(strk2)


def gribok(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")

        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        try:
            img = soup.find_all('a', class_='thumbnail')
        except:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'

        name = soup.find('h1').text
        diametr = name.split('/')
        diametr = diametr[0][-3:] + '/' + diametr[1][:3]
        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) > 1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = edit(text[0].text)
        # description = soup.find('div', class_="readmore").find_all('p')[2].text + '<br><br>' + \
        #               soup.find('div', class_="readmore").find_all('p')[4].text
        strk = '<offer id=' + '"' + str(article) + '"' + ' available="true">' + '\n\
    <url>' + i + '</url>\n\
    <price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
    <categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + description + ']]></description>\n' \
                + '<param name="Материал">' + material(name) + '</param>\n' \
                + '<param name="Количество стенок">Двустенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Диаметр, мм">' + str(diametr) + '</param>\n' \
                + '<param name="Элемент дымохода">Подставка настенная</param>\n' \
                + '<param name="Производитель">Фабрика ZIG</param>\n\
    <param name="Страна-производитель товара">Украина</param>\n\
    </offer>\n\n'
        write_text(strk2)
        print(strk2)


def krepeg(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")

        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        try:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')
        except:
            img = soup.find_all('a', class_='main-image thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'

        name = soup.find('h1').text
        try:
            diametr = name.split('D')[1][1:4]
            dlina = name.split(' м ')[0]
            text = soup.find('div', class_="tab-pane active").find_all('span')
            index = name.find(" ")
            s1 = name[:index]
            s2 = name[index:]
            company = " Фабрика ZIG"
            name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
            description = edit(text[0].text)

            strk = '<offer id=' + '"' + str(article ) + '"' + ' available="true">' + '\n\
<url>' + i + '</url>\n\
<price>' + money[0].replace(" ", "") + '</price>' \
                   + '\n<currencyId>UAH</currencyId>\n\
                    <categoryId>200</categoryId>\n'
            write_text(strk)
            print(strk)

            for i in img:
                print('<picture>' + i.get('href') + '</picture>\n')
                write_text('<picture>' + i.get('href') + '</picture>\n')

            strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                    '<stock_quantity>1000</stock_quantity>\n' \
                    + name + \
                    '\n<description><![CDATA[' + description + ']]></description>\n\
                    <param name="Диаметр труб">' + str(diametr) + ' мм' + '</param>\n' \
                    + '<param name="Производитель">Фабрика ZIG</param>\n' \
                    + '<param name="Элемент дымохода">' + element(name) + '</param>\n\
                    <param name="Страна-производитель товара">Украина</param>\n\
                    </offer>\n\n'
            write_text(strk2)
            print(strk2)
        except:
            pass


def coptilka():
    try:
        pricelookfor = r"[\d\s]+"
        soup = BeautifulSoup(get_html('https://fabrikazig.com/smokehouse-tek-50'), "lxml")

        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        try:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')
        except:
            img = soup.find_all('a', class_='main-image thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        name = soup.find('h1').text

        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"

        strk = '<offer id=' + '"154800"' + ' available="true">' + '\n\
<url>' + 'https://fabrikazig.com/smokehouse-tek-50' + '</url>\n\
<price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
        <categoryId>5</categoryId>\n'
        write_text(strk)
        print(strk)
        t = 0
        for i in img:
            t += 1
            if t == 8: break
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')
        strk2 = '''<vendor>Фабрика ZIG</vendor>
<stock_quantity>1000</stock_quantity>
<name>Коптильня электрическая для горячего копчения ПЭК-50 Фабрика ZIG (1548)</name>
<description><![CDATA[<b>Профессиональная электрическая коптильня</b> идеально подходит для копчения мяса, колбасы, 
сыров и рыбы. Работа устройства очень проста и только сводится к заполнению бака в генератор для опилок и установления 
температуры. Коптильня полностью изготавливается из кислотостойкой стали. Правильная температура в приборе получается
благодаря главному нагревателю 1500 Вт, используя термостат. Момент эксплуатации нагревателя сигнализируется контрольной 
лампой.<p>В устройстве есть 5 полочек и генератор дыма в стандартной комплектации.</p><b>Стандартное оборудование:
</b>внешний изделие - из нержавеющей стали; внутренний корпус - из кислотостойкой нержавеющей стали; распашные двери с
шарниром на правой стороне; 5 полок; 4 деревянных трубок для подвешивания для копчения; нижняя решетка с поддоном для 
жира;генератор дыма; лоток для деревянных опилок; контрольная лампа для главного нагревателя; термостат; сигнализирующая
лампа.<p><b>Преимущества:</b></p><li> простая эксплуатация;</li><li> чистота в работе;</li><li> регулирование
температуры;</li><li> экономное рациональное копчения</li><li> безопасная конструкция;</li><li> небольшое
потребление электроэнергии;</li><p><b>Назначение електрокоптильни:</b></p><li>Для малых, средних и крупных пищевых
предприятий. (Загрузка до 50кг).</li><li>(Рестораны, бары, производители мясной продукции).</li>]]></description>
<param name="Вид">Коптильня</param>
<param name="Производитель">Фабрика ZIG</param>
<param name="Страна-производитель товара">Украина</param>
<param name="Продавец">Другие продавцы</param>
<param name="Тип топлива">Электрические</param>
</offer>'''
        print(strk2)
        write_text(strk2)
    except:
        pass


def radiator(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")
        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        img = soup.find_all('a', class_='thumbnail')
        article = soup.find('div', class_="info-inline").find('span').text

        if masid.get(int(article)):
            print('ключ найден')
            article = str(masid.get(int(article)))
        else:
            print('ключ не найден', article)
            article = str(article) + '00'
        name = soup.find('h1').text

        mas_thickness = name.split(' ')[-2]
        mas_thickness = mas_thickness.split(',')
        if len(mas_thickness) > 1:
            mas_thickness = mas_thickness[0] + '.' + mas_thickness[1]
        else:
            mas_thickness = mas_thickness[0]
        diametr = name.split('D')[1][1:4]

        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = soup.find('div', class_="readmore")
        # description = soup.find('div', class_="readmore").find_all('p')[1].text + '<br><br>' + \
        #               soup.find('div', class_="readmore").find_all('p')[3].text + '<br><br>' + \
        #               soup.find('div', class_="readmore").find_all('p')[5].text

        strk = '<offer id=' + '"' + str(article) + '"' + ' available="true">' + '\n\
        <url>' + i + '</url>\n\
        <price>' + money[0].replace(" ", "") + '</price>' \
               + '\n<currencyId>UAH</currencyId>\n\
        <categoryId>200</categoryId>\n'
        write_text(strk)
        print(strk)

        for i in img:
            print('<picture>' + i.get('href') + '</picture>\n')
            write_text('<picture>' + i.get('href') + '</picture>\n')

        strk2 = '<vendor>Фабрика ZIG</vendor>\n' \
                '<stock_quantity>1000</stock_quantity>\n' \
                + name + \
                '\n<description><![CDATA[' + str(description) + ']]></description>\n' \
                + '<param name="Диаметр, мм">' + diametr + '</param>\n' \
                + '<param name="Высота, мм">' + f_dlina(name) + '</param>\n' \
                + '<param name="Количество стенок">Одностенные</param>\n' \
                + '<param name="Толщина, мм">' + mas_thickness + '</param>\n' \
                + '<param name="Элемент дымохода">Труба</param>\n' \
                  '<param name="Производитель">Фабрика ZIG</param>\n\
                  <param name="Страна-производитель товара">Украина</param>\n\
                  </offer>\n\n'
        write_text(strk2)
        print(strk2)

def finish_log():
    stroka = '\n</offers>\n</shop>\n</yml_catalog>'
    print(stroka)
    write_text(stroka)

    у = input('Файл готов')


def start_log():
    stroka = '''<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE yml_catalog SYSTEM "shops.dtd">
    <yml_catalog date="2018-04-16 12:00">
    <shop>
    <name>fabrikazig</name>
    <company>Фабрика ZIG</company>
    <url>https://fabrikazig.com/</url>
    <currencies>
    <currency id="UAH" rate="1"/>
    </currencies>
    <categories>
    <category id="1">Товары для дома</category>
    <category id="7" parentId="1">Камины, печи, сауны</category>
    <category id="200" parentId="7">Дымоходы</category>

	<category id="2">Спорт и увлечения</category>
    <category id="3" parentId="2">Активный отдых, туризм и хобби</category>
	<category id="4" parentId="3">Туризм и кемпинг</category>
	<category id="5" parentId="4">Мангалы, барбекю, гриль</category>
	
    </categories>
    <offers>\n\n'''
    print(stroka)
    write_text(stroka)


def editXML(filename):
    tree = ET.ElementTree(file=filename)
    root = tree.getroot()

    for url, ofr_id in  zip(root.iter("url"), root.iter('offer')):
        yield {ofr_id.attrib.get('id'): url.text}


def main():
    start_log()
    mas = ['https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/truby/?limit=100', \
           'https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/truby/?limit=100&page=2']
    list(map(truba, mas))

    mas2 = ['https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/trojniki/?limit=100', \
            'https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/otvod/?limit=100']
    list(map(otvod, mas2))

    mas2_2 = ['https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/regulyatory-tyagi/?limit=100', \
            'https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/revizii/?limit=100']
    list(map(revizii, mas2_2))

    mas2_3 = ['https://fabrikazig.com/odnostennye-dymohody/elementy-okonchanij/okapniki/?limit=100', \
              'https://fabrikazig.com/odnostennye-dymohody/elementy-okonchanij/kryzy/?limit=100', \
              'https://fabrikazig.com/odnostennye-dymohody/elementy-okonchanij/perehody/?limit=100', \
              'https://fabrikazig.com/odnostennye-dymohody/elementy-okonchanij/volpery/?limit=100', \
              'https://fabrikazig.com/odnostennye-dymohody/elementy-okonchanij/flyugery/?limit=100', \
              'https://fabrikazig.com/odnostennye-dymohody/elementy-okonchanij/gribki/?limit=100']
    list(map(elementy_okonchanij, mas2_3))

    volpery('https://fabrikazig.com/odnostennye-dymohody/elementy-okonchanij/okonchaniya/?limit=100')



    mas3 = ['https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/trojniki-termo/?limit=100', \
            'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/trojniki-termo/?limit=100&page=2', \
             'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/otvody/?limit=100', \
            'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/otvody/?limit=100&page=2' ]
    list(map(truba_dvux_sten, mas3))

    mas3_1 = ['https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/revizii-termo/?limit=100',  \
              'https://fabrikazig.com/dvustennye-dymohody/elementy-okonchanij-termo/konusy/?limit=100', \
              'https://fabrikazig.com/dvustennye-dymohody/elementy-okonchanij-termo/okonchanie/?limit=100', \
              'https://fabrikazig.com/dvustennye-dymohody/elementy-okonchanij-termo/podstavki-napolnye/?limit=100', \
              'https://fabrikazig.com/dvustennye-dymohody/elementy-okonchanij-termo/flyugery-termo/?limit=100'
              ]
    list(map(truba_dvux_sten_2, mas3_1))

    truba_dvux_sten_3('https://fabrikazig.com/dvustennye-dymohody/elementy-okonchanij-termo/podstavka-nastennaya/?limit=100')

    truba_dvux_sten_2(
        'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/elementy-okonchanij-termo/gribki-termo/?limit=100')

    truba_dvux_sten_1m('https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/truby-termo/?filter=52&limit=100')
    truba_dvux_sten_0_5m(
        'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/truby-termo/?limit=100&filter=51')
    truba_dvux_sten_0_3m(
        'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/truby-termo/?limit=100&filter=50')

    krepeg('https://fabrikazig.com/krepezhnye-elementy/?limit=100')
    radiator('https://fabrikazig.com/dvustennye-dymohody/radiatory/?limit=100')
    coptilka()
    finish_log()


def open_file():
    f = open('mas_id.txt')
    return f.read()


global masid
masid = {}
if __name__ == '__main__':


    # for i in editXML("file.xml"):
    #     print(tuple(i.values())[0])
    #     soup = BeautifulSoup(requests.get(tuple(i.values())[0]).text, "lxml")
    #     article = soup.find('div', class_="info-inline").find('span').text
    #     print({article: tuple(i.keys())[0]})
    #     print("'"+str(article)+"'"+':' +"'"+tuple(i.keys())[0]+"'"+', ')
    #     write_text(str(article)+':' +tuple(i.keys())[0]+', ')

    text=open_file().split(',')
    for i in text:
        key_valye=i.split(':')
        masid.update({int(key_valye[0]): key_valye[1]})

    main()