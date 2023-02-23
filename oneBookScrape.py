import re
from bs4 import BeautifulSoup
import requests

# Use the rating tag css class to get the rating value
def getStarRating(c):
    star_rating = c.select('.star-rating')[0]['class'][1]
    match star_rating:
        case 'One':
            return '1'
        case 'Two':
            return '2'
        case 'Three':
            return '3'
        case 'Four':
            return '4'
        case _:
            return 'NC'


# Get the value of any item from the product page table
def getTableItem(table, entry):
    trs = table.findAll('tr')
    for tr in trs:
        if tr.find('th').string == entry:
            return tr.find('td').string


# Get each infos from product page in a dictionary
def getBookInfos(productUrl, categoryName):
    bookPageRequest = requests.get(productUrl)
    if bookPageRequest.ok:
        c = BeautifulSoup(bookPageRequest.content, 'html.parser')
        table = c.find('table')

        if c.select('#product_description'):
            description = c.select('#product_description')[0].find_next('p').string
            description = description.replace(";", ":")
            description = description.replace("\n", "")
        else:
            description = 'NC'

        priceIncl = re.sub('Â£', '', getTableItem(table, 'Price (incl. tax)'))
        priceExcl = re.sub('Â£', '', getTableItem(table, 'Price (excl. tax)'))

        infos = {
            'product_page_url': productUrl,
            'upc': getTableItem(table, 'UPC'),
            'title': '"' + c.find('h1').string + '"',
            'price_including_tax': priceIncl if len(priceIncl) != 0 else 'NC',
            'price_excluding_tax': priceExcl if len(priceExcl) != 0 else 'NC',
            'number_available': re.findall('\d+', getTableItem(table, 'Availability'))[0],
            'product_description': description,
            'category': categoryName,
            'review_rating': getStarRating(c),
            'image_url': c.find('img')['src'].replace('../../', 'http://books.toscrape.com/')
        }
        return infos
