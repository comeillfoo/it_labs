import re

re_string = re.compile(r'("(?:[^\\"]|\\["\\/bfnrt]|\\u[0-9a-fA-F]{4})*?")\s*(.*)', re.DOTALL)

def parse_string(src):
	match = re_string.match(src)
	if match is not None:
		string, src = match.groups()
		yield eval(string), src
