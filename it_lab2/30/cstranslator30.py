# Функция, переводящая строку в число
def parseInt(line):
  dig = 0
  for c in line: dig = dig*10 + ord(c)-48
  return dig

# Начальный список, чисел Фибоначчи
FIBS = [1, 2]

# Функция, переводящая из 10 сс. в двоичную 
def decToBin(decnum):
  # переводим строку в числу
  decnum = parseInt(decnum)
  binum = ''
  while decnum > 0:
    binum = str(decnum % 2) + binum
    decnum //= 2
  binum = list(binum)
  i = len(binum)-4
  # добавляем точечки между разрядами.....
  while i > 0:
    binum.insert(i, '.')
    i-=4
  decnum = ''
  for i in binum: decnum += i;
  return decnum

# Переводит из Фибоначчиевой в десятичную
def zeckToDec(zecknum):
  result = 0
  zecknum = zecknum[::-1]
  for z in range(len(zecknum)):
    if z >= len(FIBS):
      FIBS.append(FIBS[z - 1] + FIBS[z - 2])
    result += FIBS[z] if zecknum[z] != '0' else 0
  return str(result)

infile = open('input30.txt')
outfile = open('output30.txt', 'w')
for line in infile:
  arr = line.split(' ')
  arr[len(arr)-1] = arr[len(arr)-1][0:-1]
  if arr[0] == '10':
    outfile.write('10 -> 2: ')
    for i in range(len(arr)-3): outfile.write(arr[i + 2] + ' -> ' + decToBin(arr[i + 2]) + ' | ');
    outfile.write(arr[len(arr)-1] + ' -> ' + decToBin(arr[len(arr)-1]) + '\n')
  else:
    outfile.write('Fib -> 10: ')
    for i in range(len(arr)-3): outfile.write(arr[i + 2] + ' -> ' + zeckToDec(arr[i + 2]) + ' | ');
    outfile.write(arr[-1] + ' -> ' + zeckToDec(arr[-1]) + '\n')
outfile.close()
infile.close()
