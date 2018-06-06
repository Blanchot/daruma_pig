# daruma01
# test of luma library

# code below from here: https://media.readthedocs.org/pdf/max7219/stable/max7219.pdf
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)
seg = sevensegment(device)

# write test
seg.text = "HELLO"

