import pandas as pd
import sqlite3
from Gen_4.service.routes import *

for i in book_bible:
    df = pd.read_excel(i)
    a = book_bible[i]
    db_conn = sqlite3.connect(lpi_db)
    cur = db_conn.cursor()

    create_table = f'CREATE TABLE {a}(ID INT, Sum INT)'

    df.to_sql(a, db_conn, if_exists='replace', index=False)
    pd.read_sql(f'SELECT * FROM {a}', db_conn)

