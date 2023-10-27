def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as e:
            return str(e)
    return inner

book = AddressBook()

@input_error
def add_contact(args):
    name, phone = args
    if book.find(name):
        return "Контакт з таким іменем вже існує."
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Контакт додано."

@input_error
def change_contact(args):
    name, phone = args
    contact = book.find(name)
    if not contact:
        return "Контакт не знайдено."
    contact.phones = [Phone(phone)]
    return "Номер контакту змінено."

@input_error
def show_phone(args):
    name = args[0]
    contact = book.find(name)
    if not contact:
        return "Контакт не знайдено."
    return ", ".join(map(str, contact.phones))

@input_error
def show_all_contacts(args):
    return "\n".join(f"{name}: {', '.join(map(str, record.phones))}" for name, record in book.data.items())

@input_error
def add_birthday_to_contact(args):
    name, date = args
    contact = book.find(name)
    if not contact:
        return "Контакт не знайдено."
    contact.add_birthday(date)
    return "Дата народження додана."

@input_error
def show_birthday(args):
    name = args[0]
    contact = book.find(name)
    if contact and hasattr(contact, 'birthday'):
        return str(contact.birthday)
    return "Дня народження не знайдено."

@input_error
def upcoming_birthdays(args):
    return ", ".join(book.get_birthdays_per_week())

def hello_command(args):
    return "Привіт! Як я можу вам допомогти?"

# Command Dispatcher
def dispatch(command, *args):
    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all_contacts,
        "add-birthday": add_birthday_to_contact,
        "show-birthday": show_birthday,
        "birthdays": upcoming_birthdays,
        "hello": hello_command
    }
    return commands.get(command, lambda args: "Невідома команда")(args)

# Main bot loop
def main():
    while True:
        user_input = input("Введіть команду: ")
        if user_input in ["close", "exit"]:
            print("До побачення!")
            break
        parts = user_input.split()
        command, args = parts[0], parts[1:]
        print(dispatch(command, *args))

if __name__ == "__main__":
    main()
