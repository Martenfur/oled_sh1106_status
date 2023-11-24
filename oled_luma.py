from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import sh1106

from PIL import Image, ImageDraw, ImageFont

def run(update_func):
	global font, icons, draw
	font = ImageFont.truetype('PixelOperator.ttf', 16)
	icons = ImageFont.truetype('lineawesome-webfont.ttf', 16)

	serial = i2c(port=1, address=0x3C)
	device = sh1106(serial, width=128, height=64, rotate=2)

	while True:
		with canvas(device) as draw:
			update_func(draw)

def draw_text(draw, x, y, text):
	draw.text((x, y), text, fill=255, font=font)

def draw_icon(draw, x, y, icon):
	draw.text((x, y), icon, fill=255, font=icons)

def draw_icon_text(draw, x, y, icon, text):
	draw_icon(draw, x, y, icon)
	draw_text(draw, x + 16, y, text)
