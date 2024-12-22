immutable_var = 'Fabinache line is', 1, 1, 2 ,3, 5, 8, 13, 21
print(immutable_var)
immutable_var_2 = 'Fabinache line is', [1, 1, 2 ,3, 5, 8, 13, 18]
immutable_var_2 [1][-1] = 21
print(immutable_var_2)

mutable_var = [1, 1, 2, 3, 5, 8, 13]
print(mutable_var)
mutable_var.append('21,34,55')
print(mutable_var)
mutable_var.remove('21,34,55')
print(mutable_var)
mutable_var.extend([21,34,55])
print(mutable_var)