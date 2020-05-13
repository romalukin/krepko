import os
import json
import glob
import requests
import config
import krepko_web_scraper

def compare(old_product_list: list, new_product_list: list) -> list:
    compare_list = []
    compare_string = ''
    for new_card in new_product_list:
        for old_card in old_product_list:
            if new_card['name'] == old_card['name']:
                if new_card['price'] != old_card['price']:
                    product = {
                        'name': new_card['name'],
                        'old_price': old_card['price'],
                        'price': new_card['price'],
                        'category': new_card['category'],
                        'url': new_card['url']
                    }
                    compare_list.append(product)
    compare_list = [dict(t) for t in {tuple(d.items()) for d in compare_list}]
    for card in compare_list:
        compare_string = compare_string + 'наименование: {}\nстарая цена: {}\nцена: {}\nкатегория: {}\nссылка: {}\n-----\n'.format(card['name'], card['old_price'], card['price'], card['category'], card['url'])
    return compare_string
	
def bot_sendtext(bot_message):
	### Send text message
	bot_token = config.token
	bot_chatID = config.ID
	send_text = u'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(bot_token, bot_chatID, bot_message)
	requests.get(send_text)


krepko_web_scraper.start_scrape()
files_json = glob.glob('C:/Users/romal/Documents/github/krepko/*.json')
files_xlsx = glob.glob('C:/Users/romal/Documents/github/krepko/*.xlsx')
print(files_json)
print(files_xlsx)
with open(files_json[0], encoding='utf-8') as old, open(files_json[1], encoding='utf-8') as new:
    old_product_list = json.load(old)
    new_product_list = json.load(new)
compare_string = compare(old_product_list, new_product_list) 
bot_sendtext(compare_string)
os.remove(files_json[0])
os.remove(files_xlsx[0])