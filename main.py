import utils
import datetime

# Script launch
url = 'http://books.toscrape.com/'

allBooks = utils.getAllCategoriesBooks(url)

# Write the csv
date = datetime.datetime.now().strftime('%Y-%m-%d')
with open('out/' + date + '-oneBookDatas.csv', 'w') as file:
    file.write(
        'product_page_url;'
        'universal_product_code (upc);'
        'title;'
        'price_including_tax;'
        'price_excluding_tax;'
        'number_available;'
        'product_description;'
        'category;'
        'review_rating;'
        'image_url\n'
    )
    for oneBook in allBooks:
        # print(type(oneBook))
        for key, value in oneBook.items():
            file.write(value + ';')
        file.write('\n')

print('done')