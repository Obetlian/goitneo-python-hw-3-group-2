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

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def get_birthdays_per_week(self):
        upcoming_birthdays = []
        today = datetime.today()
        for record in self.data.values():
            if hasattr(record, 'birthday'):
                b_date = record.birthday.date.replace(year=today.year)
                if (b_date.month == 2 and b_date.day == 29 and not today.year % 4 == 0):  # Handle non-leap year scenario
                    b_date = b_date.replace(day=28)
                if today <= b_date <= today + timedelta(days=7):
                    upcoming_birthdays.append(record.name.value)
        return upcoming_birthdays

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.number == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.number == old_phone:
                self.phones[idx] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.number == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.number for p in self.phones)}"

class Birthday:
    def __init__(self, date):
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', date):
            raise ValueError("Birthday format should be DD.MM.YYYY")
        self.date = datetime.strptime(date, '%d.%m.%Y')

    def __str__(self):
        return self.date.strftime('%d.%m.%Y')

