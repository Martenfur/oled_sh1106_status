import subprocess
import utils
from datetime import datetime

def get_uptime(startup_time):
	uptime = utils.get_pretty_timedelta(datetime.now() - startup_time)
	return uptime

def get_cpu():
	cmd = "top -bn1 | grep load | awk '{printf \" %.2f%%\", $(NF-2)}'"
	cpu = subprocess.check_output(cmd, shell = True)
	return str(cpu, 'utf-8')

def get_temp():
	cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
	temp = subprocess.check_output(cmd, shell = True)
	return str(temp, 'utf-8')

def get_memory():
	cmd = "free -m | awk 'NR==2{printf \" %s / %sMB\", $3,$2 }'"
	mem_usage = subprocess.check_output(cmd, shell = True)
	return str(mem_usage, 'utf-8')

def get_sd_storage():
	cmd = "df -h | awk '$NF==\"/\"{printf \" %d / %dGB %s\", $3,$2,$5}'"
	storage = subprocess.check_output(cmd, shell = True)
	return str(storage, 'utf-8')

def get_cloud_storage():
	cmd = "df -h | awk '$NF==\"/srv/dev-disk-by-uuid-11777043-4443-4612-880c-90a5d0efd236\"{printf \" %d / %dGB %s\", $3,$2,$5}'"
	storage = subprocess.check_output(cmd, shell = True)
	return str(storage, 'utf-8')
