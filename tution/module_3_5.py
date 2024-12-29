def get_multiplied_digits(number):
    str_number = str(number)

    frst = int(str_number[0])
    print(frst)
    if frst == 0:
        return 1
    if len(str_number) > 1:
        return frst * get_multiplied_digits(int(str_number[1:]))
    else:
        return frst

result = get_multiplied_digits(402030)

print(result)