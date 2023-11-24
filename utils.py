import os
import time 

# Files =========================================================================

def get_commands_filename():
	return os.path.dirname(os.path.realpath(__file__)) + "/.commands"

# Reads all text from a file even if it is busy.
def read_file_text(path):
	if not os.path.isfile(path):
		return ""

	for iter in range(0, 10):
		try:
			with open(path, "r") as file:
				return file.read()
		except (OSError, PermissionError, IOError) as e:
			pass
		time.sleep(0.1)

	return ""

# Writes text to a file even if it is busy, overriding all previous text.
def write_file_text(path, text):
	for iter in range(0, 10):
		try:
			with open(path, "w") as file:
				file.write(text)
				return
		except (OSError, PermissionError, IOError) as e:
			pass
		time.sleep(0.1)

# Files =========================================================================


# Uptime ========================================================================

def get_pretty_timedelta(tdelta):
		s = tdelta.seconds
		hours, remainder = divmod(s, 3600)
		minutes, seconds = divmod(remainder, 60)
		return str(tdelta.days) + ' days {:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

# Uptime ========================================================================


