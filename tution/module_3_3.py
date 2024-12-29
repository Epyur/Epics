def print_params(*params, a, b, c):
    print(*params, a, b, c)


values_list = [1, "text", False]
values_dict = {'a': 2, 'b': 4, 'c': 1}
print_params(*values_list, **values_dict)

def print_params_2(c, d, e):
    print(c, d, e)

values_list_2 = [54.32, 'Строка']
print_params_2(*values_list_2, 42)