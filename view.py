class ConsoleView:

   def get_command(self) -> None:
       """Ввод информации от пользователя"""
       return int(input('Введите команду: '))



   def show_menu(self) -> None:
       """Вывод меню"""
       print('0 - сбросить изменения\n'
            '1 - показать все контакты\n'
            '2 - создать контакт\n'
            '3 - найти контакт\n'
            '4 - изменить контакт\n'
            '5 - удалить контакт\n'
            '6 - сохранить изменения\n'
            '7 - выход\n')


   def show_message(self, message: str) -> None:
       """Вывод сообщений"""
       try:
           if type(message) == type(10):
               match message:
                case 0:
                    print('Файл Phonebook добавлен')
                case 1:
                    print('Изменения удалены')
                case 3:
                    print('Успех\n'
                     'Не забудьте сохранить изменения!')
                case 4:
                    print('Новый контакт:')
                case 5:
                    print('Редактирование контакта:')
           else:
               print(message)
       except Exception as e:
           print(e)







