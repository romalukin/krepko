import requests
import xlsxwriter
import json
import datetime
from bs4 import BeautifulSoup


def get_catalog(url_link: str) -> dict:
    #get the html of site 
    result = requests.get(url_link)
    src = result.content
    #make the content good to work with beautifulsoup
    soup = BeautifulSoup(src, 'lxml')

    urls = []
    category_list= []

    category = soup.find_all('div', {'class': 'catalog-block'})
    for cat in category:
        urls.append(url_link + str(cat.find('a')['href']).replace('/category/', ''))
        category_list.append(cat.find('span').string)

    catalog = dict(zip(category_list, urls))
    return catalog

def get_products(catalog_name: str, url_link: str) -> list:
    url_home = 'https://krepkoshop.com'
    product_list = []
    #get the html of site 
    result = requests.get(url_link)
    src = result.content
    #make the content good to work with beautifulsoup
    soup = BeautifulSoup(src, 'lxml')

    catalog = soup.find_all('div', {'class': 'product-blb-name'})

    for card in catalog:           
        product = {
            'name': '',
            'old_price': 0,
            'sale': 0,
            'price': 0,
            'category': catalog_name,
            'url': ''
        }
        product['name'] = card.find('h5', {'itemprop': 'name'}).find('span').string.replace('\n', ' ')
        product['url'] = url_home + str(card.find('a', {'class': 'product-name'})['href'])
        product['price'] = int(card.find('span', {'class':'price nowrap'}).contents[0].strip(' руб.').replace(' ',''))
        if card.find('span', {'class':'sale-compare-block'}):
            product['old_price'] = int(card.find('span', {'class':'compare-at-price nowrap'}).string.strip(' руб.').replace(' ',''))
            product['sale'] = int(card.find('span', {'class':'sale-compare-block'}).contents[1].string.lstrip(' (-').rstrip('%)'))
        else:
            product['old_price'] = product['price']   
        product_list.append(product)
    return product_list

def write_in_table(product_list:list) -> None:
    today = datetime.datetime.now()
    workbook = xlsxwriter.Workbook('C:/Users/romal/Documents/github/krepko/krepko-prices {}.xlsx'.format(today.strftime("%d %m %Y %H %M")))
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    worksheet.write('A1', 'наименование', bold)
    worksheet.write('B1', 'старая цена', bold)
    worksheet.write('C1', 'скидка', bold)
    worksheet.write('D1', 'цена', bold)
    worksheet.write('E1', 'категория', bold)
    worksheet.write('F1', 'ссылка', bold)

    row = 1
    
    for card in product_list:
        print(card)
        col = 0
        worksheet.write_string(row, col, card['name'])
        worksheet.write_number(row, col + 1, card['old_price'])
        worksheet.write_number(row, col + 2, card['sale'])
        worksheet.write_number(row, col + 3, card['price'])
        worksheet.write_string(row, col + 4, card['category'])
        worksheet.write_url(row, col + 5, card['url'])
        row += 1
    workbook.close()
    return

category_list = []
product_list = []
#krepko site
catalog = get_catalog("https://krepkoshop.com/category/")

for category in catalog:
    category_list.append(get_products(category, catalog[category]))
for category in category_list:
    for product in category:
        product_list.append(product) 

write_in_table(product_list)

today = datetime.datetime.now()
with open ('C:/Users/romal/Documents/github/krepko/krepko-prices {}.json'.format(today.strftime("%d %m %Y %H %M")), 'w', encoding='utf-8') as f:
    json.dump(product_list, f, ensure_ascii=False)