from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
from multiprocessing import Process, Lock
import urllib2
import csv
import pickle
# testtesttestpullreq

f = open('data.txt', 'w')

csv_arr = []
companies = []
total_checked = 0
companies_owned = {}

def add_ticker():
    print "enter ticker"
    n=raw_input()
    print "enter numberowned"
    m=raw_input()
    companies_owned[n]=m

def ticker():
	path = "companylist.csv"
	csv_file = open(path, 'rb');
	csv_reader = csv.reader(csv_file, delimiter = ",", quotechar = "\"")
	for row in csv_reader:
		csv_arr.append((row[0], row[1]))
	# print csv_arr
	while 1:
                print "Enter Portfolio Information"
                print "type name to search"
                print "type 'add' to add companies or 'quit' to exit"
                x=raw_input()
                if x=='quit':
                        break
                if x in companies_owned.keys():
                        print companies_owned[x], x
                if x=='add':
                        add_ticker()

def funct(start, fin, thread_num):
	print start, " - ", fin, ": ", thread_num, " Thread Started"
	global total_checked
	for i in range (start, fin):
		# print i
		# print "thread: ", thread_num, " :   ", i, " - ", fin
		total_checked += 1
		try:
			cnn = 'http://money.cnn.com/quote/quote.html?symb=' + csv_arr[i][0]
			cnn_soup = BeautifulSoup(urllib2.urlopen(cnn))
			price_book = cnn_soup.find('td', text = "Price/Book").next_sibling.text
			# print price_book
			if float(price_book) < 1:
				companies.append([csv_arr[i][0], price_book])
				mark_cap = cnn_soup.find('td', text = "Market cap").next_sibling.text[1:]
				mark_cap_act = ((float)(mark_cap[:-1]))
				if mark_cap[-1:] == "B":
					mark_cap_act = (int)(mark_cap_act * 1000000000)
				if mark_cap[-1:] == "M":
					mark_cap_act = (int)(mark_cap_act * 1000000)
				if mark_cap_act > 200*1000000:
					print csv_arr[i][0] , "   ", price_book, "   ", mark_cap, "   ", csv_arr[i][1], " Progress: ", total_checked, " of 3250 checked."
					# f.write(csv_arr[i][0] , "   ", price_book, "   ", mark_cap, "   ", csv_arr[i][1], "\n")
			if i % 20 == 0:
				pass
		except Exception as e:
			# print e
			pass

def main():
	ticker()
	for u in range(0, len(csv_arr)/50):
		# print u
		Process(target = funct, args = (u * 50, (u + 1) * 50, u)).start()
	# Process(target = funct, args = (0, 21)).start()
	# p.start()
	

main()

	# TODO : split by sector
