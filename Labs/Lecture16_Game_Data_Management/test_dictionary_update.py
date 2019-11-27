data = {"name": "Yuri", "x":100, "y":200}

data['name'] = 'Yuna'

print(data)

new_data = {"name": "Jisu", "x":400, "y":900}

data.update(new_data)

print(data)




class Npc:
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y


yuri = Npc('Yuri', 100, 200)

print(yuri.__dict__)

new_data = {"name": "jusu", "x":400, "y":900}

yuri.__dict__.update(new_data)

print(yuri.__dict__)
print(yuri.name, yuri.x, yuri.y)
