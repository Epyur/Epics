my_dict = {'Everest': 8849, 'K2': 8611, 'Manaslu': 8163}
print(my_dict)
print(my_dict["Everest"])
print(my_dict.get('Kilimangaro', ' Not available'))
my_dict.update({'Broad Peak': 8051})
print(my_dict)
del my_dict['K2']

print(my_dict)
a=my_dict.pop('Manaslu')
print(a)
print(my_dict)

my_set = {1, 1, 2, 3, 5, 'line'}
print(my_set)
print(my_set.add(12))
print(my_set.add(0))
print(my_set)
my_set.remove(3)
print(my_set)