import requests
from bs4 import BeautifulSoup
from time import sleep
from random import uniform, randint
#selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


base = 'https://newyork.craigslist.org'
section = '/search/edu'
driver = webdriver.Chrome(executable_path="chromedriver")
mainWin = driver.window_handles[0]
breaking = False

def hover(element):  
    hov = ActionChains(driver).move_to_element(element)
    hov.perform()

def wait(a, b):
	rand=uniform(a, b)
	sleep(rand)

for a in range(10):
	if breaking == True: 
		print 'There are Captcha now'
		driver.close()
		break

	page_number = a*100
	page = '?=%s'%page_number
	if a == 0:
		page = ''

	r = requests.get(base+section+page)
	soup = BeautifulSoup(r.content, 'html.parser')
	links = soup.find_all('a', attrs={'class':'hdrlnk'})

	for link in links:
		if breaking == True: 
			break

		try:
			print 'trying next link'
			driver.get(base+link.get('href'))
			# click the reply button to get email
			try:
				button =  driver.find_element_by_class_name('reply_button')
				button.click()
				try:
					captcha = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_id('g-recaptcha'))
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
						

						try:
							driver.switch_to_window(mainWin)
							html = driver.page_source
							s = BeautifulSoup(html, 'html.parser')
							iframes = s.find_all("iframe", attrs={'title': 'recaptcha challenge'})
							secFrame = iframes[0].get('name')

							if secFrame !=  None:
								breaking = True

						except:
							continue

						driver.switch_to_window(mainWin)
				except:
					driver.switch_to_window(mainWin)

				e = WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_class_name('anonemail'))
				email = e.text
				print email
			except:
				print 'Capcha skipped'
				continue
		except:

			continue