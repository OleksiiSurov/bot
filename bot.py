from collections import UserDict
from datetime import datetime, timedelta
import pickle


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, page_number, page_size):
        data_new = list(self.data.items())
        all_rec = page_number * page_size
        yield list(data_new[(all_rec-page_size):all_rec])

    def save_to_file(self):
        with open('saved_info.txt', 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self):
        try:
            with open('saved_info.txt', 'rb') as file:
                contacts_archive = pickle.load(file)
                return contacts_archive
        except FileNotFoundError:
            return None

    def search_name(self, symbols):
        result = {}
        for name, data in self.data.items():
            if symbols in name.lower():
                result[name] = data.phones
        return result

    def search_phone(self, symbols):
        result = {}
        for name, data in self.data.items():
            for rec in data.phones:
                if symbols in rec.value:
                    result[name] = data.phones
        return result


class Record:
    def __init__(self, new_name, birthday=None):
        self.name = Name(new_name)
        self.phones = []
        self.birthday = None

    def add_phone(self, new_phone):
        if not Phone.is_phone_valid(new_phone):
            print('not valid phone')
            return
        adding_phone = Phone()
        adding_phone.value = new_phone
        self.phones.append(adding_phone)

    def change_phone(self, old_phone, new_phone):
        if not Phone.is_phone_valid(new_phone):
            print('not valid phone')
            return
        for phone in self.phones:
            if phone.value == old_phone:
                changing = Phone()
                changing.value = new_phone
                self.phones.append(changing)
                self.phones.remove(phone)
            else:
                print('Cant find this phone number')

    def remove_phone(self, old_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.phones.remove(phone)
            else:
                print('cant find this phone number')

    def add_birthday(self, birthday):
        if not Birthday.is_birthday_valid(birthday):
            print('not valid birthday, enter "year.month.day')
            return
        birthding = Birthday()
        birthding.value = birthday
        self.birthday = birthding

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            if self.birthday.value.replace(year=today.year) >= today:
                result = self.birthday.value.replace(
                    year=today.year) - today
            else:
                result = self.birthday.value.replace(
                    year=today.year) - today.replace(year=today.year - 1)
            print(result)
        else:
            print('empty')

    def __repr__(self):
        return f'{self.phones}'


class Field:
    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    def __init__(self, name):
        self.value = name


class Phone(Field):
    @Field.value.setter
    def value(self, phone):
        self._value = phone

    @classmethod
    def is_phone_valid(cls, value):
        return 10 <= len(value) <= 12

    def __repr__(self):
        return self._value


class Birthday(Field):
    @Field.value.setter
    def value(self, birthday):
        self._value = datetime.strptime(birthday, '%Y.%m.%d').date()

    @classmethod
    def is_birthday_valid(cls, value):
        return 0 < int(value.split('.')[0]) <= datetime.now().date().year and 0 < int(value.split('.')[1]) <= 12 and 0 < int(value.split('.')[2]) <= 31

    def __repr__(self):
        return self._value


addressbook = AddressBook()


def input_error(funk):
    def inner(text_input=None):
        try:
            if len(text_input.split()) > 3:
                print('to many parameters')
                return
            if len(text_input.split()) == 3:
                text_input.split()[1] == str(text_input.split()[1])
                text_input.split()[2] == int(text_input.split()[2])
            return funk(text_input)
        except (AttributeError, IndexError, ValueError, KeyError):
            print('Enter name or phone correctly')
    return inner


def hello(_=None):
    print('How can I help you?')


def show_all(_=None):
    page_number = int(input('enter page number pls: '))
    page_size = int(input('enter how many record we need:  '))
    doit = addressbook.iterator(page_number, page_size)
    print(next(doit))


@ input_error
def add(text_input: str):
    if text_input.split()[1] not in addressbook.data:
        adding = Record(text_input.split()[1])
        adding.add_phone(text_input.split()[2])
        addressbook.add_record(adding)
        print('added')
    else:
        adder = addressbook.data[text_input.split()[1]]
        adder.add_phone(text_input.split()[2])
        print('Done')


@ input_error
def change(text_input: str):
    if text_input.split()[1] in addressbook.data:
        old_phone = input('enter old phone number what you want to change ')
        changing = addressbook.data[text_input.split()[1]]
        changing.change_phone(old_phone, text_input.split()[2])
        print('changed')
    else:
        print('no contact')


@ input_error
def delete_contact(text_input: str):
    if text_input.split()[1] in addressbook.data:
        addressbook.data.pop(text_input.split()[1])
        print('Done')


@ input_error
def remove_phone(text_input: str):
    if text_input.split()[1] in addressbook.data:
        removing = addressbook.data[text_input.split()[1]]
        removing.remove_phone(text_input.split()[2])
        print('Done')


@ input_error
def phone(text_input: str):
    if text_input.split()[1] in addressbook.data:
        print(addressbook.data[text_input.split()[1]])
    else:
        print('This contact doesnt exist')


def set_birthday(text_input: str):
    if len(text_input.split()) != 3:
        print('too long or too short command')
    if text_input.split()[1] in addressbook.data:
        try:
            setting = addressbook.data[text_input.split()[1]]
            setting.add_birthday(text_input.split()[2])
            print('done')
        except IndexError:
            print('enter "year.month.day"')


@ input_error
def show_birthday(text_input: str):
    birthding = addressbook.data[text_input.split()[1]]
    birthding.days_to_birthday()


@input_error
def find(text_input: str):
    result_from_name = addressbook.search_name(text_input.split()[1])
    result_from_phone = addressbook.search_phone(text_input.split()[1])
    if not result_from_name:
        print(result_from_phone)
    else:
        print(result_from_name)


USER_INPUT = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': phone,
    'show all': show_all,
    'delete': delete_contact,
    'remove': remove_phone,
    'set_birthday': set_birthday,
    'birthday': show_birthday,
    'find': find
}


def main_bot():
    load_contacts_book = addressbook.load_from_file()
    if load_contacts_book:
        for key, value in load_contacts_book.items():
            addressbook.data[key] = value
    while True:
        user_input = input('Enter something  ')
        user_input = user_input.lower()
        if user_input == '.':
            addressbook.save_to_file()
            break
        if user_input in ('good bye', 'close', 'exit'):
            addressbook.save_to_file()
            print('Good bye!')
            break
        if user_input in USER_INPUT:
            USER_INPUT[user_input]()
        elif user_input.split()[0] in USER_INPUT:
            USER_INPUT[user_input.split()[0]](user_input)


main_bot()
