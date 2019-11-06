from pword import parse_word, sequence
from pstr import parse_string
from pnum import parse_number
from itertools import chain

parse_left_square_brace = parse_word("[")
parse_right_square_brace = parse_word("]")
parse_comma = parse_word(",")

def parse_list_element(src):
        for match in chain(
                parse_string(src),
                parse_number(src)
        ):
                yield match
                return

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

parse_empty_sequence_flow = sequence(parse_left_square_brace, parse_right_square_brace)

def parse_sequence_flow(src):
	for _, src in parse_empty_sequence_flow(src):
		yield [], src
		return
	for (_, items, _), src in sequence(
		parse_left_square_brace,
		parse_comma_separated_list_elements,
		parse_right_square_brace
	)(src):
		yield items, src
