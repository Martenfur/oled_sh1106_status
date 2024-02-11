import time

from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import sh1106

from PIL import Image, ImageDraw, ImageFont

def run(update_func):
	global font, icons, draw
	font = ImageFont.truetype('PixelOperator.ttf', 16)
	icons = ImageFont.truetype('lineawesome-webfont.ttf', 16)

	while True:
		try:
			serial = i2c(port=1, address=0x3C)
			device = sh1106(serial, width=128, height=64, rotate=2)

			while True:
				with canvas(device) as draw:
					draw.rectangle(device.bounding_box, outline="black", fill="black")
					update_func()
		except (IOError, OSError) as e:
			print("i/o error caught: " + str(e))
			time.sleep(1)

def draw_text(x, y, text):
	draw.text((x, y), text, fill=255, font=font)

def draw_icon(x, y, icon):
	draw.text((x, y), icon, fill=255, font=icons)

def draw_icon_text(x, y, icon, text):
	draw_icon(x, y, icon)
	draw_text(x + 16, y, text)
