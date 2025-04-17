
def matcher(a, b):
    for i in a:
        for x in b:
            if i == x:
                print('Yes')
            else:
                print('No')
                print(i)
                print(x)


matcher('D1', 'D3')


if 'В' in 'Г2':
    print('j')
else:
    print('s')