from tkinter import *
from amazon_scraper import *
import webbrowser


class Window:

	def __init__(self):

		self.set_window_size()

		# create loading screen
		self.load_window()
		self.load_window.after(500, self.setup_scraper)
		self.load_window.mainloop()

		# constructs the window
		self.root = Tk()

		# sets dimensions and disables resizing the window
		self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, 
							(self.screen_width//2) - (self.width//2), 
							(self.screen_height//2) - (self.height//2)))
		self.root.resizable(False, False)

		self.title_frame()
		self.item_layout()
		self.button_layout()

		# displays the window continuously
		self.root = mainloop()


	# sets up the window size based on screen resolution
	def set_window_size(self):

		temp_window = Tk()

		# tkinter obtains the number of pixels in the screen
		self.screen_width = temp_window.winfo_screenwidth()
		self.screen_height = temp_window.winfo_screenheight()

		temp_window.destroy()

		# size of the window to create
		self.width = self.screen_width//3
		self.height = 5*self.screen_height//6


	# constructs the loading window
	def load_window(self):
		self.load_window = Tk()
		self.load_window.title('loading...')

		width = self.width//2
		height = self.height//8
		x = (self.screen_width//2) - (width//2)
		y = (self.screen_height//2) - (height//2)	
		
		self.load_window.geometry('%dx%d+%d+%d' %(width, height, x, y))

		font = "Arial 14"

		label = Label(self.load_window, font=font, 
						text='Loading assets.\nPlease wait...')
		label.pack(anchor=CENTER, pady=10)


	# creates the scraper and then destroys the loading screen
	def setup_scraper(self):
		self.scraper = AmazonScraper()
		self.load_window.destroy()


	# constructs the title of the window
	def title_frame(self):

		# window title
		self.root.title('Amazon Price Alert')
		self.root.iconbitmap(r'amazon_price_alert_icon.ico')

		# constructs a title frame to place the title in as a header
		title_frame_height = self.height//5
		title_frame = Frame(self.root, height=title_frame_height, 
							width=self.width)
		title_frame.grid(row=0, column=0, columnspan=2)

		# creates a font size to fit the title within the frame
		title_font = (title_frame_height//4)

		# title formatted as a header
		title = Label(title_frame, text='Amazon Price Alert', 
							font="Arial "+str(title_font)+" bold underline")
		title.place(x=self.width//2, y=self.height//10, anchor='center')


	# constructs the list view of the window
	def item_layout(self):

		# construct the scrollbar
		self.y_scrollbar = Scrollbar(self.root, orient=VERTICAL)
		self.x_scrollbar = Scrollbar(self.root, orient=HORIZONTAL)

		# construct List Box and binds its selection to activate buttons
		items_font = (self.height//32)
		self.items_list = Listbox(self.root, selectmode=SINGLE, height=12, 
								width=30, font="Arial "+str(items_font), 
								yscrollcommand=self.y_scrollbar.set, 
								xscrollcommand=self.x_scrollbar.set)
		self.items_list.bind('<<ListboxSelect>>', self.activate_buttons)

		# provide the scrollbars with functionality
		self.y_scrollbar.config(command=self.items_list.yview)
		self.x_scrollbar.config(command=self.items_list.xview)

		# add the list and scrollbars to the grid
		self.items_list.grid(row=1, column=0, sticky='nswe')
		self.y_scrollbar.grid(row=1, column=1, sticky='ns')
		self.x_scrollbar.grid(row=2, column=0, sticky='nswe')

		# insert appropriate items into the list
		self.fill_list()


	# constructs the frame containing the buttons to update the item list
	def button_layout(self):
		
		# create frame to hold all the buttons
		self.buttons_frame = Frame(self.root, width=self.width, bg='red')
		self.buttons_frame.grid(row=3, columnspan=2)

		button_font = "Arial "+str(self.width//25)

		# initialize buttons
		self.add_button = Button(self.buttons_frame, text='Add Item', 
									font=button_font,
									command=self.add_item_window)
		self.remove_button = Button(self.buttons_frame, text='Remove Item',
								command=self.remove_item_window, 
								state=DISABLED, font=button_font)
		self.view_details_button = Button(self.buttons_frame, 
								text='View Details', 
								command=self.view_item_details, state=DISABLED,
								font=button_font)

		# pack buttons into the frame
		self.add_button.grid(row=0, column=0, sticky='nswe')
		self.remove_button.grid(row=0, column=1, sticky='nswe')
		self.view_details_button.grid(row=0, column=2, sticky='nswe')


	# adds the Amazon items into the list box
	def fill_list(self):
		for i in range(len(self.scraper.titles)):
			self.items_list.insert(i, self.scraper.titles[i])


	# provides a pop-up box to allow user to add an item
	def add_item_window(self):
		self.new_item_window = Toplevel()

		self.new_item_window.lift()
		self.new_item_window.focus_force()
		self.new_item_window.grab_set()
		self.new_item_window.grab_release()

		self.new_item_window.title('New Item')

		niw_width = 2*self.width//3
		niw_height = self.height//6
		niw_x = (self.screen_width//2) - (niw_width//2)
		niw_y = (self.screen_height//2) - (niw_height//2)
		self.new_item_window.geometry('%dx%d+%d+%d' % 
									(niw_width, niw_height, niw_x, niw_y))
		niw_font = "Arial 15"

		label_1 = Label(self.new_item_window, text='Amazon link', 
							font=niw_font)
		label_2 = Label(self.new_item_window, text='Alert under this price: $',
							font=niw_font)
		self.textbox_1 = Entry(self.new_item_window)
		self.textbox_2 = Entry(self.new_item_window)
		submit_button = Button(self.new_item_window, text='submit', 
								font=niw_font, command=self.add_item)

		label_1.grid(row=0, column=0, sticky=E)
		label_2.grid(row=1, column=0, sticky=E)
		self.textbox_1.grid(row=0, column=1)
		self.textbox_2.grid(row=1, column=1)
		submit_button.grid(row=2, columnspan=2)


	# confirms the user actually wants to delete the selected item
	def remove_item_window(self):
		self.confirmation_window = Toplevel()

		self.confirmation_window.lift()
		self.confirmation_window.focus_force()
		self.confirmation_window.grab_set()
		self.confirmation_window.grab_release()

		self.confirmation_window.title('Remove Item?')

		width = 2*self.width//3
		height = self.height//6
		x = (self.screen_width//2) - (width//2)
		y = (self.screen_height//2) - (height//2)
		self.confirmation_window.geometry('%dx%d+%d+%d' %(width, height, x, y))

		font = "Arial 16"

		label = Label(self.confirmation_window, 
					text="Are you sure you would like to\nremove this item?", 
					font=font, anchor=CENTER)
		yes_button = Button(self.confirmation_window, text='Yes', font=font,
							command=self.remove_item)
		no_button = Button(self.confirmation_window, text='No', font=font, 
							command=self.close_confirm_window)

		label.grid(row=0, columnspan=2, sticky='nswe', padx=20)
		yes_button.grid(row=1, column=0, sticky='nswe', padx=10)
		no_button.grid(row=1, column=1, sticky='nswe', padx=10)


	# provides the user with a window containing more details about the item
	def view_item_details(self):
		self.view_window = Toplevel()

		self.view_window.lift()
		self.view_window.focus_force()
		self.view_window.grab_set()
		self.view_window.grab_release()

		self.view_window.title('See Product Details')

		width = 2*self.width//3
		height = self.height//6
		x = (self.screen_width//2) - (width//2)
		y = (self.screen_height//2) - (height//2)
		self.view_window.geometry('%dx%d+%d+%d' %(width, height, x, y))

		font = "Arial 15"

		index = self.items_list.curselection()[0]
		price = self.scraper.price_thresholds[index]

		label_1 = Label(self.view_window, 
						text='Current Alert Price: $'+str(price), font=font)
		label_2 = Label(self.view_window, font=font, 
						text='Check item online?')
		change_price_threshold_button = Button(self.view_window, font=font,
												text='Change Value', 
												command=self.threshold_window)
		open_link_button = Button(self.view_window, text='Open Link',
									font=font, command=self.open_link)

		label_1.grid(row=0, columnspan=2, sticky=W)
		change_price_threshold_button.grid(row=1, column=0, sticky=W)
		label_2.grid(row=2, column=0, sticky=E)
		open_link_button.grid(row=2, column=1, sticky=W)


	# enables buttons when an item is selected
	def activate_buttons(self, event):
		self.remove_button.config(state=NORMAL)
		self.view_details_button.config(state=NORMAL)


	# uses the provided information to add an item
	def add_item(self):

		# obtains the data from the text fields
		link = self.textbox_1.get()
		price_point = self.textbox_2.get()

		# makes sure the user entered something
		if not link or not price_point:
			return

		# adds the new data to their respective files
		add_line(link, self.scraper.links_file)
		add_line(price_point, self.scraper.price_thresholds_file)
		add_line(self.scraper.get_title(link), self.scraper.titles_file)

		# reconstructs the web scraper to account for new data
		self.scraper.URLS.append(link)
		self.scraper.price_thresholds.append(price_point)
		self.scraper.titles.append(self.scraper.get_title(link))

		# adds the new item to the end of the list box
		self.items_list.insert(self.items_list.size(), self.scraper.titles[-1])

		# closes the window that adds items and returns to home screen
		self.new_item_window.destroy()


	# removes the selected item from the saved data
	def remove_item(self):

		# obtain the line number in a file of the selected item
		line_number = self.items_list.curselection()[0]+1

		# removes the item from the list box
		self.items_list.delete(self.items_list.curselection()[0])

		# remove the item's data from the files
		remove_line(line_number, self.scraper.links_file)
		remove_line(line_number, self.scraper.price_thresholds_file)
		remove_line(line_number, self.scraper.titles_file)

		# reconstruct the scraper so it forgets the item
		del self.scraper.URLS[line_number-1]
		del self.scraper.titles[line_number-1]
		del self.scraper.price_thresholds[line_number-1]

		# destroys the confirmation window and brings user to the home screen
		self.confirmation_window.destroy()

	# destroys the confirmation window and brings user to the home screen
	def close_confirm_window(self):
		self.confirmation_window.destroy()


	# creates window for user to input and submmit a change in price value
	def threshold_window(self):
		self.change_value_window = Toplevel()

		self.change_value_window.lift()
		self.change_value_window.focus_force()
		self.change_value_window.grab_set()
		self.change_value_window.grab_release()

		self.change_value_window.title('Enter new price alert value')

		width = self.width//2
		height = self.height//8
		x = (self.screen_width//2) - (width//2)
		y = (self.screen_height//2) - (height//2)
		self.change_value_window.geometry('%dx%d+%d+%d' %(width, height, x, y))

		font = "Arial 14"

		self.price_textbox = Entry(self.change_value_window)
		submit_button = Button(self.change_value_window, text='submit',
								font=font, command=self.change_threshold)

		self.price_textbox.grid(row=0, sticky=W)
		submit_button.grid(row=1, sticky='nswe')


	# allows the user to open the link of the currently selected item
	def open_link(self):
		link = self.scraper.URLS[self.items_list.curselection()[0]]
		webbrowser.open(link)


	# uses the user input to update the price alert of the selected item
	def change_threshold(self):
		new_price = self.price_textbox.get()

		line_number = self.items_list.curselection()[0]+1

		if not new_price:
			return

		self.scraper.change_threshold(line_number, new_price)

		self.scraper.price_thresholds[line_number-1] = new_price
		
		self.change_value_window.destroy()
		self.view_window.destroy()


# called when this program is executed, opens the window
if __name__ == '__main__':
	window = Window()