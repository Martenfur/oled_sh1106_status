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
screen_change_interval = 20
status_messages = {}

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
			status_messages[message] = {
				"time": datetime.now(),
				"message": message
			}
		if command == "remove" and message in status_messages:
			removed_message = status_messages[message]
			del status_messages[message]
			log_message = str(datetime.now()) + "\n" + message + ": " + (utils.get_pretty_timedelta(datetime.now() - removed_message["time"]).replace(" days " , ":"))
			log_message += "\n=======================\n"
			utils.append_file_text(utils.get_logs_filename(), log_message)

tasks_scroll_y = 0
tasks_scroll_max_y = 0
tasks_scroll_direction = 1
tasks_max = 2

def update_status_screen():
	global tasks_scroll_y, tasks_scroll_max_y, tasks_scroll_direction, tasks_max

	if len(status_messages) == 0:
		display.draw_icon_text(26, 24, NO_TASKS_ICON, " no tasks")
		return

	y = 0
	if len(status_messages) > tasks_max:
		tasks_scroll_max_y = (len(status_messages) - tasks_max) * 32
		tasks_scroll_y += tasks_scroll_direction * 2
		if tasks_scroll_y < 0:
			tasks_scroll_y = 0
			tasks_scroll_direction *= -1
		
		if tasks_scroll_y > tasks_scroll_max_y:
			tasks_scroll_y = tasks_scroll_max_y
			tasks_scroll_direction *= -1

		y = -tasks_scroll_y

	for key in reversed(status_messages):
		display.draw_icon_text(0, y, TASK_ICON, " " + key)
		display.draw_icon_text(48, y + 16, UPTIME_ICON, " " + utils.get_pretty_short_timedelta(datetime.now() - status_messages[key]["time"]))
		y += 32



def update_info_screen():
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




def update():
	global screen_id, screen_change_counter, screen_change_interval
	
	try:
		update_status_messages()

		if screen_id == 0:
			update_info_screen()
		else:
			update_status_screen()
	except (IOError, OSError) as e:
		print("i/o error caught: " + str(e))

	screen_change_counter += 1
	if screen_change_counter >= screen_change_interval:
		screen_change_counter = 0
		screen_id += 1
		if screen_id > max_screen_id:
			screen_id = 0
	time.sleep(0.1)


display.run(update)