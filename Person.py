class Person:
    def __init__(self, firstname, lastname, age=None, mobile=None):
        self.__firstname = firstname
        self.__lastname = lastname
        self.__age = age
        self.__mobile = mobile

    def full_name(self):
        return f"{self.__firstname} {self.__lastname}"

    def get_firstname(self):
        return self.__firstname

    def set_firstname(self, firstname):
        self.__firstname = firstname

    def get_surname(self):
        return self.__lastname

    def set_surname(self, lastname):
        self.__lastname = lastname

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age

    def get_mobile(self):
        return self.__mobile

    def set_mobile(self, mobile):
        self.__mobile = mobile