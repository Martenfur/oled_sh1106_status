import utils
import time

def read_command():
	filename = utils.get_commands_filename()
	text = utils.read_file_text(filename)

	# Clearing the file.
	utils.write_file_text(filename, "")

	return text

while True:
	text = read_command()
	if text != "":
			print("text: " + text)
	time.sleep(0.1)



