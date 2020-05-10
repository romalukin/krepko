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

def  get_products(catalog_name: str, url_link: str) -> dict:
    #get the html of site 
    result = requests.get(url_link)
    src = result.content
    #make the content good to work with beautifulsoup
    soup = BeautifulSoup(src, 'lxml')

    for ul_tag in soup.find_all('ul'):
        if ul_tag['class'] == ['li3', 'product-list', 'thumbs']:
            li_tag_list = ul_tag.find_all('li')

    for li_tag in li_tag_list:            
        product = {
            'name': '',
            'old_price': 0,
            'sale': 0,
            'price': 0,
            'description': '',
            'category': '',
            'url': ''
        }
        product['name'] = li_tag.find('h5').find('span').string.replace('\n', ' ')
        product['url'] = url_link + str(li_tag.find('h5').find('a')['href'].lstrip('/'))
        product['description'] = li_tag.find('meta')['content']
        product['price'] = int(li_tag.find('span', {'class':'price nowrap'}).contents[0].strip(' руб.').replace(' ',''))
        if li_tag.find('span', {'class':'compare-at-price nowrap'}):
            product['old_price'] = int(li_tag.find('span', {'class':'compare-at-price nowrap'}).string.strip(' руб.').replace(' ',''))
        else:
            product['old_price'] = product['price']   

    return 0

#krepko site
catalog = get_catalog("https://krepkoshop.com/category/")
for category in catalog:
    get_products(category, catalog[category])
pprint(catalog)