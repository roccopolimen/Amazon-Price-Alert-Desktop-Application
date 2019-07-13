from amazon_scraper import *
import time

scraper = AmazonScraper()

# while(True):
print('Checking for Price Drops...')
scraper.check_prices()
print('Finished!')