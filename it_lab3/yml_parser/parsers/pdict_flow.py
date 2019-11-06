from parr_flow import parse_sequence_flow
from pnum import parse_number
from pstr import parse_string
from itertools import chain
from pword import parse_word, sequence

parse_left_curly_brace = parse_word("{")
parse_right_curly_brace = parse_word("}")
parse_empty_mappings = sequence(parse_left_curly_brace, parse_right_curly_brace)
parse_spaced_colon = parse_word(": ")
parse_word_null = parse_word("null", None)
parse_tilde = parse_word("~", None)
parse_true = parse_word("true", True)
parse_false = parse_word("false", False)
parse_comma = parse_word(",")

def parse_null(src):
	for match in chain(
		parse_word_null(src),
		parse_tilde(src)
	):
		yield match
		return

def parse_mappings_flow(src):
	for _, src in parse_empty_mappings(src):
		yield {}, src
		return
	for (_, items, _), src in sequence(
		parse_left_curly_brace,
		parse_comma_separated_mappings,
		parse_right_curly_brace
	)(src):
		yield items, src

def parse_mapping(src):
	for (key, _, value), src in sequence(
		parse_key,
		parse_spaced_colon,
		parse_value
	)(src):
		yield {key: value}, src

def parse_comma_separated_mappings(src):
	for (mapping, _, mappings), src in sequence(
		parse_mapping,
		parse_comma,
		parse_comma_separated_mappings
	)(src):
		mapping.update(mappings)
		yield mapping, src
		return
	for mapping, src in parse_mapping(src):
		yield mapping, src

def parse_value(src):
	for match in chain(
		parse_string(src),
		parse_number(src),
		parse_mappings_flow(src),
		parse_sequence_flow(src),
		parse_true(src),
		parse_false(src),
		parse_null(src)
	):
		yield match
		return

parse_key = parse_string
