import re #импор библиотеки регулярных выражений
from itertools import chain #возвращает по одному элементу из итераторов в порядке очереди

#генератор функций, находящих символы терминаторы
def parse_word(word, value=None):
	l = len(word)
	def result(src):
		if src.startswith(word):
			yield value, src[l:].lstrip()
	result.__name__ = "parse_%s" % word
	return result

# рекурсивная функция связывающая аргументы в формате ИЛИ
# (принимает переменное число функций)
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

# регулярка для чисел любых форматов: положительные и отрицательные целые,
# с плавающей точкой в эсконенциальной и обычных форматах
re_number = re.compile(r"(-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*(.*)", re.DOTALL)
# парсим число
def parse_number(src):
	match = re_number.match(src)
	if match is not None:
		number, src = match.groups()
		yield eval(number), src
		
# регулярка для строк в двойных кавычках
re_string = re.compile(r'("(?:[^\\"]|\\["\\/bfnrt]|\\u[0-9a-fA-F]{4})*?")\s*(.*)', re.DOTALL)
# парсим строку
def parse_string(src):
	match = re_string.match(src)
	if match is not None:
		string, src = match.groups()
		yield eval(string), src
		
# функции поиска данных символов
parse_left_curly_brace = parse_word('{')
parse_right_curly_brace = parse_word('}')
parse_spaced_colon = parse_word(': ')
parse_word_null = parse_word('null', None)
parse_tilde = parse_word('~', None)
parse_true = parse_word('true', True)
parse_false = parse_word('false', False)
parse_comma = parse_word(',')
# функция парсит пустую последовательность отображения
parse_empty_mappings = sequence(parse_left_curly_brace, parse_right_curly_brace)
# функция парсит любые записи null, кроме пустой строки
def parse_null(src):
	for match in chain(
		parse_word_null(src),
		parse_tilde(src)
	):
		yield match
		return
	
# функция парсинга строкового представления отображения
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
		
# функция парсинга элемента ключ: значение
def parse_mapping(src):
	for (key, _, value), src in sequence(
		parse_key,
		parse_spaced_colon,
		parse_value
	)(src):
		yield {key: value}, src
		
# функция парсит элементы словаря, разделённых запятыми
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
		
# функция парсит значения элемента словаря
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
	
# функция парсит ключи словаря
# (должны быть ещё скаляры, но их не получилось реализовать) :((
parse_key = parse_string
# функция, находящие символы, подобные указанным выше
parse_left_square_brace = parse_word("[")
parse_right_square_brace = parse_word("]")
parse_comma = parse_word(",")
# функция парсит элементы последовательностей
parse_list_element = parse_value
# функция парсит последовательность элементов последовательности, разделённых запятой
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
		
# функция парсинга пустой последовательности
parse_empty_sequence_flow = sequence(parse_left_square_brace, parse_right_square_brace)
# функция парсинга последовательности строчного формата
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
		
# регулярка для отлова элементов последовательностей блочного типа
re_sequence_line = re.compile(r'^- (?:.*)$', re.MULTILINE)
# функция удаления в многострочных строках лидирующих пробелов
def multi_lstrip(src):
    copy_src = ''
    for line in src.split(chr(10)):
        line = line.lstrip()
        copy_src += line + chr(10)
    return copy_src

# ручное приведение блочного формата последовательностей к строчному
def parse_sequence_block(src):
    src = multi_lstrip(src)
    glist = re.findall(re_sequence_line, src)
    lines = []
    for line in glist:
        lines += [line[2:]]
    src = '[' + ', '.join(lines) + ']'
    return parse_sequence_flow(src)

# регулярка для отлова пар ключ: значение блочного формата
re_mappings_line = re.compile(r'^(?:.*): (?:.*)$', re.MULTILINE)
# функция приводит блочный тип отображений к строковому
def parse_mappings_block(src):
    src = multi_lstrip(src)
    src = '{' + ', '.join(re.findall(re_mappings_line, src)) + '}'
    return parse_mappings_flow(src)

# функция парсинга возможных элементов .ya?ml документа
def parse_root(src):
    for match in chain(
        parse_sequence_block(src),
        parse_mappings_block(src),
        parse_mappings_flow(src),
        parse_sequence_flow(src),
        parse_string(src),
        parse_number(src),
        parse_true(src),
        parse_false(src),
        parse_null(src),
    ):
        yield match
        return

# функция парсинга строки
# (выкидывает исключения при отсутствия совпадений или наличия не распознанного текста)
def parse(src):
    match = list(parse_root(src))
    if len(match) != 1:
        raise ValueError("not a valid YAML notation")    
    result, src = match[0]
    if src.strip():
        raise ValueError("not a valid YAML notation")
    return result

# рекурсивная функция конвертации объектов python  в json
# проверяем на совпадение типов и поэлементно формируем строку по правилам json
def convert(src):
    if type(src) == type([]):
        out = '\t[' + chr(10)
        for el in src[:-1]:
            out += '\t\t' + convert(el) + ',' + chr(10)
        out += '\t\t' + convert(src[-1]) + chr(10) + '\t\t]'
        return out
    elif type(src) == type({}):
        out = '{' + chr(10)
        for el in src:
            out += '\t\t' + convert(el) + ': ' + convert(src[el]) + ',' + chr(10)
        out = out[:-2] + chr(10) + '\t}'
        return out
    elif type(src) == type(''):
        return '\"' + src + '\"'
    elif (type(src) == type(1)) or (type(src) == type(1.000)):
        return str(src)
    elif type(src) == type(True):
        if src == True:
            return "true"
        else: return "false"
    elif type(src) == type(None):
        return "null"

# стандартная процедура открытия файлов на чтение и запись
with open('timetable.yml', encoding='utf-8') as f:
        s = f.read()
with open('timetable.json', 'w', encoding='utf-8') as f:
        f.write(convert(parse(s)))
