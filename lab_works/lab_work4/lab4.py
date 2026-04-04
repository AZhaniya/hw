#6
from datetime import datetime
class Event:
    def __init__(self,type:str,data:dict):
        self.type=type
        self.data=data
        self.timestamp=datetime.now()
    def __str__(self):
        return f"Event(type= '{self.type}', data={self.data}, timestamp='{self.timestamp}'"
e = Event("ATTACK", {"damage": 20})
print(e)

#4,5,18
class Inventory:
    def __init__(self):
        self._items:Dict[int,Item]={}
    def add_item(self,item: Item):
        self._items[item.id]= item
    def remove_item(self ,item_id: int):
        self._items.pop(item_id,None)
    def get_items(self) -> list[Item]:
        return list(self._items.values())
    def unique_items(self)-> set[Item]:
        return set(self._items.values())
    def to_dict(self) -> dict[int, Item]:
        return self._items.copy()
    def get_strong_items(self,min_power:int)->list[Item]:
        r=lambda x: x.power>=min_power
        return [i for i in self._items.values() if r(i)]
    def __iter__(self):
        return iter(self._items.values())

#1,2,7,15,16,17
class Player:
    def __init__(self,id,name,hp):
        self._id=id
        self._name=name.strip().title()
        self._hp=hp if hp>0 else 0
        self._inventory= Inventory()
    def __str__(self):
        return f"Player(id={self._id}, name='{self._name}', hp={self._hp})"
    def __del__(self):
        return f"Player <{self._name}> удалён"
    @classmethod
    def from_string(cls,data:str):
        if not isinstance(data,str):
            raise ValueError
        a=[x.strip() for x in data.split(',')]
        if len(a)!=3:
            raise ValueError
        try:
            id=int(a[0])
            name=a[1]
            hp=int(a[2])
        except:
            raise ValueError
        return cls(id,name,hp)


    @property
    def hp(self):
        return self._hp
    @property
    def inventory(self):
        return self._inventory
    @property
    def id(self):
        return self._id

    def handle_event(self,event:Event):
        if event.type=='ATTACK':
            dmg= event.data.get('damage',0)
            self._hp=max(0,self._hp-dmg)
        elif event.type=='HEAL':
            self._hp+=event.data.get('heal',0)
        else:
            self._inventory.add_item(event.data.get('item'))

p=Player.from_string('2,alice,100')
print(p)


class Warrior(Player):
    def handle_event(self,event:Event):
        if event.type=='ATTACK':
            dmg=int(event.data.get('damage',0)*0.9)
            self._hp=max(0,self._hp-dmg)
        else:
            super().handle_event(event)

class Mage(Player):
    def handle_event(self,event:Event):
        if event.type=='LOOT':
            i=event.data.get('item')
            i.power=int(i.power*1.1)
        super().handle_event(event)
#%%
#3
class Item:
    def __init__(self,id,name,power):
        self.id=id
        self.name=name.strip().title()
        self.power=power

    def __str__(self):
        return f"Item(id={self.id},name='{self.name}',power={self.power})"
    def __eq__(self,other):
        if not isinstance(other,Item):
            return False
        return self.id==other.id
    def __repr__(self):
        return self.__str__()
    def __hash__(self):
        return hash(self.id)

#%%


#%%
#8,9
import ast
class Logger:
    @staticmethod
    def log(event: Event, player: Player, filename: str):
        with open(filename,'a') as f:
            f.write(f"{event.timestamp}; {player.id};{event.type};{event.data}\n")
    @staticmethod
    def read_logs(filename: str) -> list[Event]:
        a=[]
        with open(filename,'r') as f:
            for x in f:
                p=x.strip().split(';')
                if len(p)!=4:
                    continue
                try:
                    e=Event(p[2],ast.literal_eval(p[3]))
                    e.timestamp=p[0]
                    a.append(e)
                except:
                    continue
        return a

#10
class EventIterator:
    def __init__(self,events):
        self.events=events
        self.index=0
    def __iter__(self):
        return self
    def __next__(self):
        if self.index>=len(self.events):
            raise StopIteration
        e=self.events[self.index]
        self.index+=1
        return e

#%%
#11
from typing import List, Dict, Iterator


def damage_stream(events: List[Event])->Iterator[int]:
    for e in events:
        if e.type=='ATTACK':
            yield e.data.get('damage',0)

#%%
#12
import  random

def generate_events(players: list[Player], items: list[Item], n: int) -> list[Event]:
    types=['ATTACK','HEAL','LOOT']
    events=[]
    for y in range(n):
        for p in players:
            t=(lambda x: random.choice(x))(types)
            if t=='ATTACK':
                events.append(Event(t,{'damage': random.randint(5,30),
                                       'player_id':p.id}))
            elif t=='HEAL':
                events.append(Event(t,{'heal': random.randint(5,40)}))
            else:
                events.append(Event(t,{'item': random.choice(items)}))
    return events
#%%
#13
from collections import Counter
def analyze_logs(events:List[Event]):
    total_damage=sum(damage_stream(events))
    event_counts=Counter(e.type for e in events)
    most_common=event_counts.most_common(1)[0][0]
    player_damage = {}
    for e in events:
        if e.type == "ATTACK" and "player_id" in e.data:
            pid = e.data["player_id"]
            player_damage[pid] = player_damage.get(pid, 0) + e.data.get("damage", 0)
    top_player= max(player_damage, key=player_damage.get) if player_damage else None
    return {
        'total_damage':total_damage,
        'top_player': top_player,
        'most_common_event':most_common
    }
#%%
#14
decide_action=lambda x:(
    'HEAL' if x.hp<50 else
    'LOOT' if len(x.inventory.get_items())<2 else
    'ATTACK'
)
#%%
#19
def analyze_inventory(inventories: List[Inventory]):
    alli=set()
    maxx=None
    for j in inventories:
        for i in j:
            alli.add(i)
            if not maxx or i.power>maxx.power:
                maxx=i
    return {
        'unique_items': alli,
        'top_power':maxx
    }
#%%
#20
def main():
    players=[
        Warrior(1,'john',120),
        Mage(2,'alice',100)
    ]
    items=[
        Item(1,'sword',50),
        Item(2,'spear',40),
        Item(3,'bow',30)
    ]
    events=generate_events(players,items,5)
    for i in events:
        for p in players:
            p.handle_event(i)
    for i in events:
        Logger.log(i ,players[0],'log.txt')

        inv=analyze_inventory([p.inventory for p in players])
        most_i=max(players,key=lambda p: len(p.inventory.get_items()))
    logs=Logger.read_logs('log.txt')
    print("Анализ логов:", analyze_logs(logs))
    print("Инвертарь:", inv)
    print("Больше всего предметов:", most_i)


from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII']= False
@app.route("/checking")
def checking():


    items = [
        Item(1, 'sword', 50),
        Item(2, 'spear', 40),
        Item(3, 'bow', 30)
    ]
    p1 = Warrior.from_string("1, john, 120")
    p2 = Mage(2, "alice", 100)
    players = [p1, p2]
    events = generate_events(players, items, 5)
    log_file = "log.txt"
    open(log_file, 'w').close()
    for e in events:
        for p in players:
            p.handle_event(e)
            Logger.log(e, p, log_file)
            print(f"{p} -> {e}")
    inv = analyze_inventory([p.inventory for p in players])
    most_i = max(players, key=lambda p: len(p.inventory.get_items()),default=None)
    logs = Logger.read_logs(log_file)
    stats = analyze_logs(logs)


    return jsonify({
    "Analyze logs": stats,
    "Inventory": {
        "unique_items": [str(i) for i in inv["unique_items"]],
        "top_power": str(inv["top_power"]) if inv["top_power"] else None},
    'The most items': str(most_i)
})
@app.route('/')
def home():
    return "Сервер работает"

if __name__=='__main__':
    app.run(port=8000)
