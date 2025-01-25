def apply_all_func(int_list, *functions):
    results = {}

    for fun in functions:
        results.update({fun.__name__: fun(int_list)})
    return results

print(apply_all_func([6, 20, 15, 9], max, min))

print(apply_all_func([6, 20, 15, 9], len, sum, sorted))