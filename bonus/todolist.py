from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
to_do={}
n=1

while True:
    a=input('Add to list:')
    if a=='0':
        break
    to_do[n]=a
    n+=1

def del_a(n:int):
    if n in to_do:
        to_do.pop(n)
        print('deleted')

d=input('number to delete')
for x in d:
    n=int(x)
    print(del_a(n))
print(to_do)