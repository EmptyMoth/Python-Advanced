"""
Иногда бывает важно сгенерировать какие то табличные данные по заданным характеристикам.
К примеру, если вы будете работать тестировщиками, вам может потребоваться добавить
    в тестовую БД такой правдоподобный набор данных (покупки за сутки, набор товаров в магазине,
    распределение голосов в онлайн голосовании).

Давайте этим и займёмся!

Представим, что наша FrontEnd команда делает страницу сайта УЕФА с жеребьевкой команд
    по группам на чемпионате Европы.

Условия жеребьёвки такие:
Есть N групп.
В каждую группу попадает 1 "сильная" команда, 1 "слабая" команда и 2 "средние команды".

Задача: написать функцию generate_data, которая на вход принимает количество групп (от 4 до 16ти)
    и генерирует данные, которыми заполняет 2 таблицы:
        1. таблицу со списком команд (столбцы "номер команды", "Название", "страна", "сила команды")
        2. таблицу с результатами жеребьёвки (столбцы "номер команды", "номер группы")

Таблица с данными называется `uefa_commands` и `uefa_draw`
"""
import sqlite3
import random

EUROPEAN_COUNTRIES: [str] = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark',
                             'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland',
                             'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands',
                             'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden']
first_names_team: [str] = ["Солнце", "Луна", "Дерево", "Книга", "Мяч", "Меч", "Гроза", "Море", "Кит"]
second_names_team: [str] = ["Победы", "Знаний", "Ожидания", "Грусти", "Счастья", "Отчаяния", "Всевластия"]
dict_name_team: dict = dict([(first_name, second_names_team.copy()) for first_name in first_names_team])


def generate_test_data(cursor: sqlite3.Cursor, number_of_groups: int) -> None:
    commands, draws = _create_data_for_commands_and_draw(number_of_groups)
    _insert_into_commands(cursor, commands)
    _insert_into_draw(cursor, draws)


def _generate_random_country() -> str:
    return random.choice(EUROPEAN_COUNTRIES)


def _generate_random_team_name() -> str:
    random_first_name: str = random.choice(tuple(dict_name_team.keys()))
    second_names: [str] = dict_name_team[random_first_name]
    if len(second_names) <= 0:
        dict_name_team.pop(random_first_name)
        return random_first_name

    random_second_name: str = random.choice(second_names)
    second_names.remove(random_second_name)

    return f"{random_first_name} {random_second_name}"


def _create_data_for_commands_and_draw(number_of_groups: int) -> tuple[list[tuple], list[tuple]]:
    commands: [tuple[str, str, str]] = []
    draws: [tuple[int, int]] = []
    for number_of_group in range(1, number_of_groups + 1):
        for level in ["strong", "medium", "medium", "weak"]:
            random_name: str = _generate_random_team_name()
            random_country: str = _generate_random_country()
            commands.append((random_name, random_country, level))
            draws.append((random_name, number_of_group))

    return commands, draws


def _insert_into_commands(cursor: sqlite3.Cursor, commands_data: [tuple[str, str, str]]) -> None:
    cursor.executemany("""
            INSERT INTO uefa_commands (command_name, command_country, command_level)
            VALUES (?, ?, ?)
        """, commands_data)


def _insert_into_draw(cursor: sqlite3.Cursor, draw_data: [tuple[str, int]]) -> None:
    cursor.executemany("""
                INSERT INTO uefa_draw (command_number, group_number)
                VALUES ((
                    SELECT uefa_commands.command_number 
                    FROM uefa_commands 
                    WHERE command_name = ?
                    ), 
                    ?
                )
        """, draw_data)


if __name__ == '__main__':
    with sqlite3.connect("./database/hw.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        generate_test_data(cursor, 16)
