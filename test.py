url = 'https://bid.cars/ua/lot/1-48486629/2013-Toyota-Sequoia-5TDBW5G10DS092202'
url2 = 'https://mercury.bid.cars/1-48486629/2013-Toyota-Sequoia-5TDBW5G10DS092202-1.jpg'
splits = url.split('/')
url3 = f'https://mercury.bid.cars/{splits[5]}/{splits[6]}-1.jpg'
print(url3)