import view


class Controller:
    def __init__(self, phonebook, contact, console, m_file):
        self.phonebook = phonebook
        self.contact = contact
        self.console = console
        self.m_file = m_file

    def run(self) -> None:
        """Основная функция"""
        self.phonebook.set_dict_phonebook(self.m_file.read_file())
        self.console.show_message(0)
        self.console.show_menu()
        action = 1
        while action != 7:
            try:
                action = self.console.get_command()
                match action:
                    case 0:
                        self.phonebook.set_dict_phonebook(self.m_file.read_file())
                        self.console.show_message(1)
                        self.console.show_message(0)
                        pass
                    case 1:
                        self.console.show_message(self.phonebook.look_phonebook())
                        pass
                    case 2:
                        self.console.show_message(4)
                        self.phonebook.create_contact()
                        self.console.show_message(3)
                    case 3:
                        pass
                        self.phonebook.search_contact()
                    case 4:
                        self.console.show_message(5)
                        self.phonebook.edit_contact()
                        self.console.show_message(3)
                    case 5:
                        self.console.show_message(self.phonebook.delete_contact())
                    case 6:
                        self.console.show_message(self.m_file.write_file(self.phonebook.dict_phonebook))
                    case 7:
                        action = 7
            except Exception as e:
                print(e)




