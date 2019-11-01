# Parse string into integer
def parseInt(line):
  dig = 0
  for c in line: dig = dig*10 + ord(c)-48
  return dig

def decToBin(decnum):
  decnum = parseInt(decnum)
  binum = ''
  while decnum > 0:
    binum = str(decnum % 2) + binum
    decnum //= 2
  return binum

infile = open('set.txt')
outfile = open('binset.txt', 'w')
for line in infile:
  arr = line.split(' ')
  arr[len(arr)-1] = arr[len(arr)-1][0:-1]
  for i in range(len(arr)-1): outfile.write(decToBin(arr[i + 1]) + ' ');
  outfile.write(decToBin(arr[len(arr)-1]) + '\n')
outfile.close()
infile.close()
