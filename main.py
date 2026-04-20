from controller import Controller
from view import ConsoleView
from model import ManagerFile, Phonebook, Contact, NotFoundFile
from pathlib import Path
import csv
from datetime import datetime
import re
import os

file_path: Path = Path(u'phonebook.csv')

if not os.path.exists(file_path):
    raise NotFoundFile(file_path)


manager_file = ManagerFile(file_path)
phonebook = Phonebook()
console_view = ConsoleView()
contact = Contact()
controller = Controller(phonebook, contact, console_view, manager_file)
controller.run()