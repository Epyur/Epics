from Gen_2.workers.xls import *
import math

class Combustion:
    book = open_file(comb_book, 0) # open the book of measures
    title_row = book.row_values(rowx=0) # form title row names