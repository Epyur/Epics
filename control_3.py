

data_structure = [
  [1, 2, 3],
  {'a': 4, 'b': 5},
  (6, {'cube': 7, 'drum': 8}),
  "Hello",
  ((), [{(2, 'Urban', ('Urban2', 35))}])
]

def calc_sum(data_structure):
    sum_ = []
    for i in data_structure:
        if isinstance(i, list):
            for x in i:
                if isinstance(x, int):
                    sum_.append(x)
                if isinstance(x, str):
                    sum_.append(len(x))

        if isinstance(i, tuple):
            for a in i:
                if isinstance(a, int):
                    sum_.append(a)
                if isinstance(a, dict):
                    for k in a:
                        if isinstance(k, str):
                            sum_.append(len(k))
                    for v in a.items():
                        for i_2 in v:
                            if isinstance(i_2, int):
                                sum_.append(i_2)
                if isinstance(a, list):
                    for a_2 in a:
                        if isinstance(a_2, set):
                            for a_3 in a_2:
                                if isinstance(a_3, tuple):
                                    for a_4 in a_3:
                                        if isinstance(a_4, int):
                                            sum_.append(a_4)
                                        if isinstance(a_4, str):
                                            sum_.append(len(a_4))
                                        if isinstance(a_4, tuple):
                                            for a_5 in a_4:
                                                if isinstance(a_5, int):
                                                    sum_.append(a_5)
                                                if isinstance(a_5, str):
                                                    sum_.append(len(a_5))


        if isinstance(i, dict):

            for k in i:
                if isinstance(k, str):
                    sum_.append(len(k))
            for v in i.items():

                for i_1 in v:
                    if isinstance(i_1, int):
                        sum_.append(i_1)
        if isinstance(i, str):
            sum_.append(len(i))

    return(sum(sum_))

print(calc_sum(data_structure))