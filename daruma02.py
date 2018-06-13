# daruma02 (More accurate quotes: uses Binance for NEBL-BTC and Coinbase BTC-EUR)
# b01 initial submit
# See https://pyformat.info for formatting

# Luma code from here: https://media.readthedocs.org/pdf/max7219/stable/max7219.pdf

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)
seg = sevensegment(device)

import buttonshim

import requests, json
from time import sleep

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
    
    # NEBL price in BTC
    print('1 NEBL (BTC): ',nbBTC)
    
    # Percent change over the last 24 hours
    # print('Change (24hrs): ',nbBTC_change24)
    print('Change (24hrs): {:0.1f}'.format(nbBTC_change24))
    change24 = '{:0.1f}'.format(nbBTC_change24) #str truncated for display
    
    
    # Send bitcoin price and 24hr change to euro converter
    eurPrice = getBTC_euro(nbBTC)
    
    txt = '{} {}'.format(eurPrice,change24)
    return txt
    
  except requests.ConnectionError:
    print("Error querying Binance API")

# convert BTC to Euro, send to changeIndicator, return complete text for display
def getBTC_euro(nbBTC):
  try:
    r = requests.get(URL_2)
    btcEuro = json.loads(r.text)['data']['amount']
    
    # NEBL price in EUR
    nbEUR = float(nbBTC) * float(btcEuro)
    print('1 NEBL (EUR): {:0.2f}'.format(nbEUR))
    eurPrice = '{:0.2f}'.format(nbEUR) #for display
    
    # Send to changeIndicator rounded to 2 decimal places (for ButtonShim)
    eurRound = round(nbEUR,2)
    #changeIndicator(eurRound)
    
    return eurPrice
    
  except requests.ConnectionError:
    print("Error querying Coinbase API")

def changeIndicator(eurRound):
  #Button SHIM indicator changes if the price diff is more than 1 cent
  global prevPrice
  diff = nprice - prevPrice
  print('Diff since last check: ', str(diff)) #can comment this out later
  if diff >= 0.01:
    buttonshim.set_pixel(0,255,0) #value increasing since last check = green
  elif diff <= -0.01:
    buttonshim.set_pixel(255,0,0) #value decreasing since last check = red
  else:
    buttonshim.set_pixel(0,0,255) #value unchanged since last check  = blue
  prevPrice = nprice

while True:
  seg.text = getNEBL_btc()
  print() # separator
  sleep(60) # checks once a minute
  #sleep(300) # checks every 5 minutes

'''
NOTES

# Formatters for python 3.5:
# https://www.digitalocean.com/community/tutorials/how-to-use-string-formatters-in-python-3

: introduces the format spec
0 enables sign-aware zero-padding for numeric types
.2 sets the precision to 2
f displays the number as a fixed-point number
'''

'''
def getNeblioPrice():
  try:
    nprice = str(nprice) #need to do this here, can't figure how to slice float to four digits with formatting
    nprice = nprice[0:4] #slice nprice
    #nprice = nprice[0:5] #slice nprice was [0:5] but got OverflowError when percent change dropped too much
    
    n24hrChange = json.loads(r.text)['data']['quotes']['EUR']['percent_change_24h']
    print('Percent Change Last 24hr: ', str(n24hrChange)) #can comment this out later
    
    npriceAndChange = nprice + " {0:>4.1f}".format(n24hrChange)
    print(npriceAndChange) #can comment this out later
    #return nprice #nprice only
    return npriceAndChange
    
  except requests.ConnectionError:
    print("Error querying Coinmarketcap API")

'''

