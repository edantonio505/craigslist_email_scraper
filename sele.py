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

cur_dir = os.path.dirname(os.path.realpath(__file__))
base = 'https://newyork.craigslist.org'
section = '/search/edu'
driver = webdriver.Chrome(executable_path="%s/chromedriver"%cur_dir)
mainWin = driver.window_handles[0]
breaking = False
search = ''
totalamount = None

def hover(element):  
    hov = ActionChains(driver).move_to_element(element)
    hov.perform()

def wait(a, b):
	rand=uniform(a, b)
	sleep(rand)

def get_total(search):
	r = requests.get(base+section+'?query='+search)
	soup = BeautifulSoup(r.content, 'html.parser')
	total = soup.find_all('span', attrs={'class':'totalcount'})
	totalcount = total[0].get_text()
	return totalcount	

def scrape_emails(search, totalamount, breaking, skip):
	for a in range((int(totalamount)/100)+1):
		if breaking == True: 
			break

		page_number = a*100
		page = '?=%s&query='%page_number
		if a == 0:
			page = '?query='

		r = requests.get(base+section+page+search)
		soup = BeautifulSoup(r.content, 'html.parser')
		links = soup.find_all('a', attrs={'class':'hdrlnk'})

		for link in links:
			if breaking == True: 
				break

			if not dbfunctions.checkifvisited(base+link.get('href')):
				dbfunctions.save_visited(base+link.get('href'))
				try:
					print 'trying next link'
					driver.get(base+link.get('href'))
					# click the reply button to get email
					try:
						button =  driver.find_element_by_class_name('reply_button')
						button.click()
						try:
							captcha = WebDriverWait(driver, 2).until(lambda driver: driver.find_element_by_id('g-recaptcha'))
							if captcha:
								wait(1.0, 1.5)
								recaptchaFrame = WebDriverWait(driver, 1).until(lambda driver: driver.find_element_by_tag_name('iframe'))
								frameName = recaptchaFrame.get_attribute('name')
								# move the driver to the iFrame... 
								driver.switch_to_frame(frameName)
								CheckBox = WebDriverWait(driver, 1).until(lambda driver: driver.find_element_by_id("recaptcha-anchor"))
								
								wait(1.0, 1.5)
								hover(CheckBox)
								wait(0.5, 0.7)
								CheckBox.click()
								wait(2.0, 2.5)
								
								if skip == 'y':
									sleep(10)
								else:
									try:
										driver.switch_to_window(mainWin)
										html = driver.page_source
										s = BeautifulSoup(html, 'html.parser')
										iframes = s.find_all("iframe", attrs={'title': 'recaptcha challenge'})
										secFrame = iframes[0].get('name')

										if secFrame:
											print 'There is Captcha now, try again later or try setting the solve captcha option as "y"'
											driver.close()
											breaking = True
									except:
										continue

								driver.switch_to_window(mainWin)
						except:
							driver.switch_to_window(mainWin)

						e = WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_class_name('anonemail'))
						email = e.text
						if dbfunctions.checkifexists(email):
							print 'Email already saved'
						else:
							dbfunctions.create_email(email)
							print 'saving email '+email
					except:
						continue
				except:
					continue

			else: 
				print 'link already visited'

	driver.close()





if __name__=='__main__':
	if len(sys.argv) == 1:
		driver.close()
		print ''
		print ''
		print 'Usage: python sele.py [search] [solve captcha]'
		print 'solve captcha : y/n'
		print 'search: word you want to search in the education section'
		print ''
		print ''

	else: 
		print 'This will search for emails in the education section...'
		search = sys.argv[1]
		skip = ''
		if len(sys.argv) > 2:
			skip = sys.argv[2]
		totalamount = get_total(search)
		scrape_emails(search, totalamount, breaking, skip)




