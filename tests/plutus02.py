# Plutus02 Test (for 2 max7219 displays and Blinkt!)

# luma.led_matrix setup
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=2)
seg = sevensegment(device)
device.contrast(50) #set display brightness (int: 0 - 255)

import blinkt
import requests, json
from time import sleep

# for Blinkt brightness, rgb tuples and pixel list
blinkt.set_brightness(0.04)
rise = (0,8,0)
fall = (32,0,0)
same = (0,0,192)
pixels = (0,1,2,3,4,5,6,7)

neb_amt = 52.7072 # NEBL's owned
prevPrice = 0.0

# API's Used
URL_1 = 'https://api.binance.com/api/v1/ticker/24hr?symbol=NEBLBTC' #curr. price in BTC + % change last 24hrs
URL_2 = 'https://api.coinbase.com/v2/prices/spot?currency=EUR' #Convert BTC to Euro

# get current Binance price for NEBL in BTC and percent change over last 24hrs.
def getNEBL_btc():
  try:
    r = requests.get(URL_1)
    nbBTC = json.loads(r.text)['lastPrice']
    nbBTC_change24 = json.loads(r.text)['priceChangePercent']
    
    #convert to floats
    nbBTC = float(nbBTC)
    nbBTC_change24 = float(nbBTC_change24)
    
    # CONSOLE PRINTING
    print('1 NEBL (BTC): ',nbBTC)
    print('Change (24hrs): {:0.1f}'.format(nbBTC_change24))
    
    # Send bitcoin price to euro converter
    euroPrice = getBTC_euro(nbBTC) #this should be a float
    
    # Compile and return text
    # Let's not do this (below) here:
    # change24 = '{:0.1f}'.format(nbBTC_change24) #str truncated for display
    
    return euroPrice, nbBTC_change24 #floats)
    
  except requests.ConnectionError:
    print("Error querying Binance API")

# convert BTC to Euro, send to changeIndicator, return complete text for display
def getBTC_euro(nbBTC):
  try:
    r = requests.get(URL_2)
    btcEuro = json.loads(r.text)['data']['amount']
    euroPrice = nbBTC * float(btcEuro) # NEBL price in EUR
    print('1 NEBL (EUR): {:0.2f}'.format(euroPrice))
    
    '''
    # Send to changeIndicator rounded to 2 decimal places (for ButtonShim)
    eurRound = round(nbEUR,2)
    changeIndicator(eurRound)
    '''
    return euroPrice
    
  except requests.ConnectionError:
    print("Error querying Coinbase API")


def twin_display():
  euroPrice, change24 = getNEBL_btc()
  euroPrice = round(euroPrice,2)
  change24 = round(change24,1)
  str1 = '{:0.2f} {}'.format(euroPrice,change24) #formatting required to properly print euroPrice
  str2 = str(round((neb_amt * euroPrice),2))
  if len(str1) >= 0: # and len(str1) <= 10:
    str1 = '{:<10}'.format(str1) #10 counting the two decimal points
    print(str1)
    str2 = '{:<9}'.format(str2) #9 counting the single decimal point
    print(str2)
    total_str = str1 + str2
    return total_str
  else:
    print('str1 too long!')
    return '--------'


while True:
  seg.text = twin_display()
  print() # separator
  #sleep(60) # checks once a minute
  sleep(300) # checks every 5 minutes

