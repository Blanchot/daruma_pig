# daruma01
# b04 change nprice slice because of OverflowError
# See neblioRequestTest.py in Pythonista for testing formatting 

#OverflowError: Devices capabilities insufficient for value: '5.485 -10.0'

# code below from here: https://media.readthedocs.org/pdf/max7219/stable/max7219.pdf
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

# Using coinmarketcap.com
#INFO: https://coinmarketcap.com/api/

URL = 'https://api.coinmarketcap.com/v2/ticker/1955/?convert=EUR'

# Formatters for python 3.5:
# https://www.digitalocean.com/community/tutorials/how-to-use-string-formatters-in-python-3

def getNeblioPrice():
  try:
    r = requests.get(URL)
    nprice = json.loads(r.text)['data']['quotes']['EUR']['price']
    n24hrChange = json.loads(r.text)['data']['quotes']['EUR']['percent_change_24h']
    changeIndicator(nprice) #send current price to changeIndicator as float
    nprice = str(nprice) #need to do this here, can't figure how to slice float to four digits with formatting
    print('Current price: ', nprice) #can comment this out later
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


def changeIndicator(nprice):
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
  seg.text = getNeblioPrice()
  print() # separator
  #sleep(60) # checks once a minute
  sleep(300) # checks every 5 minutes


