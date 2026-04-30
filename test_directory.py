import pytest
import os
from datetime import datetime
from unittest.mock import patch, MagicMock
from model import Contact, InvalidContact, InvalidNumber, Phonebook, ManagerFile, NotFoundFile

@pytest.fixture
def contact():
    return Contact()


# 1 Успешный ввод
# 2 данные для проверки InvalidContact
# 3 данные для проверки InvalidNumber
@pytest.mark.parametrize(
    "inputs_data_by_user, should_succeed, expected_exception",
    [

        (['Иван', '+79161234567', 'Иванов', 'Иванович', 'Друг'], True, None),

        (['', '+79161234567', 'Иванов', 'Иванович', 'Друг'], False, InvalidContact),

        (['Иван', '12345', 'Иванов', 'Иванович', 'Друг'], False, InvalidNumber),
    ]
)

def test_set_contact_by_user(contact, inputs_data_by_user, should_succeed, expected_exception):
    #проверка ввода информации пользователем (для создания и изменения) тут же проверка отработка исключений
    inputs_iter = iter(inputs_data_by_user)
    with patch('builtins.input', lambda prompt: next(inputs_iter)):
        if should_succeed:
            contact.check_phone_regex = MagicMock(return_value=True)
        else:
            if expected_exception == InvalidNumber:
                contact.check_phone_regex = MagicMock(return_value=False)
        if should_succeed:
            result = contact.set_contact_by_user()
            expected_date = datetime.now().strftime("%d.%m.%Y")
            expected_result = [
                inputs_data_by_user[0],  # имя
                inputs_data_by_user[2],  # фамилия
                inputs_data_by_user[3],  # отчество
                inputs_data_by_user[1],  # номер
                inputs_data_by_user[4],  # описание
                expected_date
            ]
            assert result == expected_result
            # Проверка атрибутов
            assert contact.name == inputs_data_by_user[0]
            assert contact.number == inputs_data_by_user[1]
            assert contact.surname == inputs_data_by_user[2]
            assert contact.surname2 == inputs_data_by_user[3]
            assert contact.note == inputs_data_by_user[4]
            assert contact.date == expected_date
        else:
            with pytest.raises(expected_exception):
                contact.set_contact_by_user()


def test_add_contact():
    ''' Проверка на успешное добавление записи в словарь (логика индентичная для добавления и изменения) '''
    pb = Phonebook()
    # Тестовый словарь
    pb.dict_phonebook = {
        '0': {
            'name': 'Олег',
            'surname': 'Петров',
            'surname2': 'Иванович',
            'number': '+79991112233',
            'note': 'Работа',
            'date': '01.01.2026'
        }
    }

    fake_contact = ['Иван', 'Иванов', 'Иванович', '+79161234567', 'Друг', '02.02.2026']

    with patch.object(Contact, 'set_contact_by_user', return_value=fake_contact):
        pb.create_contact()

    assert '1' in pb.dict_phonebook.keys() #запись есть
    assert pb.dict_phonebook['1'] == {
        'name': 'Иван',
        'surname': 'Иванов',
        'surname2': 'Иванович',
        'number': '+79161234567',
        'note': 'Друг',
        'date': '02.02.2026'
    } #Значения записи


def test_edit_contact_not_found(capsys):
    """тест для не найденного id"""
    pb = Phonebook()
    pb.dict_phonebook = {'123': 'data'}  # существует только id 123
    with patch('builtins.input', return_value='999'):  # вводим несуществующий id
        pb.edit_contact()
    captured = capsys.readouterr()
    assert 'Такой записи не существует' in captured.out


def test_delete_contact():
    pb = Phonebook()
    # Тестовый словарь
    pb.dict_phonebook = {
        '0': {
            'name': 'Олег',
            'surname': 'Петров',
            'surname2': 'Иванович',
            'number': '+79991112233',
            'note': 'Работа',
            'date': '01.01.2026'
        },
        '1': {
            'name': 'Ваня',
            'surname': 'Ершов',
            'surname2': 'Викторович',
            'number': '+7999112333',
            'note': 'Дом',
            'date': '01.01.2026'
        }
    }
    with patch('builtins.input', return_value='999'):
        result = pb.delete_contact()
        assert result == 'Такой записи не существует'

    with patch('builtins.input', return_value='1'):
        result = pb.delete_contact()
        assert result == 'Контакт удален'
        assert '1' not in pb.dict_phonebook


@pytest.mark.parametrize("search_text, expected_output", [
    ('Олег', 'id:0 - Петров Олег Иванович +79991112233 Работа 01.01.2026'),
    ('Ершов', 'id:1 - Ершов Ваня Викторович +7999112333 Дом 01.01.2026'),
    ('7999112333', 'id:1 - Ершов Ваня Викторович +7999112333 Дом 01.01.2026'),
    ('Оля', 'Контакт не найден')
])
def test_search_contact(capsys, search_text, expected_output):
    pb = Phonebook()
    # Тестовый словарь
    pb.dict_phonebook = {
        '0': {
            'name': 'Олег',
            'surname': 'Петров',
            'surname2': 'Иванович',
            'number': '+79991112233',
            'note': 'Работа',
            'date': '01.01.2026'
        },
        '1': {
            'name': 'Ваня',
            'surname': 'Ершов',
            'surname2': 'Викторович',
            'number': '+7999112333',
            'note': 'Дом',
            'date': '01.01.2026'
        }
    }
    with patch('builtins.input', return_value=search_text):
        pb.search_contact()
    captured = capsys.readouterr()
    assert expected_output in captured.out


def test_write_read_file():
    """Создаём временный CSV-файл с тестовыми данными, используя функцию ManagerFile.write_file()"""
    file_path = "./test.csv"
    mf = ManagerFile(file_path)

    content = {
        '0': {
            'name': 'Олег',
            'surname': 'Петров',
            'surname2': 'Иванович',
            'number': '+79991112233',
            'note': 'Работа',
            'date': '01.01.2026'
        },
        '1': {
            'name': 'Ваня',
            'surname': 'Ершов',
            'surname2': 'Викторович',
            'number': '+7999112333',
            'note': 'Дом',
            'date': '01.01.2026'
        }
    }

    result = mf.write_file(content)
    assert result == 'Успех'

    # Проверяем загруженный с помощью ManagerFile.read_file() словарь
    result = mf.read_file()
    #  Проверяем наличие записей
    assert '1' in result.keys()
    assert '2' in result.keys()

    # Проверяем, что данные для id=1 совпадают
    assert result['1'] == {
        'name': 'Олег',
        'surname': 'Петров',
        'surname2': 'Иванович',
        'number': '+79991112233',
        'note': 'Работа',
        'date': '01.01.2026'
    }

    # Проверяем, что self.output_dict тоже заполнился
    assert mf.output_dict == result


def test_file_not_found_exception(capsys):
    file_path = 'no_file.csv'
    with pytest.raises(NotFoundFile) as exc_info:
        # Здесь вызываешь функцию/код, который должен выбросить исключение
        if not os.path.exists(file_path):
            raise NotFoundFile(file_path)
    # Проверяем сообщение (если нужно)
    assert str(exc_info.value) == f"Файл '{file_path}' не найден в указанной директории."
