from django.db import models
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