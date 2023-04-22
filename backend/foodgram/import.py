import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodgram.settings")

import django
django.setup()
from django.core.management import call_command
import urllib.request
import json
from pprint import pprint
import sqlite3
from grocery_assistant.models import Unit_of_measure, Ingredients
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

""" Выгружаем файл json """
def read_f(filename):
    with open(filename,'r', encoding='utf-8') as file:
        return json.load(file)

""" Удаление поторов в кортеже """
def delete_repeat(n_data, type_data):
    # type_data: 1 или 2
    # 1 - выбираем единицы измерения
    # 2 - выбираем ингридиенты
    lst = []
    if type_data == 1:
        for i in n_data:
            lst.append(i['measurement_unit']) 
    elif type_data == 2:
        for i in n_data:
            lst.append(i['name']) 
    lst[:] = list(set(lst))
    return lst

"""  Добавляем записи в таблицу единицы измерения """
def insert_data(lst, mode_insrt):
    try:
        conneciont = sqlite3.connect("C:/Dev/foodgram-project-react/backend/foodgram/db.sqlite3")
        cursor = conneciont.cursor()
        cursor_insert = conneciont.cursor()
        for i in range(len(lst)):
            # Добавляем записи в таблицу Единиц измерения
            if mode_insrt == 1:
                cursor.execute("SELECT id FROM grocery_assistant_unit_of_measure WHERE unit_name = ?", (lst[i], ))
                row = cursor.fetchone()
                if row:
                    print(f'({row[0]},{lst[i]}) - такая запись уже существует!')
                else:
                    cursor_insert.execute("INSERT INTO grocery_assistant_unit_of_measure (unit_name) VALUES (?)", (lst[i], ))
                    print(f'{lst[i]} - добавлена новая запись')
            # Добавляем записи в таблицу Единиц измерения
            elif mode_insrt ==2:
                cursor.execute("SELECT id FROM grocery_assistant_ingredients WHERE ingr_name = ?", (lst[i], ))
                row = cursor.fetchone()
                if row:
                    print(f'({row[0]},{lst[i]}) - такая запись уже существует!')
                else:
                    cursor_insert.execute("INSERT INTO grocery_assistant_ingredients (ingr_name) VALUES (?)", (lst[i], ))
                    print(f'{lst[i]} - добавлена новая запись')
        conneciont.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if conneciont:
            conneciont.close()
    return 'Запись в bd выполнена успешно!'

# Вызываем read_f
n_data = read_f("C:/Dev/foodgram-project-react/data/ingredients.json")
lst = []
# Обрабатываем Единицы измерения
lst = delete_repeat(n_data, 1)
print(insert_data(lst, 1))
# Обрабатываем Ингридиенты
lst = delete_repeat(n_data, 2)
print(insert_data(lst, 2))
#print(lst)
