import requests
from bs4 import BeautifulSoup
from time import sleep
from random import uniform, randint
import sys
import dbfunctions
import os
#selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import time 

cur_dir = os.path.dirname(os.path.realpath(__file__))
base = 'https://newyork.craigslist.org'
section = '/search'
driver = webdriver.Chrome(executable_path="%s/chromedriver"%cur_dir)
driver.implicitly_wait(10)
mainWin = driver.window_handles[0]
breaking = False
search = ''
totalamount = None




sections = ["cpg", "web", "sad", "sof"]




def hover(element):  
    hov = ActionChains(driver).move_to_element(element)
    hov.perform()



def wait(a, b):
	rand=uniform(a, b)
	sleep(rand)





def get_total(search, link):
	totalamount = 1
	url = base+section+"/"+link+'?query='+search.replace(" ", "+")+"&is_paid=all"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	total = soup.find_all('span', attrs={'class':'totalcount'})
	totalcount = total[0].get_text()
	return int(totalcount)	





def scrape_emails(search, totalamount, breaking, skip, link_section):
	if totalamount > 120:
		totalamount = (int(totalamount) // 120)+1 
	else:
		totalamount = 1

	for a in range(totalamount):
		if breaking == True: 
			break

		page_number = a*120
		page = "&s={}".format(page_number)
		if a == 0:
			page = ''

		url = base+section+"/"+link_section+'?query='+search.replace(" ", "+")+"&is_paid=all"+page
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')
		links = soup.find_all('a', attrs={'class':'hdrlnk'})


		print("")
		print("")
		print(link_section)
		print(str(len(links))+" results")
		print("")

		for link in links:
			link_url = link.get('href')

			if breaking == True: 
				break
			
			if not dbfunctions.checkifvisited(link.get('href')):

				try:
					print('trying next link')
					driver.get(link.get('href'))

					try:
						button =  driver.find_element_by_class_name('reply-button')
						button.click()
						# ===================================================================================================================
						# 					CHECK IF THIS WORKS LATER
						# ===================================================================================================================
						# try:
						# 	captcha = WebDriverWait(driver, 2).until(lambda driver: driver.find_element_by_id('g-recaptcha'))
						# 	if captcha:
						# 		wait(1.0, 1.5)
						# 		recaptchaFrame = WebDriverWait(driver, 1).until(lambda driver: driver.find_element_by_tag_name('iframe'))
						# 		frameName = recaptchaFrame.get_attribute('name')
						# 		# move the driver to the iFrame... 
						# 		driver.switch_to_frame(frameName)
						# 		CheckBox = WebDriverWait(driver, 1).until(lambda driver: driver.find_element_by_id("recaptcha-anchor"))

						# 		wait(1.0, 1.5)
						# 		hover(CheckBox)
						# 		wait(0.5, 0.7)
						# 		CheckBox.click()
						# 		wait(2.0, 2.5)
						# 		if skip == 'y':
						# 			sleep(10)
						# 		else:
						# 			try:
						# 				driver.switch_to_window(mainWin)
						# 				html = driver.page_source
						# 				s = BeautifulSoup(html, 'html.parser')
						# 				iframes = s.find_all("iframe", attrs={'title': 'recaptcha challenge'})
						# 				secFrame = iframes[0].get('name')
						# 				if secFrame:
						# 					print 'There is Captcha now, try again later or try setting the solve captcha option as "y"'
						# 					driver.close()
						# 					breaking = True
						# 			except:
						# 				continue
						# 		driver.switch_to_window(mainWin)
						# except Exception as error:
						# 	print(error, "error")	
						# 	driver.switch_to_window(mainWin)
						# ===================================================================================================================

						try: 
							e = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_class_name('reply-email-address'))
							email = e.text
						except Exception as error:
							print(error, "getting email")
							continue

						if dbfunctions.checkifexists(email):
							print('Email already saved')
						else:
							dbfunctions.save_visited(link_url)
							dbfunctions.create_email(email)
							print('saving email '+email)
					except Exception as error:
						print(error, "getting the result site")
						continue
				except Exception as error:
					print(error, "trying result link")
					continue
			else: 
				print('link already visited')

	





if __name__=='__main__':
	if len(sys.argv) == 1:
		driver.close()
		print('')
		print('')
		print('Usage: python sele.py [search] [solve captcha]')
		print('solve captcha : y/n')
		print('search: word you want to search in the education section')
		print('')
		print('')

	else: 
		search = sys.argv[1]
		skip = ''
		if len(sys.argv) > 2:
			skip = sys.argv[2]
	
		for link in sections:
			try: 
				totalamount = get_total(search, link)
				scrape_emails(search, totalamount, breaking, skip, link)
			except Exception as error:
				print(error, "getting total ammount")
			
		driver.quit()




