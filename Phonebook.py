from pathlib import Path
import csv
from datetime import datetime
import re

file_path = Path(u'phonebook.csv')


def check_phone_regex(number):
    # Паттерн для РФ: +7 или 8, затем 10 цифр
    pattern = r'^(\+7|8)\d{10}$'
    if re.match(pattern, number):
        return True
    return False


def add_str(row):
    book = {'name': row[0], 'surname': row[1], 'surname2': row[2], 'number': row[3], 'note': row[4], 'date': row[5]}
    return book


def read_phonebook():
    phonebook = {}
    try:
        with open(file_path, 'r') as file:
            file_csv = csv.reader(file)
            next(file)
            for row in file_csv:
                elem_list = row[0].split(';')
                phonebook[elem_list[0]] = add_str(elem_list[1:])
            print('Успех')
            return phonebook
    except:
        if file_path.exists():
            print("Не удалось прочитать файл")
        else:
            print('Файл не найден')


def look_phonebook(phonebook):
    for row in phonebook.keys():
        print(f'id:{row} - {phonebook[row]['surname']} {phonebook[row]['name']}  {phonebook[row]['surname2']} '
              f'{phonebook[row]['number']} {phonebook[row]['note']} {phonebook[row]['date']}')


def input_contact_by_user():
    number = input('Номер: ')
    if check_phone_regex(number) is False:
        print('Номер не верный')
        return
    name = input('Имя: ')
    if number == '' or name == '':
        print('Номер и имя обзательны для заполнения')
        return
    surname = input('Фамилия: ')
    surname2 = input('Отчество: ')
    note = input('Описание: ')
    date = datetime.now().strftime("%d.%m.%Y")
    return [name, surname, surname2, number, note, date]


def edit_contact(phonebook):
    print('Редактирование контакта:')
    id_contact = input('Введите id контакта:')
    phonebook[id_contact] = add_str(input_contact_by_user())


def create_contact(phonebook):
    print('Новый контакт:')
    last_id = str(int(list(phonebook.keys())[-1]) + 1)
    phonebook[last_id] = add_str(input_contact_by_user())
    print('Успех\n'
          'Не забудьте сохранить изменения!')


def search_contact(phonebook):
    found_result = 0
    text_for_search = input('Введите запрос:')
    for keys in phonebook.keys():
        for elem in phonebook[keys].values():
            if text_for_search.lower() in elem.lower():
                print(
                    f'id:{keys} - {phonebook[keys]['surname']} {phonebook[keys]['name']} {phonebook[keys]['surname2']} '
                    f'{phonebook[keys]['number']} {phonebook[keys]['note']} {phonebook[keys]['date']}')
                found_result = 1
                break
    if found_result == 0:
        print('Контакт не найден')


def delete_contact(phonebook):
    id_contact = input('Введите id контакта:')
    if id_contact not in phonebook.keys():
        print('Такой записи не существует')
    else:
        phonebook.pop(id_contact)
        print('Контакт удален')


def save_phonebook(phonebook):
    with open(f'{file_path}', 'w') as file:
       file.write(f'id;имя;фамилия;отчество;номер;описание;дата_добавления\n')
       i = 0
       for row in phonebook.keys():
           i=i+1
           file.write(f'{i};{phonebook[row]['name']};{phonebook[row]['surname']};{phonebook[row]['surname2']};'
                      f'{phonebook[row]['number']};{phonebook[row]['note']};{phonebook[row]['date']}\n')
    print('Успех')



def menu():
    print('0 - открыть файл с контктами\n'
          '1 - показать все контакты\n'
          '2 - создать контакт\n'
          '3 - найти контакт\n'
          '4 - изменить контакт\n'
          '5 - удалить контакт\n'
          '6 - сохранить изменения\n'
          '7 - выход\n')


def main():
    phonebook = {}
    menu()
    while True:
        try:
            action = int(input('Введите команду: '))
            match action:
                case 0:
                    phonebook = read_phonebook()
                case 1:
                    look_phonebook(phonebook)
                case 2:
                    try:
                        create_contact(phonebook)
                    except:
                        print('Ошибка при добавлении контакта')
                case 3:
                    search_contact(phonebook)
                case 4:
                    edit_contact(phonebook)
                case 5:
                    delete_contact(phonebook)
                case 6:
                    save_phonebook(phonebook)
                case 7:
                    break
        except:
            print('Введите значение от 0 до 7')


if __name__ == '__main__':
    main()
