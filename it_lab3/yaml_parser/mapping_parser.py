import utils_parser

parse_left_curly_brace = parse_word("{")
parse_right_curly_brace = parse_word("}")
parse_empty_mappings = sequence(parse_left_curly_brace, parse_right_curly_brace)

def parse_mappings(src):
	for _, src in parse_empty_mappings(src):
		yield {}, src
		return
	for (_, items, _), src in sequence(
		parse_left_curly_brace,
		parse_comma_separated_mappings,
		parse_right_curly_brace
	)(src):
		yield items, src

parse_spaced_colon = parse_word(": ")

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