import json
import sqlite3

""" Выгружаем файл json """


def read_f(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


""" Удаление поторов в кортеже """


def get_dictionary(n_data):
    lst = {}
    for i in n_data:
        lst.update({i['name']: i['measurement_unit']})
    return lst


"""  Добавляем записи в таблицу единицы измерения """


def insert_data(lst):
    try:
        conneciont = sqlite3.connect(
            "C:/Dev/foodgram-project-react/backend/foodgram/db.sqlite3"
        )
        cursor = conneciont.cursor()
        cursor_insert = conneciont.cursor()
        for i in lst:
            # Добавляем записи в таблицу ингридиентов
            cursor.execute("""
                SELECT id
                FROM grocery_assistant_ingredients
                WHERE ingr_name = ?""", (lst[i], ))
            row = cursor.fetchone()
            if row:
                print(
                    f'({row[0]},{lst[i]}) - такая запись уже существует!'
                )
            else:
                cursor_insert.execute(
                    """INSERT INTO grocery_assistant_ingredients
                    (ingr_name, measurement_unit)
                    VALUES (?, ?)""",
                    (i, lst[i], )
                )
                print(f'{i}:{lst[i]} - добавлена новая запись')
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
lst = {}
# Обрабатываем Единицы измерения
lst = get_dictionary(n_data)
print(insert_data(lst))
