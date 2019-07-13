import requests
import smtplib
from bs4 import BeautifulSoup

class AmazonScraper:

	def __init__(self):
		self.links_file = 'amazon_links.txt'
		self.price_thresholds_file = 'amazon_price_thresholds.txt'
		self.titles_file = 'amazon_item_names.txt'
		self.headers = {'User-Agent': 
						('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
							'AppleWebKit/537.36 (KHTML, like Gecko) '
							'Chrome/75.0.3770.100 Safari/537.36')}
		
		self.URLS = []
		self.obtain_URLS()

		self.titles = []
		self.obtain_titles()

		self.price_thresholds = []
		self.obtain_price_thresholds()


	def obtain_URLS(self):
		with open(self.links_file) as infile:
			for line in infile:
				self.URLS.append(line)


	def get_title(self, link):
		page = requests.get(link, headers=self.headers)
		soup = BeautifulSoup(page.content, "lxml")
		try:
			return(soup.find(id="productTitle").get_text().strip())
		except:
			print("An item title could not be found")
			return "Title Error"


	def obtain_titles(self):
		with open(self.titles_file) as infile:
			for line in infile:
				self.titles.append(line)


	def obtain_price_thresholds(self):
		with open(self.price_thresholds_file) as infile:
			for line in infile:
				self.price_thresholds.append(float(line))


	def check_prices(self):
		for index in range(len(self.URLS)):
			page = requests.get(self.URLS[index], headers=self.headers)
			soup = BeautifulSoup(page.content, "lxml")
			try:
				price = soup.find(id='priceblock_ourprice').get_text()
				price = float(price[1:])

				if price < self.price_thresholds[index]:
					self.send_mail(index)
					self.change_threshold(index+1, str(price))
			except:
				print("No price provided by amazon, use another link")
				print("Item with Error: "+self.get_title(self.URLS[index]))



	def send_mail(self, index):

		# setup server connection
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login('roccopolimen@gmail.com', 'ysytlrowjwhxplvy')

		page = requests.get(self.URLS[index], headers=self.headers)
		soup = BeautifulSoup(page.content, "lxml")
		price = soup.find(id='priceblock_ourprice').get_text()
		price = str(float(price[1:]))

		subject = 'Price Drop on "'+self.titles[index]+'" !!!'
		body = ('Click the amazon link to see!\nThe price is now: $'+price+'!'
													'!!\n\n'+self.URLS[index])

		mg = f"Subject: {subject}\n\n{body}"

		server.sendmail('roccopolimen@gmail.com', 'roccopolimen@gmail.com', mg)

		print('Email has been sent')

		server.quit()


	def change_threshold(self, line_number, price):
		change_value(line_number, price, self.price_thresholds_file)


# File editing methods


# adds the given text to the end of the given .txt file
def add_line(text, link):
	file = open(link, 'a')
	file.write("\n")
	file.write(text)
	file.close()


# removes a line of text from the given .txt file at the line number
def remove_line(line_number, link):
	with open(link, "r") as f:
		lines = f.readlines()

	if line_number == len(lines):
		lines[-2] = lines[-2].strip("\n")

	with open(link, "w") as f:
		for index in range(len(lines)):
			if index+1 != line_number:
				f.write(lines[index])


# changes the value of the given line with text
def change_value(line_number, text, link):
	with open(link, "r") as f:
		lines = f.readlines()

	if line_number == len(lines):
		lines[-1] = text
	else:
		lines[line_number-1] = text + "\n"

	with open(link, "w") as f:
		for line in lines:
			f.write(line)