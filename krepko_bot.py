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
    compare_list = [dict(t) for t in {tuple(card.items()) for card in compare_list}]
    for card in compare_list:
        compare_string = compare_string + '''наименование: {}\n
                                             старая цена: {}\n
                                             цена: {}\n
                                             категория: {}\n
                                             ссылка: {}\n'''.format(card['name'], card['old_price'], card['price'], card['category'], card['url']) 
    return compare_string
	
def bot_sendtext(bot_message):
	### Send text message
	bot_token = config.token
	bot_chatID = config.ID
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + bot_message
	requests.get(send_text)


krepko_web_scraper.start_scrape()
files = glob.glob('C:/Users/romal/Documents/github/krepko/*.json')
print(files)
with open(files[0], encoding='utf-8') as old, open(files[1], encoding='utf-8') as new:
    old_product_list = json.load(old)
    new_product_list = json.load(new)
compare_string = compare(old_product_list, new_product_list) 
bot_sendtext(compare_string)