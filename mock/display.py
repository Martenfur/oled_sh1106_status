
def run(update_func):
	while True:
		update_func()
		print("------------------------------")

def draw_text(x, y, text):
	print(text)

def draw_icon(x, y, icon):
	pass

def draw_icon_text(x, y, icon, text):
	print(text)
