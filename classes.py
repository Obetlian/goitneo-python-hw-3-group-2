from datetime import datetime, timedelta
import re
from collections import UserDict

class Phone:
    def __init__(self, number):
        if not re.match(r'^\d{10}$', number):
            raise ValueError("Phone number must be 10 digits.")
        self.number = number

    def __str__(self):
        return self.number

class Name:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.name] = record

    def find(self, name):
        return self.data.get(name, None)

    def get_birthdays_per_week(self):
        upcoming_birthdays = []
        today = datetime.today()
        for record in self.data.values():
            if hasattr(record, 'birthday'):
                b_date = record.birthday.date.replace(year=today.year)
                if today <= b_date <= today + timedelta(days=7):
                    upcoming_birthdays.append(record.name.name)
        return upcoming_birthdays

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, date):
        self.birthday = Birthday(date)

class Birthday:
    def __init__(self, date):
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', date):
            raise ValueError("Birthday format should be DD.MM.YYYY")
        self.date = datetime.strptime(date, '%d.%m.%Y')

    def __str__(self):
        return self.date.strftime('%d.%m.%Y')
