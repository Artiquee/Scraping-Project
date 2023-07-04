import re
import requests
from bs4 import BeautifulSoup

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def scrape_data():
    url = 'https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&country.import.usa.not=0&price.currency=1&abroad.not=0&custom.not=1&damage.not=0&page=0&size=100'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    titles = [re.search(r"(.+)\s+в", x['title']).group(1) for x in soup.find_all('a', {'data-template-v': "6"})]
    link = soup.find_all('a', {'class': 'address'})
    links = [x['href'] for x in link]
    price = soup.find_all('span', {'data-currency': 'USD'})
    prices = [x.text for x in price]
    mileage = [x.text for x in soup.find_all('li', {'class': 'item-char js-race'})]
    locations = [x.text for x in soup.find_all('li', {'class': 'item-char view-location js-location'})]
    image = [x['src'] for x in soup.find_all('img', {'class': 'outline m-auto'})]
    car_Id = [re.search(r"\d+(?=.html)", x).group() for x in links]

    return [{'Id': car_Id[i], 'title': titles[i], 'link': links[i], 'price': prices[i],
             'location': locations[i], 'mileage': mileage[i], 'img': image[i]} for i in range(len(links))]


def scrape_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = [x['src'] for x in soup.find_all('img', {'class': 'outline m-auto'}) if 'youtube' not in x['src']][:5]
    try:
        vin = soup.find('script', {'data-model-name': 'Sequoia'})['data-bidfax-pathname']
        vin = 'https://auto.ria.com/uk'+vin
        if not vin:
            vin = soup.find('a', {'class': 'unlink size16'})['href']
    except:
        vin = ''
    return images, vin


def scrape_usa_images(vin):
    vin = re.search(r'vin-(\w+)\.html', vin).group(1)
    url = 'https://www.google.com/search'
    params = {
        'q': f'site:bid.cars {vin}',
        'num': 10
    }
    session = requests.Session()
    session.headers['User-Agent'] = "User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    response = session.get(url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [x.get('href') for x in soup.find_all('a') if 'https://bid.cars' in x['href']]

    try:
        match = re.search(r'(https://bid\.cars/[^\s&]+)', links[0]).group(1)
        splits = match.split('/')
        images = [f'https://mercury.bid.cars/{splits[5]}/{splits[6]}-{x}.jpg' for x in range(1, 6)]
        return images
    except:
        return None
