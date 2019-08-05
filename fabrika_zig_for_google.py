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
    f = open('google.xml', 'a', encoding='UTF-8')
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


global number
number = 0


def truba(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:
        global number
        number += 1
        soup = BeautifulSoup(get_html(i), "lxml")

        try:
            value = soup.find('span', class_="autocalc-product-special").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению
        except:
            value = soup.find('span', class_="autocalc-product-price").text
            money = re.findall(pricelookfor, value)  # поиск по регулярному выражению

        img = soup.find_all('a', class_='thumbnail')
        article = soup.find('div', class_="info-inline").find('span').text
        name = soup.find('h1').text
        text = soup.find('div', class_="tab-pane active").find_all('span')

        description = text[0].text
        try:
            nalishie = soup.find('ul', class_="list-unstyled availability").find("span", class_="stock_status_success")
            param_nal='in stock'
        except:
            param_nal='out of stock'



        strk = '<item>\n<g:id>' +  str(article) + '</g:id>' + '\n\
        <title>' + name + '</title>\n\
        <g:description>' + description + '</g:description>' \
               + '\n<link>' + i + '</link>\n\
        <g:image_link>' + str(img[0].get('href')) + '</g:image_link>\n'
        write_text(strk)
        print(strk)
        if len(img)>=2:
            for i in range(1, len(img)):
                print('g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')
                write_text('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')




        strk2 = '<g:availability>' + param_nal + '</g:availability>\n' \
                '<g:price>' + money[0].replace(" ", "") + '.00 UAH' + '</g:price>\n' \
                '\n<g:google_product_category>2792</g:google_product_category>\n\
                <g:brand>Фабрика Зиг</g:brand>\n' \
                + '<g:condition>new</g:condition>\n</item>\n\n'
        write_text(strk2)
        print(strk2)


def otvod(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:
        global number
        number += 1
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
        name = soup.find('h1').text
        text = soup.find('div', class_="tab-pane active").find_all('span')

        description = text[0].text
        try:
            nalishie = soup.find('ul', class_="list-unstyled availability").find("span", class_="stock_status_success")
            param_nal='in stock'
        except:
            param_nal='out of stock'



        strk = '<item>\n<g:id>' +  str(article) + '</g:id>' + '\n\
        <title>' + name + '</title>\n\
        <g:description>' + description + '</g:description>' \
               + '\n<link>' + i + '</link>\n\
        <g:image_link>' + str(img[0].get('href')) + '</g:image_link>\n'
        write_text(strk)
        print(strk)
        if len(img)>=2:
            for i in range(1, len(img)):
                print('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')
                write_text('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')




        strk2 = '<g:availability>' + param_nal + '</g:availability>\n' \
                '<g:price>' + money[0].replace(" ", "") + '.00 UAH' + '</g:price>\n' \
                '\n<g:google_product_category>2792</g:google_product_category>\n\
                <g:brand>Фабрика Зиг</g:brand>\n' \
                + '<g:condition>new</g:condition>\n</item>\n\n'
        write_text(strk2)
        print(strk2)


def truba_dvux_sten(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:
        global number
        number += 1
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
        name = soup.find('h1').text
        text = soup.find('div', class_="tab-pane active").find_all('span')

        description = text[0].text
        try:
            nalishie = soup.find('ul', class_="list-unstyled availability").find("span", class_="stock_status_success")
            param_nal='in stock'
        except:
            param_nal='out of stock'



        strk = '<item>\n<g:id>' +  str(article) + '</g:id>' + '\n\
        <title>' + name + '</title>\n\
        <g:description>' + description + '</g:description>' \
               + '\n<link>' + i + '</link>\n\
        <g:image_link>' + str(img[0].get('href')) + '</g:image_link>\n'
        write_text(strk)
        print(strk)
        if len(img)>=2:
            for i in range(1, len(img)):
                print('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')
                write_text('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')




        strk2 = '<g:availability>' + param_nal + '</g:availability>\n' \
                '<g:price>' + money[0].replace(" ", "") + '.00 UAH' + '</g:price>\n' \
                '\n<g:google_product_category>2792</g:google_product_category>\n\
                <g:brand>Фабрика Зиг</g:brand>\n' \
                + '<g:condition>new</g:condition>\n</item>\n\n'
        write_text(strk2)
        print(strk2)


def truba_dvux_sten_1m(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:
        global number
        number += 1
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
        name = soup.find('h1').text
        text = soup.find('div', class_="tab-pane active").find_all('span')

        description = text[0].text
        try:
            nalishie = soup.find('ul', class_="list-unstyled availability").find("span", class_="stock_status_success")
            param_nal='in stock'
        except:
            param_nal='out of stock'



        strk = '<item>\n<g:id>' +  str(article) + '</g:id>' + '\n\
        <title>' + name + '</title>\n\
        <g:description>' + description + '</g:description>' \
               + '\n<link>' + i + '</link>\n\
        <g:image_link>' + str(img[0].get('href')) + '</g:image_link>\n'
        write_text(strk)
        print(strk)
        if len(img)>=2:
            for i in range(1, len(img)):
                print('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')
                write_text('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')




        strk2 = '<g:availability>' + param_nal + '</g:availability>\n' \
                '<g:price>' + money[0].replace(" ", "") + '.00 UAH' + '</g:price>\n' \
                '\n<g:google_product_category>2792</g:google_product_category>\n\
                <g:brand>Фабрика Зиг</g:brand>\n' \
                + '<g:condition>new</g:condition>\n</item>\n\n'
        write_text(strk2)
        print(strk2)


def truba_dvux_sten_0_5m(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:
        global number
        number += 1
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
        name = soup.find('h1').text
        text = soup.find('div', class_="tab-pane active").find_all('span')

        description = text[0].text
        try:
            nalishie = soup.find('ul', class_="list-unstyled availability").find("span", class_="stock_status_success")
            param_nal='in stock'
        except:
            param_nal='out of stock'



        strk = '<item>\n<g:id>' +  str(article) + '</g:id>' + '\n\
        <title>' + name + '</title>\n\
        <g:description>' + description + '</g:description>' \
               + '\n<link>' + i + '</link>\n\
        <g:image_link>' + str(img[0].get('href')) + '</g:image_link>\n'
        write_text(strk)
        print(strk)
        if len(img)>=2:
            for i in range(1, len(img)):
                print('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')
                write_text('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')




        strk2 = '<g:availability>' + param_nal + '</g:availability>\n' \
                '<g:price>' + money[0].replace(" ", "") + '.00 UAH' + '</g:price>\n' \
                '\n<g:google_product_category>2792</g:google_product_category>\n\
                <g:brand>Фабрика Зиг</g:brand>\n' \
                + '<g:condition>new</g:condition>\n</item>\n\n'
        write_text(strk2)
        print(strk2)


def truba_dvux_sten_0_3m(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:
        global number
        number += 1
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
        name = soup.find('h1').text
        text = soup.find('div', class_="tab-pane active").find_all('span')

        description = text[0].text
        try:
            nalishie = soup.find('ul', class_="list-unstyled availability").find("span", class_="stock_status_success")
            param_nal='in stock'
        except:
            param_nal='out of stock'



        strk = '<item>\n<g:id>' +  str(article) + '</g:id>' + '\n\
        <title>' + name + '</title>\n\
        <g:description>' + description + '</g:description>' \
               + '\n<link>' + i + '</link>\n\
        <g:image_link>' + str(img[0].get('href')) + '</g:image_link>\n'
        write_text(strk)
        print(strk)
        if len(img)>=2:
            for i in range(1, len(img)):
                print('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')
                write_text('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')




        strk2 = '<g:availability>' + param_nal + '</g:availability>\n' \
                '<g:price>' + money[0].replace(" ", "") + '.00 UAH' + '</g:price>\n' \
                '\n<g:google_product_category>2792</g:google_product_category>\n\
                <g:brand>Фабрика Зиг</g:brand>\n' \
                + '<g:condition>new</g:condition>\n</item>\n\n'
        write_text(strk2)
        print(strk2)


def gribok(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:
        global number
        number += 1
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
        name = soup.find('h1').text
        text = soup.find('div', class_="tab-pane active").find_all('span')

        description = text[0].text
        try:
            nalishie = soup.find('ul', class_="list-unstyled availability").find("span", class_="stock_status_success")
            param_nal='in stock'
        except:
            param_nal='out of stock'



        strk = '<item>\n<g:id>' +  str(article) + '</g:id>' + '\n\
        <title>' + name + '</title>\n\
        <g:description>' + description + '</g:description>' \
               + '\n<link>' + i + '</link>\n\
        <g:image_link>' + str(img[0].get('href')) + '</g:image_link>\n'
        write_text(strk)
        print(strk)
        if len(img)>=2:
            for i in range(1, len(img)):
                print('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')
                write_text('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')




        strk2 = '<g:availability>' + param_nal + '</g:availability>\n' \
                '<g:price>' + money[0].replace(" ", "") + '.00 UAH' + '</g:price>\n' \
                '\n<g:google_product_category>2792</g:google_product_category>\n\
                <g:brand>Фабрика Зиг</g:brand>\n' \
                + '<g:condition>new</g:condition>\n</item>\n\n'
        write_text(strk2)
        print(strk2)


def krepeg(URL):
    html = get_html(URL)
    mas = get_ads(html)

    pricelookfor = r"[\d\s]+"
    # write_text = ''
    for i in mas:
        global number
        number += 1
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
        name = soup.find('h1').text
        text = soup.find('div', class_="tab-pane active").find_all('span')

        description = text[0].text
        try:
            nalishie = soup.find('ul', class_="list-unstyled availability").find("span", class_="stock_status_success")
            param_nal='in stock'
        except:
            param_nal='out of stock'



        strk = '<item>\n<g:id>' +  str(article) + '</g:id>' + '\n\
        <title>' + name + '</title>\n\
        <g:description>' + description + '</g:description>' \
               + '\n<link>' + i + '</link>\n\
        <g:image_link>' + str(img[0].get('href')) + '</g:image_link>\n'
        write_text(strk)
        print(strk)
        if len(img)>=2:
            for i in range(1, len(img)):
                print('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')
                write_text('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')


        strk2 = '<g:availability>' + param_nal + '</g:availability>\n' \
                '<g:price>' + money[0].replace(" ", "") + '.00 UAH' + '</g:price>\n' \
                '\n<g:google_product_category>2792</g:google_product_category>\n\
                <g:brand>Фабрика Зиг</g:brand>\n' \
                + '<g:condition>new</g:condition>\n</item>\n\n'
        write_text(strk2)
        print(strk2)

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
            img = soup.find_all('a', class_='thumbnail')
        except:
            img = soup.find('div', class_="image-additional owl-carousel").find_all('a', class_='thumbnail')
        article = soup.find('div', class_="info-inline").find('span').text
        name = soup.find('h1').text
        text = soup.find('div', class_="tab-pane active").find_all('span')

        description = text[0].text
        try:
            nalishie = soup.find('ul', class_="list-unstyled availability").find("span", class_="stock_status_success")
            param_nal='in stock'
        except:
            param_nal='out of stock'



        strk = '<item>\n<g:id>' +  str(article) + '</g:id>' + '\n\
        <title>' + name + '</title>\n\
        <g:description>' + 'Профессиональная электрическая коптильня идеально подходит для копчения мяса, колбасы, сыров\
и рыбы. Работа устройства очень проста и только сводится к заполнению бака в генератор для опилок и установления \
температуры. Коптильня полностью изготавливается из кислотостойкой стали. Правильная температура в приборе \
получается благодаря главному нагревателю 1500 Вт, используя термостат. Момент эксплуатации нагревателя\
сигнализируется контрольной лампой. В устройстве есть 5 полочек и генератор дыма в стандартной комплектации.'\
               + '</g:description>' \
               + '\n<link>' + 'https://fabrikazig.com/smokehouse-tek-50' + '</link>\n\
        <g:image_link>' + str(img[0].get('href')) + '</g:image_link>\n'
        write_text(strk)
        print(strk)
        if len(img)>=2:
            for i in range(1, len(img)):
                if i == 10: break
                print('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')
                write_text('<g:additional_image_link>' + img[i].get('href') + '</g:additional_image_link>\n')


        strk2 = '<g:availability>' + param_nal + '</g:availability>\n' \
                '<g:price>' + money[0].replace(" ", "") + '.00 UAH' + '</g:price>\n' \
                '\n<g:google_product_category>687</g:google_product_category>\n\
                <g:brand>Фабрика Зиг</g:brand>\n' \
                + '<g:condition>new</g:condition>\n</item>\n\n'
        write_text(strk2)
        print(strk2)


    except:
        pass


def finish_log():
    stroka2 = '''

	</channel>
</rss>'''
    write_text(stroka2)
    print(stroka2)

    у = input('Файл готов')


def start_log():
    stroka = '''<?xml version="1.0"?>
<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">
	<channel>
		<title>Фабрика Зиг</title>
		<link>https://fabrikazig.com</link>
		<description>Трубы, крепежные элементы, двухстенные дымоходы, элементы окончаний</description>\n\n'''
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
            'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/revizii-termo/?limit=100',  \
            'https://fabrikazig.com/dvustennye-dymohody/elementy-okonchanij-termo/flyugery-termo/?limit=100',\
            'https://fabrikazig.com/dvustennye-dymohody/elementy-okonchanij-termo/konusy/?limit=100', \
            'https://fabrikazig.com/dvustennye-dymohody/elementy-okonchanij-termo/okonchanie/?limit=100',\
            'https://fabrikazig.com/dvustennye-dymohody/elementy-okonchanij-termo/podstavki-napolnye/?limit=100', \
            'https://fabrikazig.com/dvustennye-dymohody/elementy-okonchanij-termo/podstavka-nastennaya/?limit=100']

    list(map(truba_dvux_sten, mas3))
    #
    gribok(
        'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/elementy-okonchanij-termo/gribki-termo/?limit=100')

    truba_dvux_sten_1m('https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/truby-termo/?filter=52&limit=100')
    truba_dvux_sten_0_5m(
        'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/truby-termo/?limit=100&filter=51')
    truba_dvux_sten_0_3m(
        'https://fabrikazig.com/katalog-produkcii/dvustennye-dymohody/truby-termo/?limit=100&filter=50')

    krepeg('https://fabrikazig.com/katalog-produkcii/krepezhnye-elementy/?limit=100')
    coptilka()
    finish_log()


if __name__ == '__main__':
    main()
