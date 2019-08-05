import requests, re
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
        return '0.3 м'
    if name.find(" 1 м ") >= 1:
        return '1 м'
    if name.find(" 0,5 м ") >= 1:
        return '0.5 м'


def truba(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")

        value = soup.find('span', class_="autocalc-product-price").text
        money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        img = soup.find_all('a', class_='thumbnail')
        article = soup.find('div', class_="info-inline").find('span').text

        name = soup.find('h1').text
        diametr = name.split('D')[1][:4]

        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = edit(text[0].text)

        strk = '<offer id=' + '"' + str(article + "00") + '"' + ' available="true">' + '\n\
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
                <param name="Тип">Комплектующие к дымоходам</param>\n' \
                + '<param name="Количество труб">1</param>\n' \
                + '<param name="Диаметр труб">' + str(diametr)[1:] + ' мм' + '</param>\n' \
                + '<param name="Длина">' + f_dlina(name) + '</param>\n' \
                                                           '<param name="Производитель">Фабрика ZIG</param>\n\
                                                           <param name="Страна-производитель товара">Украина</param>\n\
                                                           </offer>\n\n'
        write_text(strk2)
        print(strk2)


def otvod(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")

        value = soup.find('span', class_="autocalc-product-price").text
        money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        try:
            img = soup.find_all('a', class_='thumbnail')
        except:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        name = soup.find('h1').text
        diametr = name.split('D')[1][:4]
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = edit(text[0].text)

        strk = '<offer id=' + '"' + str(article + "00") + '"' + ' available="true">' + '\n\
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
        <param name="Тип">Комплектующие к дымоходам</param>\n' \
                + '<param name="Количество труб">1</param>\n' \
                + '<param name="Диаметр труб">' + str(diametr)[1:] + ' мм' + '</param>\n' \
                + '<param name="Производитель">Фабрика ZIG</param>\n\
                <param name="Страна-производитель товара">Украина</param>\n\
                </offer>\n\n'
        write_text(strk2)
        print(strk2)


def truba_dvux_sten(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:

        soup = BeautifulSoup(get_html(i), "lxml")

        value = soup.find('span', class_="autocalc-product-price").text
        money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        try:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')
        except:
            img = soup.find_all('a', class_='main-image thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        name = soup.find('h1').text
        diametr = name.split(' ')[-4][:3]
        print(diametr)
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = edit(text[0].text)

        strk = '<offer id=' + '"' + str(article + "00") + '"' + ' available="true">' + '\n\
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
                <param name="Тип">Комплектующие к дымоходам</param>\n' \
                + '<param name="Количество труб">1</param>\n' \
                + '<param name="Диаметр труб">' + str(diametr) + ' мм' + '</param>\n' \
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

        value = soup.find('span', class_="autocalc-product-price").text
        money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        try:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')
        except:
            img = soup.find_all('a', class_='main-image thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        name = soup.find('h1').text
        diametr = name.split(' ')[-4][:3]
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = edit(text[0].text)

        strk = '<offer id=' + '"' + str(article + "00") + '"' + ' available="true">' + '\n\
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
        <param name="Тип">Комплектующие к дымоходам</param>\n' \
                + '<param name="Количество труб">1</param>\n' \
                + '<param name="Диаметр труб">' + str(diametr) + ' мм' + '</param>\n' \
                + '<param name="Производитель">Фабрика ZIG</param>\n\
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

        value = soup.find('span', class_="autocalc-product-price").text
        money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        try:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')
        except:
            img = soup.find_all('a', class_='main-image thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        name = soup.find('h1').text
        diametr = name.split(' ')[-4][:3]
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = edit(text[0].text)

        strk = '<offer id=' + '"' + str(article + "00") + '"' + ' available="true">' + '\n\
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
        <param name="Тип">Комплектующие к дымоходам</param>\n' \
                + '<param name="Количество труб">1</param>\n' \
                + '<param name="Диаметр труб">' + str(diametr) + ' мм' + '</param>\n' \
                + '<param name="Производитель">Фабрика ZIG</param>\n\
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

        value = soup.find('span', class_="autocalc-product-price").text
        money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        try:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')
        except:
            img = soup.find_all('a', class_='main-image thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        name = soup.find('h1').text
        diametr = name.split(' ')[-4][:3]
        dlina = name.split(' ')
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = edit(text[0].text)

        strk = '<offer id=' + '"' + str(article + "00") + '"' + ' available="true">' + '\n\
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
        <param name="Тип">Комплектующие к дымоходам</param>\n' \
                + '<param name="Количество труб">1</param>\n' \
                + '<param name="Диаметр труб">' + str(diametr) + ' мм' + '</param>\n' \
                + '<param name="Производитель">Фабрика ZIG</param>\n\
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

        value = soup.find('span', class_="autocalc-product-price").text
        money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        try:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')
        except:
            img = soup.find_all('a', class_='main-image thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

        name = soup.find('h1').text
        diametr = name.split(' ')[-4][:3]
        dlina = name.split(' м ')[0]
        text = soup.find('div', class_="tab-pane active").find_all('span')
        index = name.find(" ")
        s1 = name[:index]
        s2 = name[index:]
        company = " Фабрика ZIG"
        name = '<name>' + s1 + company + s2 + ' (' + article + ')' + '</name>'
        description = edit(text[0].text)

        strk = '<offer id=' + '"' + str(article + "00") + '"' + ' available="true">' + '\n\
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
        <param name="Тип">Комплектующие к дымоходам</param>\n' \
                + '<param name="Количество труб">1</param>\n' \
                + '<param name="Диаметр труб">' + str(diametr) + ' мм' + '</param>\n' \
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

        value = soup.find('span', class_="autocalc-product-price").text
        money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        try:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')
        except:
            img = soup.find_all('a', class_='main-image thumbnail')

        article = soup.find('div', class_="info-inline").find('span').text

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

            strk = '<offer id=' + '"' + str(article + "00") + '"' + ' available="true">' + '\n\
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
                    <param name="Тип">Комплектующие к дымоходам</param>\n' \
                    + '<param name="Количество труб">1</param>\n' \
                    + '<param name="Диаметр труб">' + str(diametr) + ' мм' + '</param>\n' \
                    + '<param name="Производитель">Фабрика ZIG</param>\n\
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
    <category id="1">Камины, печи, сауны</category>
    <category id="200" parentId="1">Печи</category>


	<category id="2">Спорт и увлечения</category>
    <category id="3" parentId="2">Активный отдых, туризм и хобби</category>
	<category id="4" parentId="3">Туризм и кемпинг</category>
	<category id="5" parentId="4">Мангалы, барбекю, гриль</category>

    </categories>
    <offers>'''
    print(stroka)
    write_text(stroka)


def main():
    start_log()
    mas = ['https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/truby/?limit=100', \
           'https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/truby/?limit=100&page=2']
    list(map(truba, mas))

    mas2 = ['https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/otvod/?limit=100', \
            'https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/trojniki/?limit=100', \
            'https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/revizii/?limit=100', \
            'https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/regulyatory-tyagi/?limit=100', \
            'https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/elementy-okonchanij/?limit=100&page=1', \
            'https://fabrikazig.com/katalog-produkcii/odnostennye-dymohody/elementy-okonchanij/?limit=100&page=2']
    list(map(otvod, mas2))
    mas3 = ['https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/otvody/?limit=100', \
            'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/otvody/?limit=100&page=2', \
            'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/trojniki-termo/?limit=100', \
            'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/trojniki-termo/?limit=100&page=2', \
            'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/revizii-termo/?limit=100', \
            'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/elementy-okonchanij-termo/?limit=100&filter=74,88,76,86,87', \
            'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/elementy-okonchanij-termo/?filter=74,88,76,86,87&limit=100&page=2']

    list(map(truba_dvux_sten, mas3))

    gribok(
        'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/elementy-okonchanij-termo/gribki-termo/?limit=100')

    truba_dvux_sten_1m('https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/truby-termo/?filter=52&limit=100')
    truba_dvux_sten_0_5m(
        'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/truby-termo/?limit=100&filter=51')
    truba_dvux_sten_0_3m(
        'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/truby-termo/?limit=100&filter=50')

    krepeg('https://fabrikazig.com/krepezhnye-elementy/?limit=100')
    coptilka()
    finish_log()


if __name__ == '__main__':
    main()
