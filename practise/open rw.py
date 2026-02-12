#1
with open('data.txt' , 'w', encoding='utf-8') as f:
    f.write('Привет\n')
    f.write('что то пишу\n')
with open('data.txt' , 'r', encoding='utf-8') as f:
    t=f.read()
    print(t)

#2
with open('file.txt' , 'w', encoding='utf-8') as f:
    for i in range(1,11):
        f.write(str(i)+'\n')
with open('file.txt' , 'r', encoding='utf-8') as f:
    c=f.read()
    print(c)

#3
with open('names.txt' , 'w', encoding='utf-8') as f:
    f.write('Zhaniya\n')
    f.write('Magzhan\n')
    f.write('Arman\n')

with open('names.txt' , 'r', encoding='utf-8') as f:
    n=f.read()
    print(n.upper())

#1csv
import csv
with open('data.csv' , 'w', encoding='utf-8') as f:
    f.write('jknhibuy\n')
    f.write('вар\n')
with open('data.csv' , 'r', encoding='utf-8') as f:
    s=f.read()
    print(s)

#2
with open('file.csv' , 'w', encoding='utf-8') as f:
    for i in range(1,11):
        f.write(str(i)+'\n')
with open('file.csv' , 'r', encoding='utf-8') as f:
    c=f.read()
    print(c)

#3
with open('names.csv', 'w', encoding='utf-8') as f:
    f.write('azamat\n')
    f.write('mukhtar\n')
    f.write('aida\n')
with open('names.csv', 'r', encoding='utf-8') as f:
    a=f.read()
    print(a.upper())

#4
d=[{"name": "Zhaniya", "age": 17, "grade": 5},
    {"name": "Magzhan", "age": 18, "grade": 4},
    {"name": "Arman", "age": 16, "grade": 5}]
with open('std.csv', 'w', encoding='utf-8', newline='') as f:
    a=['name','age','grade']
    b= csv.DictWriter(f, fieldnames=a)
    b.writeheader()
    b.writerows(d)