from utils_parser import  parse_word, parse_number, parse_string
from itertools import chain

parse_true = parse_word("true", True)
parse_false = parse_word("false", False)
def parse_null(src):
        for match in chain(
                parse_word("null", None),
                parse_word("~", None)
        )(src):
                yield match
                return

def parse_tags(src):
	for match in chain(
		parse_number,
		parse_string,
		parse_true,
		parse_false,
		parse_null
	):
		yield match
		return
