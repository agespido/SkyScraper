from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import geckodriver_autoinstaller
import warnings 
from time import sleep
import random
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

airport_dict = {
	'bio': 'BILBAO',
	'bkkt': 'BANGKOK',
	'cgki': 'JAKARTA',
	'kulm': 'KUALA LUMPUR',
	'sgn': 'SAIGON'
}

class Trip:
	def __init__(self, _departure_ap, _arrival_ap, _date):
		self.departure_ap = _departure_ap
		self.arrival_ap = _arrival_ap
		self.date = _date
		self.price = ''
		self.dep_time = ''
		self.arr_time = ''
		self.duration = ''
		self.connections = ''

	def __str__(self):
		return '\033[92mFlight {} -> {} on {} at {} (duration {}) => {}\033[0m'.format(airport_dict[self.departure_ap], airport_dict[self.arrival_ap], self.date, self.dep_time, self.duration, self.price)

	def get_data(self, driver):
		wait(4)
		WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dayview-first-result"]/div/div[3]/div/div/div/span')))
		self.price = driver.find_element(By.XPATH, '//*[@id="dayview-first-result"]/div/div[3]/div/div/div/span').text
		self.dep_time = driver.find_element(By.XPATH, '//*[@id="dayview-first-result"]/div/div[1]/div/div[1]/div[3]/div/div[2]/div[1]/span[1]/div/span').text
		self.duration = driver.find_element(By.XPATH, '//*[@id="dayview-first-result"]/div/div[1]/div/div[1]/div[3]/div/div[2]/div[2]/span').text
		self.arr_time = driver.find_element(By.XPATH, '//*[@id="dayview-first-result"]/div/div[1]/div/div[1]/div[3]/div/div[2]/div[3]/span[1]/div/span[1]').text
		self.connections = driver.find_element(By.XPATH, '//*[@id="dayview-first-result"]/div/div[1]/div/div[1]/div[3]/div/div[2]/div[2]/div[2]/span').text

	def write_to_file(self):
		fname = 'travel_all_over_the_world.csv'
		# Write file header if file does not exist
		if not os.path.isfile(fname):
			f = open(fname, 'w')
			f.write('Date, Departure Airport, Departure Time, Arrival Airport, Arrival Time, Flight Duration, Number of Connections, Price\n')
		else:
			f = open(fname, 'a')
		f.write('{}, {}, {}, {}, {}, {}, {}, {}\n'.format(self.date, airport_dict[self.departure_ap], self.dep_time, airport_dict[self.arrival_ap], self.arr_time, self.duration, self.connections, self.price))
		f.close()
def set_url(base_url, departure_airport, arrival_airport, oneway_date, payload):
	return '{}/{}/{}/{}{}'.format(base_url, departure_airport, arrival_airport, oneway_date, payload)

def wait(min = 2, max = 4):
	if max <= min:
		max = min + 1
	sleep(random.uniform(min, max))

def increase_date(date):
	# if the last two characters are greater than 31, increase the first two characters by 1
	if int(date[-2:]) >= 31:
		date = str(int((int(date) + 100) / 100) * 100) # Add 1 month
	if int(date[-4:-2]) >= 12:
		date = str(int((int(date) + 10000) / 10000) * 10000 + 1000) # Add 1 year
	return str(int(date) + 1)

def init_driver():
	warnings.filterwarnings("ignore", category=DeprecationWarning) # Ignore deprecation warnings
	geckodriver_autoinstaller.install()
	options = Options()
	options.headless = True
	cap = DesiredCapabilities().FIREFOX
	cap["marionette"] = True
	driver = webdriver.Firefox(capabilities=cap, options=options)
	return driver
