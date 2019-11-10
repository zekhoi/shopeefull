import requests as req
from bs4 import BeautifulSoup as bs
import json
import time as tm
from colorama import init,Fore
import csv,os
from datetime import date

today = str(date.today())
init()

headers ={
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
		'Accept': '*/*',
		'Sec-Fetch-Site': 'cross-site',
		'Sec-Fetch-Mode': 'cors',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
		'Cookie': '_gcl_au=1.1.1805060871.1573050834; csrftoken=o2vL1uM6rjqnZeoF8DL1TvxV3UTNEQ0Q; SPC_IA=-1; SPC_EC=-; SPC_U=-; SPC_F=mLEuEMmtcbYOuxFXoeu1LhVm3sVPaYWI; REC_T_ID=764ae7e6-00a2-11ea-9518-ccbbfe5deb6f; SPC_SI=y19ecj3o4kc4z755mc14k0ogtct4bjro; REC_T_ID=76a057eb-00a2-11ea-95e2-ccbbfe5d5dc7; welcomePkgShown=true; _ga=GA1.3.507803947.1573050840; _gid=GA1.3.1036868182.1573050840; SPC_RW_HYBRID_ID=53; language=id; AMP_TOKEN=%24NOT_FOUND; REC_MD_20=1573055624; SPC_T_IV="qqYfP57NxFROEOr2gCk2rQ=="; SPC_T_ID="rhIBTy5XHQDYjc2Be34aQnc37c2A7D7Zpl7wBBUHzrzsdUsyH4jTMpS65f8G+Q0+EqhDmGdQyJmUfZSx0zt35b3s5q1OHlgbwNoHlrjbXZU="'
		}


def time(sec):
	tm.sleep(sec)

def search(keyword,limit,headers):
	return req.get('https://shopee.co.id/api/v2/search_items/?by=relevancy&keyword='+keyword+'&limit='+limit+'&newest=0&order=desc&page_type=search&version=2',headers=headers)

def products(itemid,shopid):
	return req.get('https://shopee.co.id/api/v2/item/get?itemid='+itemid+'&shopid='+shopid)

def seller(shopid,headers):
	return req.get('https://shopee.co.id/api/v2/search_users/?keyword='+shopid+'&limit=100&with_search_cover=true',headers=headers)

def shoper(shop,limit,headers):
	return req.get('https://shopee.co.id/api/v2/search_items/?by=pop&limit='+limit+'&match_id='+shop+'&newest=0&order=desc&page_type=shop&version=2',headers=headers)

def photo(imgcode):
	return req.get('http://cf.shopee.co.id/file/'+imgcode)
def got():
	return req.get('https://shopee.co.id/api/v2/search_items/?by=pop&limit=100&match_id=39869292&newest=0&order=desc&page_type=shop&version=2')
print (" ##########################")
print (" #                        #")
print (" #        Insomniac       #")
print (" #  https://insomniac.id  #")
print (" #       Supi Scraper     #")
print (" #                        #")
print (" ##########################")
print(" 1. Search Item")
print(" 2. Search Seller")



menu = int(input(' Menu : '))
try:
	if (menu == 1):
		keyword = input(' Search keyword : ')
		limit = int(input(' Get items total (Max 100) : '))
		print(" Searching "+ str(limit) + " " + keyword + " on shopee")
		p = search(keyword,str(limit),headers)
		barangs = json.loads(p.text)
		items = barangs['items']
		print("" , len(items), "items found" )
		save = input(' Save to Excel ?(y/n) : ')
		if save == 'y' or save == 'Y':
			name = input(' Save as (filename).csv : ')
			if not os.path.exists(today):
				os.mkdir(today)
			file = open(today+"/"+name+'.csv','w') # w untuk write/mengganti data sebelumnya (menjadi terhapus sebelumnya)
		                                # a untuk menambah data tanpa menghapus data sebelumnya
			writer = csv.writer(file)
			writer.writerow(['Nama Barang', 'Item ID','Shop ID','Terjual', 'Harga'])
		img = input(' Save images ?(y/n) : ')
		time(4)
		if img == 'y' or img == 'Y':
			if not os.path.exists(today):
				os.makedirs(today)
		for item in items:
			itemid = str(item['itemid'])
			shopid = str(item['shopid'])
			infoses = products(itemid,shopid)
			infos = json.loads(infoses.text)
			time(2)
			info = infos['item']
			images = info['images']
			print(Fore.GREEN + "[+] " +Fore.YELLOW + info['name'])
			print(Fore.GREEN + "[+]" +Fore.YELLOW+" ItemID : "+itemid)
			print(Fore.GREEN + "[+]" +Fore.YELLOW+" ShopID : "+shopid)
			print(Fore.GREEN + "[+]" +Fore.YELLOW+" Sold   :",info['historical_sold'],"sold")
			print(Fore.GREEN + "[+] " +Fore.YELLOW+"Rp", str(info['price_max'])[0:-5])
			if img == 'y' or img == 'Y':
				if not os.path.exists(today +"/"+str(item['itemid'])):
					folder = os.makedirs(today+"/"+str(item['itemid']))
				for image in images:
					imgs = photo(image)
					if imgs.status_code == 200:
					    with open(today+"/"+str(itemid)+"/"+str(image)+".png", 'wb') as f:
					        f.write(imgs.content)
					    print(Fore.GREEN + "[+]" +Fore.YELLOW ,image,"saved")
					else:
						print(Fore.RED + "[-]" +Fore.YELLOW ,image,"failed to save")
					time(1)
			print("\n")
			if save == 'y' or save == 'Y':
				writer.writerow([info['name'], info['itemid'], info['shopid'],str(info['historical_sold']),str(info['price_max'])[0:-5]])
			time(1.7)
		if save == 'y' or save == 'Y':
			file.close()
		print(' Done!')
	elif (menu == 2):
		sell = input(' Search keyword : ')
		print(" Searching "+ sell + " on shopee")
		p = seller(sell,headers)
		time(2)
		scrape = json.loads(p.text)
		getshop = scrape['data']['users']
		if  len(getshop) == 0:
			print(' Not Found')
		else:
			i=0
			for shop in getshop:
				i+=1
				print("["+str(i)+"]"+shop['shopname'])
			anu = int(input(" I choose number : "))
			data = scrape['data']['users'][anu-1]
			shopid = str(data['shopid'])
			shopname = data['shopname']
			time(2)
			print(" Get",shopname,": "+shopid)
			limit = int(input(' Get items total (Max 100) : '))
			getitems = json.loads(shoper(shopid,str(limit),headers).text)
			items = getitems['items']
			time(2)
			print("" , len(items), "items found")
			save = input(' Save to Excel ?(y/n) : ')
			if save == 'y' or save == 'Y':
				name = input(' Save as (filename).csv : ')
				if not os.path.exists(today):
					os.mkdir(today)
				file = open(today+"/"+name+'.csv','w') # w untuk write/mengganti data sebelumnya (menjadi terhapus sebelumnya)
			                                # a untuk menambah data tanpa menghapus data sebelumnya
				writer = csv.writer(file)
				writer.writerow(['Nama Barang', 'Item ID','Shop ID','Terjual', 'Harga'])
			img = input(' Save images ?(y/n) : ')
			for item in items:
				itemid = str(item['itemid'])
				infoses = products(itemid,shopid)
				# time(5)
				infos = json.loads(infoses.text)
				info = infos['item']
				images = info['images']
				print(Fore.GREEN + "[+] " +Fore.YELLOW + info['name'])
				print(Fore.GREEN + "[+]" +Fore.YELLOW+" ItemID : "+itemid)
				print(Fore.GREEN + "[+]" +Fore.YELLOW+" ShopID : "+shopid)
				print(Fore.GREEN + "[+]" +Fore.YELLOW+" Sold   :",info['historical_sold'],"sold")
				print(Fore.GREEN + "[+] " +Fore.YELLOW+"Rp", str(info['price_max'])[0:-5])
				if img == 'y' or img == 'Y':
					if not os.path.exists(today +"/"+str(item['itemid'])):
						folder = os.makedirs(today+"/"+str(item['itemid']))
					for image in images:
						imgs = photo(image)
						if imgs.status_code == 200:
						    with open(today+"/"+str(itemid)+"/"+str(image)+".png", 'wb') as f:
						        f.write(imgs.content)
						    print(Fore.GREEN + "[+]" +Fore.YELLOW ,image,"saved")
						else:
							print(Fore.RED + "[-]" +Fore.YELLOW ,image,"failed to save")
						time(1)
				print("\n")
				if save == 'y' or save == 'Y':
					writer.writerow([info['name'], info['itemid'], info['shopid'],str(info['historical_sold']),str(info['price_max'])[0:-5]])
				time(1.7)
			if save == 'y' or save == 'Y':
				file.close()
		print(' Done!')
	else:
		print('Something Wrong...')
except:
	print(' There was an error!')
