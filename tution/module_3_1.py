calls = 0

def count_calls():
    global calls
    calls += 1

def string_info(list_):
    a = list_.__len__()
    b = list_.upper()
    c = list_.lower()
    list_1 = [a, b, c]
    tuple_  = tuple(list_1)
    count_calls()
    return tuple_


def is_contains(string, list_to_search):
    if string.lower() in (item.lower() for item in list_to_search):
        word = True
        count_calls()
    else:
        word = False
        count_calls()
    return word



print(string_info('Tri'))
print(is_contains('Frst', ['frst', 'scnd', 'thrd']))
print(calls)