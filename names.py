def test_function():
    def inner_function():
        print('Я в области видимости функции test_function()')
    return inner_function()

test_function()
#inner_function() #в таком варианте внутреннюю функцию не вызвать отдельно от внешней функции

# в таком варианте "внутрення" функция может быть применена как внутри другой функции, так и сама по себе
def inner_function_2():
    print('Я в области видимости функции test_function_2()', 'но могу работать и сама по себе')

def test_function_2():
   print("Это работает")
   inner_function_2()

inner_function_2()
test_function_2()