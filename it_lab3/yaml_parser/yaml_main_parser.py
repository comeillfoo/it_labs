#!/usr/bin/python3
import re
import utils_parser
import mapping_parser
import sequence_parser

def parse_root(src):
	for match in chain(
		parse_mappings(src),
		parse_mapping(src),
		parse_sequence(src),
		parse_scalars(src)
	):
		yield match
		return

def parse(s):
	s = s.strip()
	match = list(parse_root(s))
	if len(match) != 1:
		raise ValueError("not a valid YAML code")
	result, src = match[0]
	if src.strip():
		raise ValueError("not a valid YAML notation")
	return result