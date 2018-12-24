from sys import stderr

_INFO = "\033[94m" # blue
_WARNING = "\033[93m" # yellow
_ERROR = "\033[91m" # red
_END = "\033[0m"

def info(text):
	print(f"{_INFO}[INFO]{_END} {text}")

def warning(text):
	print(f"{_WARNING}[WARNING]{_END} {text}")

def error(text):
	print(f"{_ERROR}[ERROR]{_END} {text}", file = stderr)
