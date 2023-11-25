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
SD_ICON = "\uf7c2"
TASK_ICON = "\uf0c6"
NO_TASKS_ICON = "\uf0f4"


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


screen_id = 0
max_screen_id = 1
screen_change_counter = 0
screen_change_interval = 10
status_messages = []

def update_status_messages():
	global status_messages

	filename = utils.get_commands_filename()
	text = utils.read_file_text(filename)

	if text == "":
		return

	# Clearing the file.
	utils.write_file_text(filename, "")

	lines = text.splitlines()

	for line in lines:
		words = line.split()
		if len(words) < 2:
			return
		command = words[0]
		message = ' '.join(words[1:])
		if command == "add":
			if message not in status_messages:
				status_messages.append(message)
		if command == "remove" and message in status_messages:
			status_messages.remove(message)


def update_status_screen():
	if len(status_messages) == 0:
		display.draw_icon_text(26, 24, NO_TASKS_ICON, " no tasks")

	y = 0
	for status in reversed(status_messages):
		display.draw_icon_text(0, y, TASK_ICON, " " + status)
		y += 16


def update_info_screen():
	global show_sd_card, switch_counter, switch_counter_max

	update_status_messages()
	
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




def update():
	global screen_id, screen_change_counter, screen_change_interval

	if screen_id == 0:
		update_info_screen()
	else:
		update_status_screen()

	screen_change_counter += 1
	if screen_change_counter >= screen_change_interval:
		screen_change_counter = 0
		screen_id += 1
		if screen_id > max_screen_id:
			screen_id = 0
	
	time.sleep(0.1)


display.run(update)