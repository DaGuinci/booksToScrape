import oneBookScrape
import datetime

# Script launch
url = 'https://books.toscrape.com/catalogue/olio_984/index.html'

oneBookInfos = oneBookScrape.getBookInfos(url, 'categoryTest')

date = datetime.datetime.now().strftime('%Y-%m-%d')

# Write the csv
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
    for key, value in oneBookInfos.items():
        file.write(value + ';')
    file.write('\n')

print('done')