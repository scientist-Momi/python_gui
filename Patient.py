from Person import Person

class Patient(Person):
    def __init__(self, firstname, lastname, age, mobile, postcode, doctor=None):
        super().__init__(firstname, lastname, age, mobile)
        self.__postcode = postcode
        self.__doctor = doctor 
        self.__symptoms = [] 
        self.__family = []

    def get_postcode(self):
        return self.__postcode

    def get_doctor(self):
        return self.__doctor

    def set_postcode(self, postcode):
        self.__postcode = postcode
        
    def link_family_member(self, firstname, age, mobile, postcode):
        family_member = {"firstname": firstname, "age": age, "mobile": mobile, "postcode": postcode}
        self.__family.append(family_member)

    def get_family(self):
        return self.__family  

    def link(self, doctor):
        self.__doctor = doctor

    def add_symptom(self, symptom_list):
        unique_symptoms = [symptom for symptom in symptom_list if symptom not in self.__symptoms]
        self.__symptoms.extend(unique_symptoms)

    def get_symptoms(self):
        return self.__symptoms

