from fastapi import FastAPI, HTTPException
app = FastAPI()
@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI is running"}

#1,2
class User:
    def __init__(self,id:int, name:str,email:str):
        self._id=id
        self._name=name.strip().title()
        if '@' not in email:
            raise ValueError
        self._email = email.strip().lower()
    def __str__(self):
        return f"User(id={self._id}, name='{self._name}', email='{self._email}')"
    def __del__(self):
        return f"User {self._name} deleted"
    @classmethod
    def from_string(cls,data:str):
        p=[x.strip() for x in data.split(',')]
        if len(p)!=3:
            raise ValueError
        id=int(p[0])
        name=p[1]
        email=p[2]
        return cls(id,name,email)

@app.post('/task1')
def task1():
    u = User(1, " john doe ", "John@Example.COM")
    return u

@app.post('/task2')
def task2():
    u1= User.from_string("2, Alice Wonderland , alice@wonder.com")
    return u1

#3
class Product:
    def __init__(self,id:int,name:str,price:float,category:str):
        self.id=id
        self.name=name
        self.price=price
        self.category=category
    def __str__(self):
        return f"Product(id={self.id},name='{self.name}',price={self.price}, category='{self.category}')"
    def  __eq__(self,other):
        if not isinstance(other,Product):
            return False
        return self.id==other.id
    def __hash__(self):
        return hash(self.id)
    def to_dict(self):
        return {
            'id': self.id,
            'name':self.name,
            'price':self.price,
            'category':self.category
        }
@app.post('/task3')
def task3():
    pr=Product(1,'Laptop',1200.0,'electronic')
    return pr.to_dict()

#4,5
class Inventory:
    def __init__(self):
        self.products = {}
    def add_product(self,product: Product):
        self.products[product.id]=Product
    def remove_product(self,product_id: int):
        self.products.pop(product_id,None)
    def get_product(self,product_id: int):
        return self.products.get(product_id)
    def get_all_product(self):
        return list(self.products.values())
    def unique_products(self):
        return set(self.products.values())
    def to_dict(self):
        return self.products.copy()
    def filter_by_price(self, min_price:float)->list[Product]:
        r=[x for x in self.products.values() if (lambda y: y.price>=min_price)(x)]
        return r


@app.post('/task4,5')
def add_pr():
    inv = Inventory()
    inv.add_product(Product(1, "Laptop", 1200.0, "Electronics"))
    inv.add_product(Product(2, "Mouse", 25.0, "Electronics"))
    expensive=inv.filter_by_price(100.0)
    return expensive

#6
from datetime import datetime
class Logger:
    @staticmethod
    def log_action(user: User, action: str, product: Product, filename: str):
        timestamp=datetime.now()
        l=f"{timestamp};{user._id};{action};{product.id}/n"
        with open(filename,'a') as f:
            f.write(l)

    @staticmethod
    def read_logs(filename: str):
        logs=[]
        with open(filename,'r') as f:
            for l in f:
                t,u_id,act,p_id= l.strip().split(';')
                logs.append({
                    'timestamp':t,
                    'user_id':u_id,
                    'action':act,
                    'product_id':p_id
                })
        return logs
p2=Product(1, "Laptop", 1200.0, "Electronics")
p1=Product(2, "Mouse", 25.0, "Electronics")
u1=User.from_string("2, Alice Wonderland , alice@wonder.com")
u = User(1, " john doe ", "John@Example.COM")

@app.post('/task6/action')
def log_write():
    Logger.log_action(u,'BUY',p2,'logs.txt')
    Logger.log_action(u1,'BUY',p1,'logs.txt')
    return {'information is written'}

@app.get('/task6/read')
def get_log():
    return Logger.read_logs('logs.txt')

#7,8
from typing import List
class Order:
    def __init__(self,id:int,user:User,products:List[Product]):
        self.id=id
        self.user=user
        self.products=products if products else []
    def add_product(self,product:Product):
        self.products.append(product)
    def remove_product(self,product_id:int):
        self.products=[p for p in self.products if p.id!=product_id]
    def total_price(self):
        s=sum(p.price for p in self.products)
        return s
    def most_expensive_products(self,n:int):
        ex=sorted(self.products, key=lambda p: p.price,reverse=True)[:n]
        return ex
    def __str__(self):
        product=','.join([p.name for p in self.products])
        return f"Order(id={self.id},user={self.user._id}, products=[{product}])"


@app.post('/task7,8')
def order():
    ord = Order(1,u,[])
    ord.add_product(p2)
    ord.add_product(p1)
    return {
        'order': ord,
        'summa': ord.total_price(),
        'expensive': ord.most_expensive_products(1)
    }

#9
def price_stream(products):
    for p in products:
        yield p.price
prod=[p2,p1]
@app.get('/task9')
def get_price():
    return {list(price_stream(prod))}


#10
class OrderIterator:
    def __init__(self,orders):
        self.orders=orders
        self._index=0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index<len(self.orders):
            order=self.orders[self._index]
            self._index+=1
            return order
        else:
            raise StopIteration
lst=[
    Order(1,u,[p1]),
    Order(2,u1,[p2]),
    Order(3,u,[p1,p2])
]
ordi=OrderIterator(lst)
@app.get('/task10')
def next_ord():
    try:
        order=next(ordi)
        return {str(order)}
    except StopIteration:
        raise HTTPException(404,'No more orders')

