from utils.utils import *

DEBUG = False # Must be False for production

# Fields for the URL
BASE_URL = 'https://www.skyscanner.es'
URL = BASE_URL + '/transporte/vuelos'
DEPARTURE_AIRPORT = 'bio'
ARRIVAL_AIRPORTS = list(airport_dict.keys())[1:]
EARLIEST_DATE = '230801' # Use as a first date to iterate over
PAYLOAD = '?adults=1' # Other fields

# Other variables
LATEST_BACK_DATE = '230820'
MAX_ATTEMPTS = 3

def get_trips(driver, dep_ap, arr_ap, dep_date=EARLIEST_DATE, back_date=LATEST_BACK_DATE):
	trip = Trip(dep_ap, arr_ap, dep_date)
	attempts = 0
	while(int(trip.date) < int(back_date)):
		try:
			url = set_url(URL, trip.departure_ap, trip.arrival_ap, trip.date, PAYLOAD)
			driver.get(url)
			trip.get_data(driver)
			print(trip.__str__())
		except Exception as e:
			attempts += 1
			print('\033[91mError: could not get information for date {} (attempt {}/{})\033[0m'.format(trip.date, attempts, MAX_ATTEMPTS))
			print(e) if DEBUG else None
			if attempts >= MAX_ATTEMPTS:
				print('Skipping date {}'.format(trip.date))
				trip.date = increase_date(trip.date)
				attempts = 0
			driver.quit()
			wait(1, 10)
			driver = init_driver()
			continue

		trip.write_to_file()
		trip.date = increase_date(trip.date)
		attempts = 0
		wait()

def main():
	# One-way trips
	for arr_airport in ARRIVAL_AIRPORTS:
		driver = init_driver()
		get_trips(driver, DEPARTURE_AIRPORT, arr_airport)
		driver.quit()
	
	# Back trips
	for arr_airport in ARRIVAL_AIRPORTS:
		driver = init_driver()
		get_trips(driver, arr_airport, DEPARTURE_AIRPORT)
		driver.quit()

if __name__ == '__main__':
	main()
