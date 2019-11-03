from itertools import chain
import utils_parser
import mapping_parser

parse_left_square_brace = parse_word("[")
parse_right_square_brace = parse_word("]")

def parse_list_element(src):
	for match in chain(
		parse_scalar(src),
		parse_mappings(src),
		parse_mapping(src),
		parse_sequence(src),
		parse_tags(src)
	):
		yield match
		return

parse_spaced_dash = parse_word("- ")
parse_newline = parse_word("\n")

def parse_dash_separated_sequence(src):
	for (_, element, _, elements), src in sequence(
		parse_spaced_dash,
		parse_list_element,
		parse_newline,
		parse_dash_separated_sequence
	)(src):
		yield [element] + elements, src
		return
	for element, src in parse_list_element(src):
		yield [element], src

def parse_comma_separated_list_elements(src):
	for (element, _, elements), src in sequence(
		parse_list_element,
		parse_comma,
		parse_comma_separated_list_elements
	)(src):
		yield [element] + elements, src
		return
	for element, src in parse_list_element(src):
		yield [element], src

parse_empty_comma_separated_sequence = sequence(parse_left_square_brace, parse_right_square_brace)

def parse_comma_separated_sequence(src):
	for _, src in parse_empty_comma_separated_sequence(src):
		yield [], src
		return
	for (_, items, _), src in sequence(
		parse_left_square_brace,
		parse_comma_separated_list_elements,
		parse_right_square_brace
	)(src):
		yield items, src

def parse_sequence(src):
	for match in chain(
		parse_dash_separated_sequence(src),
		parse_comma_separated_sequence(src)
	):
		yield match
		return