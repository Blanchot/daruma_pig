# Plutus02 Tests

# luma.led_matrix setup
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=2)
seg = sevensegment(device)

import requests, json
from time import sleep

neb_amt = 28.741 # NEBL's owned
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
    #euroPrice = float(nbBTC) * float(btcEuro) #(don't need to turn nbBTC to float again!)
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
  str1 = '{} {}'.format(euroPrice,change24)
  str2 = str(round((neb_amt * euroPrice),2))
  #euroPrice = '{:0.2f}'.format(nbEUR) #for display
  if len(str1) >= 0: # and len(str1) <= 10:
    str1 = '{:<8}'.format(str1) # don't know if I need the 's' 
    print(str1)
    str2 = '{:<8}'.format(str2)
    print(str2)
    total_str = str1 + str2
    return total_str
  else:
    print('str1 too long!')
    return '--------'

while True:
  seg.text = twin_display()
  print() # separator
  sleep(60) # checks once a minute
  #sleep(300) # checks every 5 minutes

'''
Padding Formatting
https://pyformat.info/#string_pad_align
https://www.digitalocean.com/community/tutorials/how-to-use-string-formatters-in-python-3
'{:10}'.format('test') # with spaces
'{:_<10}'.format('test') #with underscores

'''

