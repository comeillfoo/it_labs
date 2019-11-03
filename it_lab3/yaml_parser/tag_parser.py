import utils_parser

parse_true = parse_word("true", True)
parse_false = parse_word("false", False)
parse_null = parse_word("\n", None) # TODO: define null value

def parse_tags(src):
	for match in chain(
		parse_number,
		parse_string
		parse_true,
		parse_false,
		parse_null
	):
		yield match
		return
