from collections import UserDict
from datetime import datetime, timedelta

class Field: #Базовий клас для полів запису 
       def __init__(self, value):
            self.value = value

       def __str__(self):
            return str(self.value)

class Name(Field):   #Клас для зберігання імені контакту. Обов'язкове поле.
       def __init__(self, value):
            self.value = value
            super().__init__(value)		              

class Phone(Field): #Клас для зберігання номеру телефона. Має валідацію формату.
	def __init__(self, phone):
              if not phone.isdigit() or len(phone) != 10: # Лише 10 цифр
                     raise ValueError("Номер телефону має складатись з 10 цифр.") # В іншому випадку помилка
              super().__init__(phone)
       
class AddressBook(UserDict): # Клас для зберігання всіх контатів

    def add_record(self, record): # Метод додавання контакту
        self.data[record.name] = record

    def find(self, name): # Метод для знаходження та перевірки контакту
        return self.data.get(name)

    def get_upcoming_birthday(self):
        upcoming_birthdays = []
        today = datetime.today()
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.replace(year=today.year)
                if today <= birthday_this_year <= today + timedelta(days=30):
                    congratulation_date_str = birthday_this_year.strftime('%d.%m.%Y')
                    upcoming_birthdays.append({"name": record.name, "congratulation_date": congratulation_date_str})
        return upcoming_birthdays
    
    def delete(self,name): # Метод для видалення контакту
        del self[name]

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

class Record: # Клас для зберігання інформації про контакт (ім'я та номер телефону).
    def __init__(self, name, birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []

    def add_phone(self, phone): #додовання
        self.phones.append(phone)

    def edit_phone(self, old_phone, new_phone): # зміна
        for ind, number in enumerate(self.phones):
            if number.value == old_phone: 
                self.phones[ind] = Phone(new_phone)
                break
            else:
                raise ValueError
            
    def remove_phone(self, phone): # видалення
        for number in self.phones:
            if number.value == phone:
                self.phones.remove(number)
                return 
            raise ValueError

    def add_birthday(self, birthday):
        self.birthday = birthday

    def find_phone(self, phone): # пошук
        for number in self.phones:
            if number.value == phone:
                return number
            return None
        
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(number.value for number in self.phones)}"

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Not found."
    return inner

def parse_input(user_input: str):
    command, *args = user_input.split()
    command = command.strip().lower()
    return command, args

def get_greeting():
    return "How I can help you?"

@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    
    if record is None:
        record = Record(name)
        book.add_record(record)
        
    if phone:
        record.add_phone(phone)
    return "Contact added."

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)

    if not record:
        return f"{name} doesn't exist. Add it before changing it."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."
    
@input_error    
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if not record:
        return f"{name} doesn't exist."
    return ", ".join(record.phones)

@input_error    
def show_all(book: AddressBook):
    if len(book.data) == 0:
        return "Contacts list is empty."
    return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)

    if not record:
        record = Record(name)
        book.add_record(record)

    record.add_birthday(birthday)

    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)        

    if not record:
        return f"{name} doesn't exist."
    if not record.birthday:
        return f"{name} doesn't have birthday."
    return record.birthday

def birthdays(book: AddressBook):
    if len(book.data) == 0:
        return "Contacts list is empty."
    
    return book.get_upcoming_birthday()

def get_good_bye():
    return "Good bye!"

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        
        if command == "hello":
            print(get_greeting())
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command in ("close", "exit"):
            print(get_good_bye())
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()