import unicodedata
from fastapi import FastAPI, HTTPException
from starlette.responses import HTMLResponse

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
        self.registration_date=date.today()
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

@app.get('/task1')
def task1():
    u = User(1, " john doe ", "John@Example.COM")
    return {'result':u}

@app.get('/task2')
def task2():
    u1= User.from_string("2, Alice Wonderland , alice@wonder.com")
    return {'result':u1}

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
@app.get('/task3')
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
    return {'result':expensive}

#6
from datetime import datetime, date
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
u2 = User(1, " john doe ", "John@Example.COM")

@app.post('/task6/action')
def log_write():
    Logger.log_action(u2,'BUY',p2,'logs.txt')
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


@app.get('/task7,8')
def order():
    ord = Order(1,u2,[])
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
    return {'result':list(price_stream(prod))}


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
    Order(1,u2,[p1]),
    Order(2,u1,[p2]),
    Order(3,u2,[p1,p2])
]
ordi=OrderIterator(lst)
@app.get('/task10')
def next_ord():
    try:
        order=next(ordi)
        return {'result':str(order)}
    except StopIteration:
        raise HTTPException(404,'No more orders')

import numpy as np
#11
products=[p1,p2]
arr= np.array([x.price for x in products])
@app.get('/task11')
def arr_price():
    return {'prices':arr}

#12
arr = np.array([1200, 25, 450])
r=(float(np.mean(arr)),float(np.median(arr)))
@app.get('/task12')
def mean_med_arr():
    return {'result':r}

#13
@app.get('/task13')
def normalize():
    arr1 = np.array([1200.0, 25.0, 450.0])
    r=(arr1-arr1.min())/(arr1.max()-arr1.min())
    return {'normalized':r}

#14
products = [Product(1,"Laptop",1200.0,"Electronics"), Product(2,"T-Shirt",20.0,"Clothing")]
arr= np.array([x.category for x in products])
@app.get('/task14')
def category():
    return {'categories':arr}

#15
arr = np.array(["Electronics","Clothing","Electronics"])
res=np.unique(arr)
@app.get('/tas15')
def unique_arr():
    return {'result': res}

#16
products = [Product(1,"Laptop",1200.0,"Electronics"), Product(2,"Mouse",25.0,"Electronics"), Product(3,"Monitor",450.0,"Electronics")]
prices=np.array([x.price for x in products])
avg=np.mean(prices)
r=[p for p in products if p.price>avg]
@app.get('/task16')
def more_than_avg():
    return {'result': r}

#17
arr=np.array([1200.0, 25.0, 450.0])
r=arr*0.9
@app.get('/task17')
def sale():
    return {'result': r}
#18
orders = [Order(1,u1,[Product(1,"Laptop",1200.0,"Electronics")]), Order(2,u2,[Product(2,"Mouse",25.0,"Electronics"), Product(1,"Laptop",1200.0,"Electronics")])]
s= [sum(p.price for p in order.products) for order in orders]
@app.get('/task18')
def sum_of_price_month():
    return {'result':s}

#19
@app.get('/task19')
def average():
    arr = np.array([1200.0, 1225.0])
    r=np.mean(arr)
    return {'result':r}

#20
arr=np.array([1200.0, 900.0, 1500.0])
r=np.where(arr>1000)
@app.get('/task20')
def index():
    return {'result':r}


#21
import pandas as pd
@app.get('/task21', response_class=HTMLResponse)
def df_users():
    users = [User(1, "John Doe", "john@example.com"),
             User(2, "Alice", "alice@example.com")]
    df=pd.DataFrame([{
        'id':u.id,
        'name':u.name ,
        'email':u.email,
        'registration_date':u.registration_date
    }for u in users])
    return df.to_html(index=False)

#22
@app.get('/task22', response_class=HTMLResponse)
def df_product():
    products = [Product(1, "Laptop", 1200.0, "Electronics"), Product(2, "T-Shirt", 20.0, "Clothing")]
    df = pd.DataFrame([{
        'id': p.id,
        'name': p.name,
        'category': p.category,
        'price': p.price
    } for p in products])
    return df.to_html(index=False)

#23
@app.get('/task23', response_class=HTMLResponse)
def orders():
    udf=pd.DataFrame({
        'id':[1,2],
        'name':['John','Alice']
    })
    ordf=pd.DataFrame({
        'order_id':[101,102],
        'user_id':[1,2],
        'total':[1200,25]
    })
    df=pd.merge(ordf,udf,left_on='user_id',right_on='id')
    df=df.rename(columns={'name':'user_name'})
    return df[['order_id','user_name','total']].to_html(index=False)

#24
@app.get('/task24', response_class=HTMLResponse)
def more_than_value():
    data={
        'order_id':[101,102],
        'user_name':['John','Alice'],
        'total':[1200,25]
    }
    df=pd.DataFrame(data)
    r=df[df['total'] > 100]
    return r.to_html(index=False)

#25
@app.get('/task25', response_class=HTMLResponse)
def group():
    data = {
        'order_id': [101, 103,102],
        'user_name': ['John', 'John' ,'Alice'],
        'total': [1200,500, 25]
    }
    df = pd.DataFrame(data)
    r=df.groupby('user_name')['total'].sum()
    r=r.rename(columns={'total':'total_sum'})
    return r.to_html(index=False)

#26
@app.get('/task26',response_class=HTMLResponse)
def mean_groupby():
    data = {
        'order_id': [101, 103, 102],
        'user_name': ['John', 'John', 'Alice'],
        'total': [1200, 500, 25]
    }
    df = pd.DataFrame(data)
    r=df.groupby('user_name')['total'].mean()
    r=r.rename(columns={'total':'mean_total'})
    return r.to_html(index=False)

#27
@app.get('/task27',response_class=HTMLResponse)
def count_orders():
    data = {
        'order_id': [101, 103, 102],
        'user_name': ['John', 'John', 'Alice'],
        'total': [1200, 500, 25]
    }
    df = pd.DataFrame(data)
    r=df.groupby('user_name')['order_id'].count()
    r=r.rename(columns={'order_id':'order_count'})
    return r.to_html(index=False)

#28
@app.get('/task28',response_class=HTMLResponse)
def mean_category():
    data={
        'id':[1,2,3],
        'name':['Laptop','Mouse','Shirt'],
        'category':['Electronics','Electronics','Clothing'],
        'price':[1200,25,20]
    }
    df = pd.DataFrame(data)
    r = df.groupby('category')['price'].mean()
    r = r.rename(columns={'price': 'mean_price'})
    return r.to_html(index=False)

#29
@app.get('/task29',response_class=HTMLResponse)
def new_column():
    data = {
        'id': [1, 2],
        'name': ['Laptop', 'Mouse'],
        'price': [1200, 25]
    }
    df = pd.DataFrame(data)
    df['discounted_price']=df['price']*0.9
    return df.to_html(index=False)

#30
@app.get('/task30',response_class=HTMLResponse)
def sort_val():
    data = {
        'id': [1, 2,3],
        'name': ['Laptop', 'Mouse','Monitor'],
        'price': [1200, 25,450]
    }
    df = pd.DataFrame(data)
    df=df.sort_values(by='price',ascending=False)
    return df.to_html(index=False)

#31
@app.get('/task31',response_class=HTMLResponse)
def quantiy():
    data = {
        'order_id': [101, 102],
        'product_name': ['Laptop', 'Mouse'],
        'price': [1200, 25]
    }
    df = pd.DataFrame(data)
    df['quantity'] = df.groupby('order_id')['product_name'].transform('count')
    return df.to_html(index=False)

#32
@app.get('/task32',response_class=HTMLResponse)
def total_pr():
    data = {
        'order_id': [101, 102],
        'product_name': ['Laptop', 'Mouse'],
        'price': [1200, 25],
        'quantity':[1,2]
    }
    df = pd.DataFrame(data)
    df['total_price']=df['quantity']*df['price']
    return df.to_html(index=False)

#33
@app.get('/task33',response_class=HTMLResponse)
def only_elec():
    data = {
        'product_name': ['Laptop', 'Mouse','T-Shirt'],
        'category':['Electronics','Electronics','Clothing'],
        'price': [1200, 25,20]
    }
    df = pd.DataFrame(data)
    df=df[df['category']=='Electronics']
    return df.to_html(index=False)

#34
@app.get('/task34',response_class=HTMLResponse)
def count_categ():
    data = {
        'product_name': ['Laptop', 'Mouse','T-Shirt'],
        'category':['Electronics','Electronics','Clothing'],
        'price': [1200, 25,20]
    }
    df = pd.DataFrame(data)
    r=df.groupby('category').size().reset_index(name='count')
    return r.to_html(index=False)

#35
@app.get('/task35',response_class=HTMLResponse)
def mean_categ():
    data = {
        'product_name': ['Laptop', 'Mouse','T-Shirt'],
        'category':['Electronics','Electronics','Clothing'],
        'price': [1200, 25,20]
    }
    df = pd.DataFrame(data)
    r=df.groupby('category')['price'].mean().reset_index()
    r=r.rename(columns={'price':'mean_price'})
    return r.to_html(index=False)

#36
@app.get('/task36',response_class=HTMLResponse)
def sorted():
    data = {
        'order_id':[101,102,103],
        'total_price':[20,1200,25]
    }
    df = pd.DataFrame(data)
    r=df.sort_values(by='total_price',ascending=False)
    return r.to_html(index=False)

#37
@app.get('/task37',response_class=HTMLResponse)
def top3():
    data = {
        'order_id':[101,102,103,104],
        'total_price':[1200,50,500,1500]
    }
    df = pd.DataFrame(data)
    r = df.sort_values(by='total_price', ascending=False).head(3)
    return r.to_html(index=False)
#38
@app.get('/task38', response_class=HTMLResponse)
def merge_data():
    udf=pd.DataFrame({
        'user_id':[1,2],
        'user_name':['John','Alice']
    })
    ordf=pd.DataFrame({
        'order_id':[101,102],
        'user_id':[1,2],
        'total':[1200,50]
    })
    df=pd.merge(ordf,udf,on='user_id')
    return df[['order_id','user_name','total']].to_html(index=False)

#39
@app.get('/task39',response_class=HTMLResponse)
def mean():
    data = {
        'user_name': ['John', 'John', 'Alice'],
        'total': [1200, 500, 50]
    }
    df = pd.DataFrame(data)
    r=df.groupby('user_name')['total'].mean()
    r=r.rename(columns={'total':'mean_total'})
    return r.to_html(index=False)

#40
@app.get('/task40',response_class=HTMLResponse)
def count_ord():
    data = {
        'user_name': ['John', 'John', 'Alice'],
        'order_id': [101,102,103]
    }
    df = pd.DataFrame(data)
    r=df.groupby('user_name')['order_id'].count().reset_index()
    r=r.rename(columns={'order_id':'order_count'})
    return r.to_html(index=False)

#41
@app.get('/task41',response_class=HTMLResponse)
def max_ord():
    data = {
        'user_name': ['John', 'John', 'Alice'],
        'total_price': [1200, 500, 50]
    }
    df = pd.DataFrame(data)
    r=df.groupby('user_name')['total_price'].max().reset_index()
    r=r.rename(columns={'total_price':'max_order'})
    return r.to_html(index=False)

#42
@app.get('/task42',response_class=HTMLResponse)
def unq_cat():
    data = {
        'user_name': ['John', 'John', 'John', 'Alice'],
        'category':["Electronics", "Electronics", "Clothing", "Clothing"]
    }
    df = pd.DataFrame(data)
    r=df.groupby('user_name')['category'].nunique().reset_index()
    r=r.rename(columns={'category':'unique_categories'})
    return r.to_html(index=False)

#43
@app.get('/task43',response_class=HTMLResponse)
def vip():
    data = {
        'user_name': ['John','Alice'],
        'total_sum':[1700,25]
    }
    df = pd.DataFrame(data)
    df['VIP']=df['total_price']>1000
    return df.to_html(index=False)


#44
app.get('/task44',response_class=HTMLResponse)
def sort_total_mean():
    data = {
        'user_name': ['John','Alice','Bob'],
        'total_sum':[1700,25,1700],
        'mean_total':[850,25,600]
    }
    df = pd.DataFrame(data)
    r = df.sort_values(by=['total_sum','mean_total'], ascending=[False,True])
    return r.to_html(index=False)

#45
app.get('/task45',response_class=HTMLResponse)
def all():
    df = pd.DataFrame({
        "user_name": ["John", "John", "Alice"],
        "order_id": [101, 103, 102],
        "total_price": [1200, 500, 25],
        "category": ["Electronics", "Clothing", "Clothing"]
    })
    total_ord=df.groupby('user_name')['order_id'].count()
    total_sum=df.groupby('user_name')['total_price'].sum()
    mean_total=df.groupby('user_name')['total_price'].mean()
    max_ord=df.groupby('user_name')['total_price'].max()
    unq=df.groupby('user_name')['category'].nunique()
    r = pd.DataFrame({
        "total_orders": total_ord,
        "total_sum": total_sum,
        "mean_total": mean_total,
        "max_order": max_ord,
        "unique_categories": unq
    }).reset_index()
    r['VIP']=r['total_sum']>1000
    return r.to_html(index=False)