import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from typing import Union, List, Dict, Optional
import sqlite3

from Gen_9.service.body import work_data
from Gen_9.service.rout_map import sbd, ns, ekn_book, cus_book


class PandasSQLManager:
    def __init__(self, db_url: str = 'sqlite:///database.db'):
        """
        Инициализация менеджера базы данных

        :param db_url: URL базы данных (например, 'sqlite:///database.db' или 'postgresql://user:password@localhost/db')
        """
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.connection = self.engine.connect()
        self.inspector = inspect(self.engine)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Закрытие соединения с базой данных"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()

    def create_db_from_dataframe(self, df: pd.DataFrame, table_name: str,
                                 if_exists: str = 'replace', index: bool = False,
                                 dtype: Optional[Dict] = None) -> bool:
        """
        Создание таблицы в базе данных из DataFrame

        :param df: DataFrame с данными
        :param table_name: имя таблицы
        :param if_exists: поведение при существующей таблице ('fail', 'replace', 'append')
        :param index: записывать ли индекс DataFrame как отдельную колонку
        :param dtype: словарь с указанием типов данных для колонок
        :return: True если успешно, False если ошибка
        """
        try:
            df.to_sql(
                table_name,
                con=self.engine,
                if_exists=if_exists,
                index=index,
                dtype=dtype
            )
            print(f"Таблица '{table_name}' успешно создана/обновлена")
            return True
        except SQLAlchemyError as e:
            print(f"Ошибка при создании таблицы '{table_name}': {e}")
            return False

    def add_table(self, df: pd.DataFrame, table_name: str,
                  if_exists: str = 'fail', index: bool = False,
                  dtype: Optional[Dict] = None) -> bool:
        """
        Добавление новой таблицы в базу данных

        :param df: DataFrame с данными
        :param table_name: имя таблицы
        :param if_exists: поведение при существующей таблице ('fail', 'replace', 'append')
        :param index: записывать ли индекс DataFrame как отдельную колонку
        :param dtype: словарь с указанием типов данных для колонок
        :return: True если успешно, False если ошибка
        """
        if if_exists == 'fail' and table_name in self.get_table_names():
            print(f"Таблица '{table_name}' уже существует")
            return False

        return self.create_db_from_dataframe(df, table_name, if_exists, index, dtype)

    def upsert_data(self, table_name: str, df: pd.DataFrame,
                    match_columns: Union[str, List[str]]) -> bool:
        """
        Обновление и добавление данных в таблицу (UPSERT)

        :param table_name: имя таблицы
        :param df: DataFrame с новыми данными
        :param match_columns: колонки для проверки совпадения (первичный ключ или список колонок)
        :return: True если успешно, False если ошибка
        """
        if not isinstance(match_columns, list):
            match_columns = [match_columns]

        try:
            # Получаем существующие данные
            existing_df = self.get_table_data(table_name)

            if existing_df is None or existing_df.empty:
                # Если таблица пустая, просто добавляем все данные
                return self.create_db_from_dataframe(df, table_name, if_exists='append')

            # Находим новые и измененные записи
            temp_df = df.merge(
                existing_df,
                on=match_columns,
                how='left',
                indicator=True,
                suffixes=('', '_existing')
            )

            # Разделяем на новые и существующие записи
            new_records = temp_df[temp_df['_merge'] == 'left_only'].drop(columns=['_merge'])
            existing_records = temp_df[temp_df['_merge'] == 'both'].drop(columns=['_merge'])

            # Обновляем существующие записи
            if not existing_records.empty:
                # Удаляем колонки с суффиксом '_existing'
                update_cols = [col for col in existing_records.columns
                               if not col.endswith('_existing') and col not in match_columns]

                # Формируем SQL для обновления
                with self.engine.begin() as conn:
                    for _, row in existing_records.iterrows():
                        set_clause = ", ".join([f"{col} = :{col}" for col in update_cols])
                        where_clause = " AND ".join([f"{col} = :{col}" for col in match_columns])

                        params = row[update_cols + match_columns].to_dict()

                        sql = f"""
                        UPDATE {table_name}
                        SET {set_clause}
                        WHERE {where_clause}
                        """

                        conn.execute(sql, params)

            # Добавляем новые записи
            if not new_records.empty:
                new_records = new_records[[col for col in new_records.columns
                                           if not col.endswith('_existing')]]
                self.create_db_from_dataframe(new_records, table_name, if_exists='append')

            print(
                f"Таблица '{table_name}' успешно обновлена (добавлено: {len(new_records)}, обновлено: {len(existing_records)})")
            return True
        except SQLAlchemyError as e:
            print(f"Ошибка при обновлении таблицы '{table_name}': {e}")
            return False

    def get_table_data(self, table_name: str, query: Optional[str] = None,
                       params: Optional[Dict] = None) -> Optional[pd.DataFrame]:
        """
        Извлечение данных из таблицы

        :param table_name: имя таблицы
        :param query: дополнительный SQL запрос (если None, выбираются все данные)
        :param params: параметры для SQL запроса
        :return: DataFrame с данными или None при ошибке
        """
        try:
            if query is None:
                query = f"SELECT * FROM {table_name}"

            df = pd.read_sql(query, con=self.engine, params=params)
            return df
        except SQLAlchemyError as e:
            print(f"Ошибка при получении данных из таблицы '{table_name}': {e}")
            return None

    def get_table_names(self) -> List[str]:
        """Получение списка всех таблиц в базе данных"""
        return self.inspector.get_table_names()

    def table_exists(self, table_name: str) -> bool:
        """Проверка существования таблицы"""
        return table_name in self.get_table_names()

    def get_table_schema(self, table_name: str) -> Optional[Dict]:
        """
        Получение схемы таблицы

        :param table_name: имя таблицы
        :return: словарь с информацией о колонках или None при ошибке
        """
        try:
            columns = self.inspector.get_columns(table_name)
            return {col['name']: col['type'] for col in columns}
        except SQLAlchemyError as e:
            print(f"Ошибка при получении схемы таблицы '{table_name}': {e}")
            return None


if __name__ == "__main__":

    ekn_1 = pd.read_excel(cus_book)
    # Использование класса
    with PandasSQLManager('sqlite:///lpi.db') as db_manager:
        # # 1. Создание базы данных из DataFrame
        # db_manager.create_db_from_dataframe(aim_df, 'requests')

        # 2. Добавление новой таблицы

        # db_manager.add_table(ekn_1, 'manufactures')
    #
        # # 3. Обновление данных с проверкой совпадений
        # db_manager.upsert_data('experiments', res, 'index')
    #
        # 4. Извлечение данных
        print("\nДанные из таблицы requests:")
        fin = db_manager.get_table_data('requests')
        fin.to_excel('fin.xlsx')
        print(fin)
    #     print("\nСписок таблиц в базе данных:")
    #     print(db_manager.get_table_names())
    #
    #     print("\nСхема таблицы products:")
    #     print(db_manager.get_table_schema('products'))
    def create_pivot_table(db_path, table_name, index_col, pivot_col, value_col):
        conn = sqlite3.connect(db_path)

        # Получаем уникальные значения для столбцов сводки
        pivot_values = pd.read_sql(f"SELECT DISTINCT {pivot_col} FROM {table_name}", conn)[pivot_col].tolist()

        # Генерируем SQL запрос
        case_exprs = [f"SUM(CASE WHEN {pivot_col} = '{v}' THEN {value_col} ELSE 0 END) AS \"{v}\""
                      for v in pivot_values]

        query = f"""
        SELECT 
            {index_col},
            {', '.join(case_exprs)}
        FROM {table_name}
        GROUP BY {index_col};
        """

        # Выполняем запрос
        pivot_df = pd.read_sql(query, conn)
        conn.close()

        return pivot_df


    # Использование
    pivot_data = create_pivot_table('lpi.db', 'requests', 'ID', 'ekn', 'cust_mail')
    pivot_data.to_excel('piv.xlsx')