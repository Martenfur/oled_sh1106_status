import time
import subprocess
import utils

import oled_luma as display

from datetime import datetime
from datetime import timedelta

UPTIME_ICON = "\uf017"
CPU_ICON = "\uf2db"
TEMP_ICON = "\uf2cb"
MEMORY_ICON = "\uf538"
CLOUD_STORAGE_ICON = "\uf0c2"
SD_ICON= "\uf7c2"

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


def draw_uptime(x, y):
	uptime = utils.get_pretty_timedelta(datetime.now() - startup_time)
	display.draw_icon_text(x, y, UPTIME_ICON, " " + uptime)

def draw_cpu(x, y):
	cmd = "top -bn1 | grep load | awk '{printf \" %.2f%\", $(NF-2)}'"
	cpu = subprocess.check_output(cmd, shell = True)
	display.draw_icon_text(x, y, CPU_ICON, str(cpu, 'utf-8'))

def draw_temp(x, y):
	cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
	temp = subprocess.check_output(cmd, shell = True)
	display.draw_icon_text(x, y, TEMP_ICON, str(temp, 'utf-8'))

def draw_memory(x, y):
	cmd = "free -m | awk 'NR==2{printf \" %s / %sMB\", $3,$2 }'"
	mem_usage = subprocess.check_output(cmd, shell = True)
	display.draw_icon_text(x, y, MEMORY_ICON, str(mem_usage, 'utf-8'))

def draw_sd_storage(x, y):
	cmd = "df -h | awk '$NF==\"/\"{printf \" %d / %dGB %s\", $3,$2,$5}'"
	storage = subprocess.check_output(cmd, shell = True)
	display.draw_icon_text(x, y, SD_ICON, str(storage, 'utf-8'))

def draw_cloud_storage(x, y):
	cmd = "df -h | awk '$NF==\"/srv/dev-disk-by-uuid-48c68453-e0e4-459b-b46d-9fe9ac086466\"{printf \" %d / %dGB %s\", $3,$2,$5}'"
	storage = subprocess.check_output(cmd, shell = True)
	display.draw_icon_text(x, y, CLOUD_STORAGE_ICON, str(storage, 'utf-8'))

def update():
	global show_sd_card, switch_counter, switch_counter_max

	update_offset()

	y = y_offset
	draw_uptime(0, y)
	y += 16
	#draw_cpu(0, y)
	draw_temp(80 - 16, y)
	y += 16
	draw_memory(0, y)
	y += 16

	if show_sd_card:
		draw_sd_storage(0, y)
	else:
		draw_cloud_storage(0, y)

	switch_counter += 1
	if switch_counter > switch_counter_max:
		switch_counter = 0
		show_sd_card = not show_sd_card

	time.sleep(0.1)

display.run(update)