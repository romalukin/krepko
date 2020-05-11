import json
import glob

def compare(old_product_list: list, new_product_list: list) -> list:
    compare_list = []
    for new_card in new_product_list:
        for old_card in old_product_list:
            if new_card['name'] == old_card['name']:
                if new_card['price'] != old_card['price']:
                    product = {
                        'name': new_card['price'],
                        'old_price': old_card['price'],
                        'price': new_card['price'],
                        'category': new_card['category'],
                        'url': new_card['category']
                    }
                    compare_list.append(product)
    return


files = glob.glob('C:/Users/romal/Documents/github/krepko/*.json')
with open(files[0], encoding='utf-8') as old, open(files[1], encoding='utf-8') as new:
    old_product_list = json.load(old)
    new_product_list = json.load(new)

