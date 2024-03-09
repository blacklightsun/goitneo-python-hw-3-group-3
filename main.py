import re
from  datetime import datetime, timedelta
from collections import UserDict

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print("Give me a valid (lenght > 0, only characters or digits) name\n and/or valid (ten digits)phone number\nand/or valid date (in dd.mm.yyyy format only) please.")
    return inner
# other errors that cause an exception are not yet expected by logic

class Field:
    """
    Objects of the class allow to do:
    - keep contact data: some value.
    Field have got the following attribute(s): a value.
    Objects of the class is can processed as a parent for items of the Record object.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)



class Name(Field):
    """
    Objects of the class allow to do:
    - keep contact name: as specific value for Field .
    Field have got the following attribute(s): a value.
    Objects of the class is can processed as a specific item of the Record object.
    """
    def __init__(self, value: str):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if re.search(r'^[a-zA-Z0-9]+$', value) is not None:
            self.__value = value
        else:
            print("Name can't be empty and must contains characters only")            



class Phone(Field):
    """
    Objects of the class allow to do:
    - keep contact phone number: as specific value for Field .
    Field have got the following attribute(s): a value.
    Objects of the class is can processed as a specific item of the Record object.
    """
    def __init__(self, value: str):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if re.search(r'^\d{10}$', new_value):
            self.__value = new_value
        else:
            print("Ten digit for phone numder only")



class Birthday(Field):
    """
    Objects of the class allow to do:
    - keep contact birthday: as specific value for Field .
    Field have got the following attribute(s): a value.
    Objects of the class is can processed as a specific item of the Record object.
    """
    def __init__(self, value: str):
        super().__init__(value)
        # self._value = None
        self.value = value

    # @property
    # def value(self):
    #     return self._value

    # @value.setter
    # def value(self, value):
    #     if re.search(r'\b(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19\d\d|20\d\d)\b', value):
    #         self.value = datetime(
    #                 int(value[6:]),
    #                 int(value[3:5]),
    #                 int(value[0:2]),
    #                 0, 0, 0,
    #                 )
    #     else:
    #         print("Date in dd.mm.yyyy format only")    



class Record:
    '''
    Objects of the class allow to do:
    - keep contact data: a name, a list of phone numbers, a birthday, etc.
    - find and return object 'phone',
    - add new object 'phone',
    - delete object 'phone'.
    Records have got the following attributes: a name as object, a list of phone number objects.
    Objects of the class is can processed as item of AddressBook object.
    '''
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def find_phone(self, phone: str):
        '''
        Recieve a 'phone' string.
        Return from the list a Phone class object with value is 'phone' string.
        '''
        for p in self.phones:
            if phone == p.value:
                return p
   
    @input_error
    def add_phone(self, new_phone: str):
        '''
        Recieve a 'phone' string.
        Add to the list a Phone class object with value is 'new_phone' string.
        Print message with confirmation.
        '''
        if self.find_phone(new_phone):
            print(f'{self.name} have got the {new_phone} phone already.')
        else:
            self.phones.append(Phone(new_phone))
            print(f'{new_phone} is added for {self.name}.')

    @input_error
    def edit_phone(self, old_phone: str, new_phone: str):
        '''
        Recieve a 'old_phone' string.
        Remove from the list a Phone class object with value is 'old_phone' string and 
        add to the list a Phone class object with value is 'new_phone' string.
        Print message with confirmation.
        '''

        if old_phone == new_phone:
            print(f'{old_phone} is equal to {new_phone}.')
        else:
            phone = self.find_phone(old_phone)
            if phone:
                self.phones.remove(phone)
                self.phones.append(Phone(new_phone))
                print(f'{old_phone} is changed to {new_phone} for {self.name}.')
            else:
                print(f'{self.name} haven\'t got the {new_phone} phone number.')
 
    def remove_phone(self, del_phone: str):
        '''
        Recieve a 'del_phone' string.
        Remove from the list a Phone class object with value is 'del_phone' string.
        Print message with confirmation.
        '''
        phone = self.find_phone(del_phone)
        if phone:
            self.phones.remove(phone)
            print(f'{del_phone} is removed the {self.name}.')
        else:
            print(f'{self.name}\'s haven\'t got the {del_phone} phone number.')  

    @input_error
    def add_birthday(self, birthday_string: str):
        '''
        Recieve a 'birthday_string' string.
        Change date in Birthday field.
        '''
        if re.search(r'\b(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19\d\d|20\d\d)\b', birthday_string):
            self.birthday = Birthday(datetime(
                    int(birthday_string[6:]),
                    int(birthday_string[3:5]),
                    int(birthday_string[0:2]),
                    0, 0, 0,
                    ))
            print(f'Birthday {birthday_string} is added for {self.name}.')
        else:
            print('The date is not valid')

        

    def show_birthday(self):
        '''
        Simply print birthday info.
        '''
        if self.birthday is None:
            print(f'\n{self.name}\'s birthday is not specified.\n')
        else:
            print(f'\n{self.name}\'s birthday is {self.birthday.value.strftime('%d.%m.%Y')}.\n')

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {', '.join(p.value if p.value is not None else " " for p in self.phones).rstrip(', ')}\n"
  


class AddressBook(UserDict):
    '''
    Objects of the class allow to do:
    - keep records with contact data,
    - find and return record as object,
    - add new records,
    - delete record as object.
    Records keep as items of a dict. Dict's keys are a name of the record, dict's values are the record as the object.
    Objects of the class are can processed as separate objects to downloading/saving to a disk, for copying, etc.
    '''

    @input_error
    def find(self, name: str):
        '''
        Recieve a 'name' string.
        Return from the dict a Record class object with key is 'name' string.
        '''
        
        if name in self.data.keys():
            return self.data[name]

    @input_error
    def delete(self, del_name: str):
        '''
        Recieve a 'del_name' string.
        Remove from the dict a Record class object with key is 'del_name' string.
        Print message with confirmation.
        '''
        record = self.find(del_name)
        if record:
            del record
            print(f'Contact {del_name} is deleted.')
        else:
            print(f'Sorry, but {del_name} is not in your contact book yet. ((')
        
    def add_record(self, new_name: object):
        '''
        Recieve a 'new_name' string.
        Remove from the dict a Record class object with key is 'del_name' string.
        Print message with confirmation.
        '''
        record = self.find(new_name.name)
        if record:
            print(f'Sorry, but {record.name} is in your contact book already. ((')
        else:
            self.data[new_name.name.value] = new_name
            print(f'Contact {new_name.name} is added.')
    
    def get_birthdays_per_week(self):
        '''
        This method print a list of contacts with birthdays today and next 6 days.
        If birthday will be on weekends (Saturday, Sunday) then birthday message would move
        on next Monday.
        '''

        if len(self.data) == 0:
            print('\nNobody is in your contact list. (((\n')
            return

        BIRTHDATE_SCOPE = 7 # today and next 6 days
        WEEKENDS = (5, 6) # 5, 6 = saturday, sunday
        today_date = datetime.today().date()

        birthdays_dict = dict()
        for record in self.data.values():

            if record.birthday is not None: # checking for empty birthday
                birthday_this_year = record.birthday.value.date().replace(year=today_date.year)
            else:
                break

            weekday = birthday_this_year.weekday()
            if weekday in WEEKENDS: 
                birthday_this_year = birthday_this_year + timedelta(days=(7 - weekday)) # move to Monday

            day_delta = (birthday_this_year - today_date).days # days from today to birthday
            if 0 <= day_delta and day_delta < BIRTHDATE_SCOPE:

                name = record.name.value

                if birthday_this_year not in birthdays_dict:
                    birthdays_dict[birthday_this_year] = name + ", " # for first date in dict
                else:
                    birthdays_dict[birthday_this_year] += name + ", " # for second and next dates in dict

        days_list = [i for i in birthdays_dict.keys()]

        if len(days_list) == 0:
            print(f"\nNo one celebrates their birthday in next {BIRTHDATE_SCOPE} days. (((\nThrow a party for yourself!!!\n")
            return

        days_list.sort()

        print_text = f"\nBirthdays in next {BIRTHDATE_SCOPE} days:\n-------------------------\n"

        for day in days_list:
            print_text += f"{str(day.strftime('%A'))+":":<12} {birthdays_dict[day].rstrip(', ')}\n"

        print(print_text)



def get_help():
    '''
    This function returns a user help data.
    '''
    help_string = 'Help will be in next version. )))'
    print(help_string)



def main():
    '''
    This is the function with a main wokr cycle for inputing of commands.
    '''
    book = AddressBook()

    print("\nWelcome to the assistant bot!\n")
    while True:

        parser_list = input("Enter a command: ").split()
        for _ in range(3 - len(parser_list)):
            parser_list.append(None)
        command, name, *args = parser_list
        if command is None:
            print("\nCommand isn't entered! Enter it, please!\n")
            continue
        command = command.strip().lower()
        arguments = (*args,)
        # парсінг команд виконується стільки ж разів, скільки й головний цикл у main(),
        # тому не бачу сенсу виділяти три рядки коду в окрему функцію і збільшувати кількість рядків з кодом

        if command in ("close", "exit", 'quit', 'e', 'q'):
            print("\nGood bye!\n")
            break

        elif command == "hello":
            print("\nHello! How can I help you?\n")

        elif command == "all":
            print("\nYour contact(s):\n-------------------------\n")
            for record in book.data.values():
                print(record)

        elif command in ("help", 'h'):
            get_help()       

        elif command in ("birthdays", 'bd'):
            book.get_birthdays_per_week()

        elif command in ('add',):
            record = Record(name)
            for phone in arguments:
                record.add_phone(phone)
            book.add_record(record)

        elif command in ('add-birthday',):
            book.find(name).add_birthday(arguments[0])

        elif command in ('show-birthday',):
            book.find(name).show_birthday()

        elif command in ('change',):
            if len(arguments) == 2:
                old_phone = arguments[0]
                new_phone = arguments[1]
                book.find(name).edit_phone(old_phone, new_phone)
            else:
                print('Old and new phone numbers isn\'t enter correctly')
    
        elif command in ('phone',):
            print(book.find(name))

        else:
            print("\nInvalid command!\n")

book = AddressBook()

if __name__ == "__main__":
    main()
