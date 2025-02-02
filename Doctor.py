from Person import Person

class Doctor(Person):
    def __init__(self, firstname, lastname, speciality):
        super().__init__(firstname, lastname)
        self.__speciality = speciality
        self.__patients = []

    def get_speciality(self) :
        return self.__speciality

    def set_speciality(self, new_speciality):
        self.__speciality = new_speciality

    def add_patient(self, patient):
        if patient not in self.__patients:
            self.__patients.append(patient)
        
    def remove_patient(self, patient):
        if patient in self.__patients:
            self.__patients.remove(patient)
    
    def get_patients(self):
        return self.__patients

    def __str__(self) :
        return f'{self.full_name():^30}|{self.__speciality:^15}'