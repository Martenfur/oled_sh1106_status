from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import sh1106

import time
import subprocess

from PIL import Image, ImageDraw, ImageFont

serial = i2c(port=1, address=0x3C)
device = sh1106(serial, width=128, height=64, rotate=2)

font = ImageFont.truetype('PixelOperator.ttf', 16)
icons = ImageFont.truetype('lineawesome-webfont.ttf', 16)


show_sd_card = True
switch_counter = 0
switch_counter_max = 3

while True:
	with canvas(device) as draw:
		draw.rectangle(device.bounding_box, outline="black", fill="black")
		cmd = "uptime | awk ' { print $1 }'"
		Uptime = subprocess.check_output(cmd, shell = True )

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

		# Uptime.
		draw.text((0, 0), "\uf017", fill=255, font=icons)
		draw.text((16, 0), " " + str(Uptime,'utf-8'), fill=255, font=font)

		# CPU.
		draw.text((0, 16), "\uf2db", fill=255, font=icons)
		draw.text((16, 16), str(CPU,'utf-8'), fill=255, font=font)

		# Temps.
		draw.text((80 - 16, 16), "\uf2cb", fill=255, font=icons)
		draw.text((80, 16), str(Temp,'utf-8') , fill=255, font=font)

		# Memory.
		draw.text((0, 32), "\uf538", fill=255, font=icons)
		draw.text((16, 32), str(MemUsage,'utf-8'), fill=255, font=font)

		# Disk.
		icon = "\uf0c2"
		if show_sd_card:
			icon = "\uf7c2"
		draw.text((0, 48), icon, fill=255, font=icons)
		draw.text((16, 48), str(Disk,'utf-8'), fill=255, font=font)

	switch_counter += 1
	if switch_counter > switch_counter_max:
		switch_counter = 0
		show_sd_card = not show_sd_card

	time.sleep(0.1)


