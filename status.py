from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import sh1106

import time
import subprocess
import utils

from datetime import datetime
from datetime import timedelta

from PIL import Image, ImageDraw, ImageFont

UPTIME_ICON = "\uf017"
CPU_ICON = "\uf2db"
TEMP_ICON = "\uf2cb"
MEMORY_ICON = "\uf538"
CLOUD_STORAGE_ICON = "\uf0c2"
SD_ICON= "\uf7c2"

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

def draw_text(draw, x, y, text):
	draw.text((x, y), text, fill=255, font=font)

def draw_icon(draw, x, y, icon):
	draw.text((x, y), icon, fill=255, font=icons)

def draw_icon_text(draw, x, y, icon, text):
	draw_icon(draw, x, y, icon)
	draw_text(draw, x + 16, y, text)


def draw_uptime(draw, x, y):
	uptime = utils.get_pretty_timedelta(datetime.now() - startup_time)
	draw_icon_text(draw, x, y, UPTIME_ICON, " " + uptime)

def draw_cpu(draw, x, y):
	cmd = "top -bn1 | grep load | awk '{printf \" %.2f%\", $(NF-2)}'"
	cpu = subprocess.check_output(cmd, shell = True)
	draw_icon_text(draw, x, y, CPU_ICON, str(cpu, 'utf-8'))

def draw_temp(draw, x, y):
	cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
	temp = subprocess.check_output(cmd, shell = True)
	draw_icon_text(draw, x, y, TEMP_ICON, str(temp, 'utf-8'))

def draw_memory(draw, x, y):
	cmd = "free -m | awk 'NR==2{printf \" %s / %sMB\", $3,$2 }'"
	mem_usage = subprocess.check_output(cmd, shell = True)
	draw_icon_text(draw, x, y, MEMORY_ICON, str(mem_usage, 'utf-8'))

def draw_sd_storage(draw, x, y):
	cmd = "df -h | awk '$NF==\"/\"{printf \" %d / %dGB %s\", $3,$2,$5}'"
	storage = subprocess.check_output(cmd, shell = True)
	draw_icon_text(draw, x, y, SD_ICON, str(storage, 'utf-8'))

def draw_cloud_storage(draw, x, y):
	cmd = "df -h | awk '$NF==\"/srv/dev-disk-by-uuid-48c68453-e0e4-459b-b46d-9fe9ac086466\"{printf \" %d / %dGB %s\", $3,$2,$5}'"
	storage = subprocess.check_output(cmd, shell = True)
	draw_icon_text(draw, x, y, CLOUD_STORAGE_ICON, str(storage, 'utf-8'))

def update(draw):
	update_offset()
	draw.rectangle(device.bounding_box, outline="black", fill="black")

	y = y_offset
	draw_uptime(draw, 0, y)
	y += 16
	draw_cpu(draw, 0, y)
	draw_temp(draw, 80 - 16, y)
	y += 16
	draw_memory(draw, 0, y)
	y += 16
	icon = CLOUD_STORAGE_ICON

	if show_sd_card:
		draw_sd_storage(draw, 0, y)
	else:
		draw_cloud_storage(draw, 0, y)

	switch_counter += 1
	if switch_counter > switch_counter_max:
		switch_counter = 0
		show_sd_card = not show_sd_card

	time.sleep(0.1)

while True:
	with canvas(device) as draw:
		update(draw)