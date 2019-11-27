import json

numbers = [1,2,3,4]
numbers_string = json.dumps(numbers)
print(numbers_string)

values_string = '{"x":10, "y":20, "size":4.5}'
values = json.loads(values_string)
print(values)

