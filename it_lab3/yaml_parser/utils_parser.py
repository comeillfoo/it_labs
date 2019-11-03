import re
from itertools import chain
#from mapping_parser import parse_mapping, parse_mappings
#from tag_parser import parse_tags

re_number = re.compile(r"(-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*(.*)", re.DOTALL)

def parse_number(src):
	match = re_number.match(src)
	if match is not None:
		number, src = match.groups()
		yield eval(number), src

re_string = re.compile(r"('(?:[^\\']|\\['\\/bfnrt]|\\u[0-9a-fA-F]{4})*?')\s*(.*)", re.DOTALL)

def parse_string(src):
	match = re_string.match(src)
	if match is not None:
		string, src = match.groups()
		yield eval(string), src

re_scalar = re.compile(r"([a-zA-Z_а-яА-ЯёЁ]+)\s*(.*)", re.DOTALL)

def parse_scalar(src):
	match = re_scalar.match(src)
	if match is not None:
		scalar, src = match.groups()
		yield str(scalar), src

def parse_word(word, value=None):
	l = len(word)
	def result(src):
		if src.startswith(word):
			yield value, src[l:].lstrip()
	result.__name__ = "parse_%s" % word
	return result

def sequence(*funcs):
	if (len(funcs) == 0):
		def result(src):
			yield (), src
		return result
	def result(src):
		for arg1, src in funcs[0](src):
			for others, src in sequence(*funcs[1:])(src):
				yield (arg1,) + others, src
	return result

parse_comma = parse_word(",")

def parse_value(src):
	for match in chain(
		parse_scalar(src),
		parse_tags(src),
		parse_mappings(src),
		parse_sequence(src)
	):
		yield match
		return

parse_key = parse_scalar
