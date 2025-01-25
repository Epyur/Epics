import pandas as pd
import sqlite3
from Gen_4.service.routes import *

df = pd.read_excel(flam_book)

db_conn = sqlite3.connect(lpi_db)
cur = db_conn.cursor()

create_table = 'CREATE TABLE FlamBook(ID INT, Sum INT)'

df.to_sql('FlamBook', db_conn, if_exists="append", index=False)
pd.read_sql('SELECT * FROM FlamBook', db_conn)

