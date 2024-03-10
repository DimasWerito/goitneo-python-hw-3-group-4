from classes import AddressBook, Record, Name, Phone, Birthday, InvalidDateFormat, InvalidLengthFormat, InvalidDigitFormat


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Give me name, please."
        except InvalidDateFormat:
            return "Invalid date format, should be DD.MM.YYYY"
        except InvalidLengthFormat:
            return "Invalid phone length, should be 10 symbols."
        except InvalidDigitFormat:
            return "Invalid symbols, should be only digits."

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts: AddressBook):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, contacts: AddressBook):
    name, old_phone, new_phone = args
    record: Record = contacts.find(name)
    if record:
        is_changed = record.edit_phone(old_phone, new_phone)
        return "Contact have been changed." if is_changed else "Old number phone was not found."
    else:
        return "Contact was not found."
    
@input_error  
def phone_contact(args, contacts: AddressBook):
    name = args[0]
    record: Record = contacts.find(name)
    if record:
        return ", ".join([ph.value for ph in record.phones])
    else:
        return "Contact was not found."
    
def all_contacts(contacts: AddressBook):
    info  = ""
    for name, phone in contacts.data.items():
        info += f"{name}: {phone}\n"
    return info

@input_error
def add_birthday(args, contacts: AddressBook):
    name, birthday = args
    record: Record = contacts.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday has been added."
    else:
        return "Contact was not found."
    
@input_error
def show_birthday(args, contacts):
    name = args[0]
    record: Record = contacts.find(name)
    if record:
        return record.birthday.value if record.birthday else "Unknown Birthday."
    else:
        return "Contact was not found."
    
@input_error
def birthdays(contacts: AddressBook):
    persons = contacts.get_birthdays_per_week()
    if not persons:
        return "Next week there is no Birthdays."
    else:
        return "\n".join(persons)

def main():
    contacts: AddressBook = AddressBook()
    contacts.load()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            contacts.save()
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(phone_contact(args, contacts))
        elif command == "all":
            print(all_contacts(contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()