import re
from bs4 import BeautifulSoup
import requests
import os

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

        # Get and transform book description
        if c.select('#product_description'):
            description = c.select('#product_description')[0].find_next('p').string
            description = description.replace(';', ':')
            description = description.replace('\n', '')
            description = description.replace('"', '”')
        else:
            description = 'NC'

        # Get and transform book prices
        priceIncl = re.sub('Â£', '', getTableItem(table, "Price (incl. tax)"))
        priceExcl = re.sub('Â£', '', getTableItem(table, "Price (excl. tax)"))

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

        # Download the book's image
        if not os.path.exists('out/images/'):
            os.mkdir('out/images/')
        if not os.path.exists('out/images/' + infos['category']):
            os.mkdir('out/images/' + infos['category'])

        imgData = requests.get(infos['image_url']).content
        imgName = infos['title'].replace('"', '')
        imgName = imgName.replace(' ', '_')
        imgName = imgName.replace('\'', '')
        imgName = imgName.replace('/', '-')

        with open(f"out/images/{infos['category']}/{imgName}.jpg", "wb+") as f:
            f.write(imgData)

        return infos

def getOnePageInfos(allBooks, url):
    pageRequest = requests.get(url)
    if pageRequest.ok:
        pageContent = BeautifulSoup(pageRequest.content, 'html.parser')

        # get the category name
        category = url.split('/')[-2]
        categoryName = category.split('_')[0]

        # Get all books urls
        articles = pageContent.findAll('article')

        # Loop in the urls and for each add a new bookInfo line
        for article in articles:
            articleUrl = article.find('a')['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
            allBooks.append(getBookInfos(articleUrl, categoryName))

        # Test if there is several pages, and if so repeat the operation
        nextPage = pageContent.find('li', class_='next')
        if nextPage:
            # treat next page
            segments = url.rpartition('/')
            nextUrl = url.replace(segments[-1], nextPage.find('a')['href'])

            getOnePageInfos(allBooks, nextUrl)


# List and proceed every categories url
def getAllCategoriesBooks(url):
    r = requests.get(url)

    if r.ok:
        allBooks = []
        soup = BeautifulSoup(r.content, 'html.parser')

        # Get all the categories urls
        categoryEntries = soup.find('div', class_='side_categories').findAll('li')

        # Delete the first item, named Books, referring to all books without category
        categoryEntries.pop(0)
        i = 0

        # Browse all categories
        for entry in categoryEntries:
            linkTag = entry.find('a')
            categoryUrl = url + linkTag['href']
            getOnePageInfos(allBooks, categoryUrl)

        return allBooks
