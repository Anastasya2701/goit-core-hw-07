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

class Birthday(Field):
      def __init__(self, value):
            try:
                self.value = datetime.strptime(value, "%d.%m.%Y").date()
                super().__init__(self.value.strftime("%d.%m.%Y"))
            except ValueError:
                raise ValueError("Не правильний формат дати має бути ДД.ММ.РРРР.")
           
       
class Record: # Клас для зберігання інформації про контакт (ім'я та номер телефону).
       def __init__(self, name):
            self.name = Name(name)
            self.phones = []
            self.birthday = None

       def add_phone(self, phone): # додавання
              self.phones.append(Phone(phone))

       def add_birthday(self, birthday):
             self.birthday = Birthday(birthday)

       def remove_phone(self, phone): # видалення
              for number in self.phones:
                     if number.value == phone:
                          self.phones.remove(number)
                          return 
              raise ValueError
           
       def edit_phone(self, old_phone, new_phone): # зміна
              for ind, number in enumerate(self.phones):
                     if number.value == old_phone: 
                            self.phones[ind] = Phone(new_phone)
                            break
              else:
                     raise ValueError
           
       def find_phone(self, phone): # пошук
              for number in self.phones:
                     if number.value == phone:
                         return number
              return None

       def __str__(self):
           return f"Contact name: {self.name.value}, phones: {'; '.join(number.value for number in self.phones)}"

class AddressBook(UserDict): # Клас для зберігання всіх контатів
        
        def add_record(self, record: Record): # Метод додавання контакту
              name = record.name.value
              self.data.update({name: record})
        
        def find(self,name): # Метод для знаходження та перевірки контакту
              return self.get(name)
              
        def delete(self,name): # Метод для видалення контакту
              del self[name]

        def get_upcoming_birthday(self, days=7):
            def prepare_users(records):
                    prepare_records = []
                    for record in records:
                          if record.birthday:
                                prepare_records.append(record)
                    return prepare_records
              
            def find_next_weekday(start_date, weekday):
                    days_ahead = weekday - start_date.weekday()
                    if days_ahead <= 0:
                        days_ahead += 7
                    return start_date + timedelta(days=days_ahead)
            def find_uncoming_birthday(prepared_records):
                    today = datetime.today().date()
                    upcoming_birthdays = []
                    for record in prepared_records:
                        birthday_this_year = record.birthday.value.replace(year=today.year)

                        if birthday_this_year < today:
                            birthday_this_year = birthday_this_year.replace(year=today.year+1)
            
                        if 0 <= (birthday_this_year - today).days <= days:
                            if birthday_this_year.weekday() >= 5:
                                birthday_this_year = find_next_weekday(birthday_this_year, 0)

                            congratulation_date_str = birthday_this_year.strftime('%d.%m.%Y')
                            upcoming_birthdays.append({"name": record["name"], "congratulation_date": congratulation_date_str})
                    return upcoming_birthdays
            prepared_records = prepare_users(self.data.values())
            upcoming_birthdays = find_uncoming_birthday(prepared_records)
            return upcoming_birthdays
        
        def __str__(self):
              return "\n".join(str(record) for record in self.data.values())

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
    return command, *args

def get_greeting():
     return "How I can help you?"

@input_error
def add_contact(args, book:AddressBook):
    name, phone = args
    record = book.find(name)
    
    if not record:
         recored = Record(name)
         
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book:AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)

    if not record:
        return f"{name} doesn't exists. Add it before changing it."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."
    
    
@input_error    
def show_phone(args, book:AddressBook):
    name = args[0]
    record = book.find(name)

    if not record:
         return f"{name} doesn't exist. "

@input_error    
def show_all(book:AddressBook):
    if len(book.data) == 0:
        return "Contacts list is empty."
    return book

@input_error
def add_birthday(args, book:AddressBook):
    name, birthday = args
    record = book.find(name)

    if not record:
        record = Record(name)
        book.add_record(record)

    record.add_birthday(birthday)

    return "Birthday added."

@input_error
def show_birthday(args, book:AddressBook):
    name = args[0]
    record = book.find(name)        

    if not record:
         return f"{name} doesn't exist."
    if not record.birthday:
         return f"{name} doesn't have birthday."
    return record.birthday

def birthdays(book:AddressBook):
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
        command, *args = parse_input(user_input)
        
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
        elif command == "close" or "exit":
            print(get_good_bye())
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()