import requests
import xlsxwriter
from bs4 import BeautifulSoup
from pprint import pprint


def get_catalog(url_link: str) -> dict:
    #get the html of site 
    result = requests.get(url_link)
    src = result.content
    #make the content good to work with beautifulsoup
    soup = BeautifulSoup(src, 'lxml')

    urls = []
    category_list= []

    for ul_tag in soup.find_all('ul'):
        if ul_tag['class'] == ['catalog']:
            a_zone = ul_tag.find_all('a')

    for a_tag in a_zone:
        urls.append(url_link + str(a_tag['href']).replace('/category/', ''))
        span = a_tag.find('span')
        category_list.append(span.string)

    catalog = dict(zip(category_list, urls))
    return catalog

def  get_products(catalog_name: str, url_link: str) -> list:
    url_home = 'https://krepkoshop.com/category'
    product_list = []
    #get the html of site 
    result = requests.get(url_link)
    src = result.content
    #make the content good to work with beautifulsoup
    soup = BeautifulSoup(src, 'lxml')


    catalog = soup.find_all('li', {'itemtype': 'http://schema.org/Product'})

    for card in catalog:            
        product = {
            'name': '',
            'old_price': 0,
            'sale': 0,
            'price': 0,
            'description': '',
            'category': catalog_name,
            'url': ''
        }
        product['name'] = card.find('h5', {'itemprop': 'name'}).find('span').string.replace('\n', ' ')
        product['url'] = url_home + str(card.find('a', {'class': 'product-name'})['href'])
        product['description'] = card.find('meta', {'itemprop': 'description'})['content']
        product['price'] = int(card.find('span', {'class':'price nowrap'}).contents[0].strip(' руб.').replace(' ',''))
        if card.find('span', {'class':'sale-compare-block'}):
            product['old_price'] = int(card.find('span', {'class':'compare-at-price nowrap'}).string.strip(' руб.').replace(' ',''))
            product['sale'] = int(card.find('span', {'class':'sale-compare-block'}).contents[1].string.lstrip(' (-').rstrip('%)'))
        else:
            product['old_price'] = product['price']   
        product_list.append(product)
    return product_list


product_list = []
#krepko site
catalog = get_catalog("https://krepkoshop.com/category/")
for category in catalog:
    product_list.append(get_products(category, catalog[category]))
pprint(catalog)

with open('C:/Users/romal/Documents/github/krepko/test.txt', 'w', encoding='utf-8') as f:
    for category in product_list:
        for card in category:
            f.write('-----\n')
            for field in card:
                f.write('{}: {}\n'.format(field, card[field]))