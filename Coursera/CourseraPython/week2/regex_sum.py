import re

f = open('regex_sum_42.txt','r')
txt = f.read()
print txt
numbers = re.findall('[0-9]+',txt)
print numbers
converted = []
for num in numbers:
    converted.append(int(num))

print sum(converted)
