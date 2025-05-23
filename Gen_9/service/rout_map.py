import os
import sys
from pathlib import Path
import pandas as pd


def get_base_dir():
    """Определяет базовую директорию с учётом структуры Gen_9 = dist"""
    if getattr(sys, 'frozen', False):
        # Режим EXE: файлы в подпапках Gen_9/db внутри распакованного EXE
        return Path(sys.executable).parent
    else:
        # Режим разработки: корень проекта (где Gen_9/db)
        return Path(__file__).parent.parent  # Поднимаемся на уровень выше до Gen_9


def get_db_path(filename, folder='db'):
    """Возвращает путь к файлу в db с проверкой существования"""
    path = get_base_dir() / folder / filename
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    return str(path)


# Инициализация путей
try:
    in_title = get_db_path("in_title.xlsx")
    sbd = get_db_path("sbd.xlsx")
    ekn_book = get_db_path("EKN.xlsx")
    out_names = get_db_path("out_names.xlsx")
    cus_book = get_db_path("custiomer.xls")
    inc_book = get_db_path("inc.xlsx")
    exp_book = get_db_path("exp.xlsx")
    alltasks = get_db_path("alltasks.xlsx")
    closedtasks = get_db_path("closedtasks.xlsx")
    results_base = get_db_path("results.xlsx", 'out')


    # Шаблоны
    doc_templ = get_db_path("g_short.docx")
    doc_templ_fg = get_db_path("g_full.docx")
    doc_templ_v = get_db_path("v_short.docx")

except FileNotFoundError as e:
    print(f"Ошибка инициализации путей: {e}")
    sys.exit(1)


# TDT-файлы
def TdtFile(file_date):
    path = get_base_dir() / "tdt" / f"{file_date} 00_00.tdt"
    return str(path)


tdt_path = str(get_base_dir() / "tdt")

# Загрузка пространства имён
try:
    name_space_df = pd.read_excel(in_title)
    ns = name_space_df.set_index('col_num')['val'].to_dict()
except Exception as e:
    print(f"Ошибка загрузки пространства имён: {e}")
    ns = {}