import csv
from datetime import datetime
import re



def add_str(row: list) -> dict:
    """Добавление строки в словарь Phonebook"""
    book = {'name': row[0], 'surname': row[1], 'surname2': row[2], 'number': row[3], 'note': row[4], 'date': row[5]}
    return book

class MyException(Exception):
    pass

class NotFoundFile(MyException):
    def __init__(self, filename: str):
        super().__init__(f"Файл '{filename}' не найден в указанной директории.")


class InvalidNumber(MyException):
    def __init__(self, number: str):
        super().__init__(f"Неверный номер {number}")


class InvalidContact(MyException):
    def __init__(self):
        super().__init__(f"Номер и имя обязательны к заполнению.")



class Contact:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.surname = ''
        self.surname2 = ''
        self.number = ''
        self.note = ''
        self.date = ''

    def set_contact_by_user(self) -> list:
        """Ввод информации о контакте"""
        self.name = input('Имя: ')
        if self.name == '':
            raise InvalidContact()
        self.number = input('Номер: ')
        if self.check_phone_regex(self.number) is False:
            raise InvalidNumber(self.number)
        self.surname = input('Фамилия: ')
        self.surname2 = input('Отчество: ')
        self.note = input('Описание: ')
        self.date = datetime.now().strftime("%d.%m.%Y")
        return [self.name, self.surname, self.surname2, self.number, self.note, self.date]

    def check_phone_regex(self, number) -> bool:
        """Проверка номера"""
        pattern = r'^(\+7|8)\d{10}$'
        if re.match(pattern, number):
            return True
        return False


class Phonebook(Contact):
    def __init__(self):
        self.dict_phonebook = {}

    def set_dict_phonebook(self, dict_csv_file: dict) -> None:
        """Сеттер для объекта phonebook"""
        self.dict_phonebook = dict_csv_file

    def look_phonebook(self) -> str:
        """Выввод всех контактов"""
        all_phonebook_text = ''
        for row in self.dict_phonebook.keys():
            all_phonebook_text = all_phonebook_text + (f'id:{row} - {self.dict_phonebook[row]['surname']} '
                                                       f'{self.dict_phonebook[row]['name']}  '
                                                       f'{self.dict_phonebook[row]['surname2']} '
                                                       f'{self.dict_phonebook[row]['number']} '
                                                       f'{self.dict_phonebook[row]['note']} '
                                                       f'{self.dict_phonebook[row]['date']}\n')
        return all_phonebook_text

    def create_contact(self) -> None:
        """Создание контакта"""
        last_id = str(int(list(self.dict_phonebook.keys())[-1]) + 1)
        self.dict_phonebook[last_id] = add_str(Contact.set_contact_by_user(Contact()))

    def edit_contact(self) -> None:
        """Изменение контакта"""
        id_contact = input('Введите id контакта:')
        if id_contact not in self.dict_phonebook.keys():
            print('Такой записи не существует')
        else:
            self.dict_phonebook[id_contact] = add_str(Contact.set_contact_by_user(Contact()))

    def search_contact(self) -> None:
        """Поиск контакта"""
        found_result = 0
        text_for_search = input('Введите запрос:')
        for keys in self.dict_phonebook.keys():
            for elem in self.dict_phonebook[keys].values():
                if text_for_search.lower() in elem.lower():
                    print(
                        f'id:{keys} - {self.dict_phonebook[keys]['surname']} {self.dict_phonebook[keys]['name']} {self.dict_phonebook[keys]['surname2']} '
                        f'{self.dict_phonebook[keys]['number']} {self.dict_phonebook[keys]['note']} {self.dict_phonebook[keys]['date']}')
                    found_result = 1
                    break
        if found_result == 0:
            print('Контакт не найден')


    def delete_contact(self) -> str:
        """Удаление контакта"""
        id_contact = input('Введите id контакта:')
        if id_contact not in self.dict_phonebook.keys():
            return('Такой записи не существует')
        else:
            self.dict_phonebook.pop(id_contact)
            return('Контакт удален')


class ManagerFile:
    def __init__(self, path_file: str):
        self.path_file = path_file
        self.output_dict = {}

    def read_file(self) -> dict:
        """Чтение файла"""
        with open(self.path_file, 'r') as file:
            file_csv = csv.reader(file)
            next(file)
            for row in file_csv:
                elem_list = row[0].split(';')
                self.output_dict[elem_list[0]] = add_str(elem_list[1:])
        return self.output_dict


    def write_file(self, dict_for_save: dict) -> str:
        with open(f'{self.path_file}', 'w') as file:
            file.write(f'id;имя;фамилия;отчество;номер;описание;дата_добавления\n')
            i = 0
            for row in dict_for_save.keys():
                i = i + 1
                file.write(f'{i};{dict_for_save[row]['name']};{dict_for_save[row]['surname']};{dict_for_save[row]['surname2']};'
                           f'{dict_for_save[row]['number']};{dict_for_save[row]['note']};{dict_for_save[row]['date']}\n')
        return ('Успех')
