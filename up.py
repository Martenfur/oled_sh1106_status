import utils
import os 
import sys

sys.argv.pop(0)

filename = utils.get_commands_filename()
utils.append_file_text(filename, " ".join(sys.argv) + "\n")