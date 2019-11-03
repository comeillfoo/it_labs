import re
from utils_parser import parse_scalar
from mapping_parser import parse_mappings, parse_mapping 
from sequence_parser import parse_sequence
from itertools import chain

def parse_root(src):
	for match in chain(
		parse_mappings(src),
		parse_mapping(src),
		parse_sequence(src),
		parse_scalar(src)
	):
		yield match
		return

def parse(s):
	s = s.strip()
	match = list(parse_root(s))
	if len(match) != 1:
		raise ValueError("not a valid YAML notation")
	result, src = match[0]
	if src.strip():
		raise ValueError("not a valid YAML notation")
	return result

f = open("timetable.yml", 'r')
s = f.read()
print(parse(s))
f.close()
