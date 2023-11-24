from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import sh1106

import time
import subprocess

from datetime import datetime
from datetime import timedelta

from PIL import Image, ImageDraw, ImageFont

# Uptime.
def get_pretty_timedelta(tdelta):
		s = tdelta.seconds
		hours, remainder = divmod(s, 3600)
		minutes, seconds = divmod(remainder, 60)
		return str(tdelta.days) + ' days {:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
# Uptime.



serial = i2c(port=1, address=0x3C)
device = sh1106(serial, width=128, height=64, rotate=2)

font = ImageFont.truetype('PixelOperator.ttf', 16)
icons = ImageFont.truetype('lineawesome-webfont.ttf', 16)


show_sd_card = True
switch_counter = 0
switch_counter_max = 3

startup_time = datetime.now()

# Anti burn-in.
y_offset = 0
y_counter = 0
y_dir = 1

def update_offset():
	global y_offset, y_counter, y_dir
	y_counter += 1
	if y_counter > 600:
		y_offset += y_dir
		y_counter = 0
	if y_offset > 2:
		y_dir *= -1
		y_offset = 2
	if y_offset < 0:
		y_dir *= -1
		y_offset = 0
# Anti burn-in.

while True:
	with canvas(device) as draw:
		update_offset()
		draw.rectangle(device.bounding_box, outline="black", fill="black")

		Uptime = get_pretty_timedelta(datetime.now() - startup_time)

		cmd = "top -bn1 | grep load | awk '{printf \" %.2f%\", $(NF-2)}'"
		CPU = subprocess.check_output(cmd, shell = True )

		cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
		Temp = subprocess.check_output(cmd, shell = True )

		cmd = "free -m | awk 'NR==2{printf \" %s / %sMB\", $3,$2 }'"
		MemUsage = subprocess.check_output(cmd, shell = True )

		if show_sd_card:
			cmd = "df -h | awk '$NF==\"/\"{printf \" %d / %dGB %s\", $3,$2,$5}'"
		else:
			cmd = "df -h | awk '$NF==\"/srv/dev-disk-by-uuid-48c68453-e0e4-459b-b46d-9fe9ac086466\"{printf \" %d / %dGB %s\", $3,$2,$5}'"
		Disk = subprocess.check_output(cmd, shell = True )

		y = y_offset
		# Uptime.
		draw.text((0, y), "\uf017", fill=255, font=icons)
		draw.text((16, y), " " + Uptime, fill=255, font=font)
		y += 16

		# CPU.
		draw.text((0, y), "\uf2db", fill=255, font=icons)
		draw.text((16, y), str(CPU,'utf-8'), fill=255, font=font)

		# Temps.
		draw.text((80 - 16, y), "\uf2cb", fill=255, font=icons)
		draw.text((80, y), str(Temp,'utf-8') , fill=255, font=font)
		y += 16

		# Memory.
		draw.text((0, y), "\uf538", fill=255, font=icons)
		draw.text((16, y), str(MemUsage,'utf-8'), fill=255, font=font)
		y += 16

		# Disk.
		icon = "\uf0c2"
		if show_sd_card:
			icon = "\uf7c2"
		draw.text((0, y), icon, fill=255, font=icons)
		draw.text((16, y), str(Disk,'utf-8'), fill=255, font=font)

	switch_counter += 1
	if switch_counter > switch_counter_max:
		switch_counter = 0
		show_sd_card = not show_sd_card

	time.sleep(0.1)


