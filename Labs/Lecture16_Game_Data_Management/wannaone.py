import json

class Boy():
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y


team = []

with open('wannaone_data.json', 'r') as f:
    wannaone_data = json.load(f)

for data in wannaone_data:
    boy = Boy(data['name'], data['x'] * 100 / 3, data['y'] * 100 / 3)
    team.append(boy)

