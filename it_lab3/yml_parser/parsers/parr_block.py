from pword import parse_word, sequence
from pstr import parse_string
from pnum import parse_number
from itertools import chain

parse_spaced_dash = parse_word("-")

def parse_list_element(src):
        for match in chain(
                parse_string(src),
                parse_number(src)
        ):
                yield match
                return

def parse_sequence_block(src):
	for (_, element, elements), src in sequence(
                parse_spaced_dash,
		parse_list_element,
		parse_sequence_block
	)(src):
		yield [element] + elements, src
		return
	for element, src in parse_list_element(src):
		yield [element], src
