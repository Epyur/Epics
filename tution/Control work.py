import statistics
from http.cookiejar import join_header_words

grades = [[5, 3, 3, 5, 4], [2, 2, 2, 3], [4, 5, 5, 2], [4, 4, 3], [5, 5, 5, 4, 5]]
students = {'Johnny', 'Bilbo', 'Steve', 'Khendrik', 'Aaron'}
grades_a = grades[0]
grades_b = grades[1]
grades_j = grades[2]
grades_k = grades[3]
grades_s = grades[4]
avg_a = sum(grades_a)/len(grades_a)
avg_b = sum(grades_b)/len(grades_b)
avg_j = sum(grades_j)/len(grades_j)
avg_k = sum(grades_k)/len(grades_k)
avg_s = sum(grades_s)/len(grades_s)
print(grades_a)
print(grades_b)
print(grades_j)
print(grades_k)
print(grades_s)
students = list(students)
students.sort()
a = list(filter(lambda x: x.startswith('A'), students))
b = list(filter(lambda x: x.startswith('B'), students))
j = list(filter(lambda x: x.startswith('J'), students))
k = list(filter(lambda x: x.startswith('K'), students))
s = list(filter(lambda x: x.startswith('S'), students))
grades_list = [avg_a,  avg_b, avg_j, avg_k, avg_s]
print(grades_list)
print(students)
students_book=dict(zip(students, grades_list))
print(students_book)
print('Average grade of ', a[0], ' is ', str(avg_a))
print('Average grade of ', b[0], ' is ', str(avg_b))
print('Average grade of ', j[0], ' is ', str(avg_j))
print('Average grade of ', k[0], ' is ', str(avg_k))
print('Average grade of ', s[0], ' is ', str(avg_s))