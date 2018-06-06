# daruma01
# b01 first test: getting and displaying Neblio price

# code below from here: https://media.readthedocs.org/pdf/max7219/stable/max7219.pdf
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)
seg = sevensegment(device)

import requests, json
from time import sleep

# Using coinmarketcap.com
#INFO: https://coinmarketcap.com/api/

URL = 'https://api.coinmarketcap.com/v2/ticker/1955/?convert=EUR'

# write test
#seg.text = "HELLO"

def getNeblioPrice():
  try:
    r = requests.get(URL)
    nprice = json.loads(r.text)['data']['quotes']['EUR']['price']
    nprice = str(nprice)
    nprice = nprice[0:5] #slice nprice
    print(nprice) #can comment this out later
    return nprice
  except requests.ConnectionError:
    print("Error querying Coinmarketcap API")

while True:
  seg.text = getNeblioPrice()
  sleep(60)


'''
# Sample code that works:

def getBitcoinPrice():
  URL = 'https://www.bitstamp.net/api/ticker/'
  try:
    r = requests.get(URL)
    priceFloat = float(json.loads(r.text)['last'])
    return priceFloat
  except requests.ConnectionError:
    print("Error querying Bitstamp API")

while True:
  print("Bitstamp last price: $" + str(getBitcoinPrice()) + "/BTC")
  sleep(5)

'''

