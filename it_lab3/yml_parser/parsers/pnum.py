import re

re_number = re.compile(r"(-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*(.*)", re.DOTALL)

def parse_number(src):
	match = re_number.match(src)
	if match is not None:
		number, src = match.groups()
		yield eval(number), src
