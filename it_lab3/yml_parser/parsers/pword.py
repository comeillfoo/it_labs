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
