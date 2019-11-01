# Словарь сопоставляющий каждой тетраде, записанной в обратном порядке, её шестнадцатеричный эквивалент
tetra = {'0000':'0', '1000':'1','0100':'2','1100':'3','0010':'4','1010':'5','0110':'6','1110':'7',
         '0001':'8', '1001':'9','0101':'A','1101':'B','0011':'C','1011':'D','0111':'E','1111':'F',}

# Функция, переводящая строку в число
def parseInt(line):
  dig = 0
  for c in line: dig = dig*10 + ord(c)-48
  return dig

# Функция переводит из -10 сс. в 10 сс.
def negaDecToDec(ndecnum):
  # разворачиваем строковое представление числа
  ndecnum = ndecnum[::-1]
  dec = 1
  buffer = 0
  for c in ndecnum:
    n = parseInt(c)
    buffer += n*dec
    dec *= -10
  return str(buffer)

# Функция, переводящая из двоичной в шестнадцатеричной по упрощённому алгоритму
def binToHex(binum):
  # разворачиваем строковое представление двоичного числа
  binum = binum[::-1]
  # дополняем строку нулями до длины кратной 4 с избытком
  if len(binum) % 4 > 0: binum = binum + '0' * ((len(binum) % 4)+4)
  hexnum = ''
  for i in range(len(binum)//4):
    # последовательно срезаем по 4 цифры и переводим
    hexnum = tetra[binum[4*i:4*(i + 1)]] + hexnum
  # убираем лидирующий нуль
  if hexnum[0] == '0': hexnum = hexnum[1:]
  return hexnum

infile = open('input29.txt')
outfile = open('output29.txt', 'w')
# проходясь по каждой строке входного файла параллельно осуществляем перевод и форматированный вывод в выходной файл
for line in infile:
  arr = line.split(' ')
  arr[len(arr)-1] = arr[len(arr)-1][0:-1]
  if arr[0] == '-10':
    outfile.write('-10 -> 10: ')
    for i in range(len(arr)-3): outfile.write(arr[i + 2] + ' -> ' + negaDecToDec(arr[i + 2]) + ' | ');
    outfile.write(arr[-1] + ' -> ' + negaDecToDec(arr[-1]) + '\n')
  else:
    outfile.write('2 -> 16: ') 
    for i in range(len(arr)-3): outfile.write(arr[i + 2] + ' -> ' + binToHex(arr[i + 2]) + ' | ');
    outfile.write(arr[-1] + ' -> ' + binToHex(arr[-1]) + '\n')
outfile.close()
infile.close() 
    
