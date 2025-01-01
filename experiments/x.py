# import openpyxl
#
# rb = openpyxl.open('1.xlsx')
# rb_sheet = rb['Sheet1']
# print(rb_sheet)
#
# list_1 = [[3, 4, 5], [6, 7, 8]]
# count = 0
# for item in list_1:
#     count += 1
#     for i in item:
#         rb_sheet.cell(count, i).value = i
#
#     rb.save('1.xlsx')

lst = ['a', 'b', 'c', 'd']

del lst[0]

print(lst)