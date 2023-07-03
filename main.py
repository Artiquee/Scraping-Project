import time
import db
import script

while True:
    # Scrape data from page
    cars = script.scrape_data()

    # Check cars in db
    db.check_db(cars)

    # Check if all cars in db are available
    db.is_available(cars)

    time.sleep(600)