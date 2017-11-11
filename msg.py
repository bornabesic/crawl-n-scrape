from sys import stderr

class TermColor:
    INFO = "\033[94m" # blue
    WARNING = "\033[93m" # yellow
    ERROR = "\033[91m" # red
    END = "\033[0m"

def info(text):
	print("{}[INFO]{} {}".format(TermColor.INFO, TermColor.END, text))

def warning(text):
	print("{}[WARNING]{} {}".format(TermColor.WARNING, TermColor.END, text))

def error(text):
	print("{}[ERROR]{} {}".format(TermColor.ERROR, TermColor.END, text), file = stderr)