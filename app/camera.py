import json
class Camera():
    def __init__(self, ipaddress, name, id):
        self.ipaddress = ipaddress
        self.name = name
        self.id = id
    def __str__(self):
        return self.id + ":" + self.ipaddres + ":" + self.name
