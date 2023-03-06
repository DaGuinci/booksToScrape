# Python script to scrape books datas from http://books.toscrape.com/ website

## Environment

This script runs with Python 3.9.13

## Activation

In the project folder:

``` python -m venv env ```

Activate the environment

``` source env/bin/activate ```

Or if Windows :
``` env/Scripts/activate.bat ```

## Dependencies

``` pip install -r requirements.txt ```

The requirements.txt wil install the packages:

- Requests

- BeautifulSoup4

## Execution

``` python main.py ```

## Rendering

The datas will be found in a "out" folder:
- a csv file with all text datas
- a "images" folder containing one folder by category, containing the images.
