import time
import utils
import os

if os.name == "nt":
	import mock.display as display
	import mock.status_provider as sp
else:
	import linux.display as display
	import linux.status_provider as sp

from datetime import datetime

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

def update():
	global show_sd_card, switch_counter, switch_counter_max

	update_offset()

	y = y_offset
	display.draw_icon_text(0, y, UPTIME_ICON, " " + sp.get_uptime(startup_time))
	y += 16
	display.draw_icon_text(0, y, CPU_ICON, sp.get_cpu())
	display.draw_icon_text(80 - 16, y, TEMP_ICON, sp.get_temp())
	y += 16
	display.draw_icon_text(0, y, MEMORY_ICON, sp.get_memory())
	y += 16

	if show_sd_card:
		display.draw_icon_text(0, y, SD_ICON, sp.get_sd_storage())
	else:
		display.draw_icon_text(0, y, CLOUD_STORAGE_ICON, sp.get_cloud_storage())

	switch_counter += 1
	if switch_counter > switch_counter_max:
		switch_counter = 0
		show_sd_card = not show_sd_card

	time.sleep(0.1)

display.run(update)