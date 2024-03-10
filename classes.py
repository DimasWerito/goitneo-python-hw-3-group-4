import pickle
import os
from collections import UserDict
from datetime import datetime
from collections import defaultdict

class InvalidDateFormat(Exception):
    pass

class InvalidLengthFormat(Exception):
    pass

class InvalidDigitFormat(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.value = self.validate(value)

    def validate(self, value):
        if len(value) != 10:
            raise InvalidLengthFormat
        elif not value.isdigit():
            raise InvalidDigitFormat
        else:
            return value
        
class Birthday(Phone):
    def validate(self, value):
        try:
            date_object = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise InvalidDateFormat
        return value
    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday =  None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        ph = self.find_phone(phone)
        if ph:
            self.phones.remove(ph)

    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone):
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
            return True
        return False

    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                return ph
            
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)} \
            {self.birtday.value if self.birthday else ''}"

class AddressBook(UserDict):
    file_name = "addressbook.bin"

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if self.data.get(name):
            self.data.pop(name)

    def get_birthdays_per_week(self):
        persons = defaultdict(list)
        today = datetime.today().date()
        for user in self.data.values():
            name = user.name.value
            birthday = user.birthday
            if not birthday:
                continue
            birthday = datetime.strptime(birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year+1)
            delta_days = (birthday_this_year - today).days
            if delta_days < 7:
                week_day_num = birthday_this_year.weekday()
                if week_day_num in [5, 6, 0]:
                    persons["Monday"].append(name)
                elif week_day_num == 1:
                    persons["Tuesday"].append(name)
                elif week_day_num == 2:
                    persons["Wednesday"].append(name)
                elif week_day_num == 3:
                    persons["Thursday"].append(name)
                elif week_day_num == 4:
                    persons["Friday"].append(name)
        info = []
        for day, names in persons.items():
            info.append(f"{day}: {', '.join(names)}\n")
        return info
    
    def load(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "rb") as f:
                self.data = pickle.load(f)
            
    def save(self):
        with open(self.file_name, "wb") as f:
            pickle.dump(self.data, f)


if __name__ == "__main__":
            # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")