name = input("Code du fichier : ")
source = open(name + '.txt', 'r')
dest = open(name + '_reversed.txt', 'w')
lines = []

for line in source:
	lines.append(line)

last = len(lines) - 1
if lines[last][-1] is not "\n":
	lines[last] += "\n"

for i in range(last, -1, -1):
	dest.write(lines[i])

source.close()
dest.close()