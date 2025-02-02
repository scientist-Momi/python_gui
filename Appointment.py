class Appointment:
    def __init__(self, doctor, patient, datetime_obj):
        self.doctor = doctor
        self.patient = patient
        self.datetime = datetime_obj

    def get_doctor_fullname(self):
        return f"{self.doctor.full_name()}"

    def get_patient_fullname(self):
        return f"{self.patient.full_name()}"
    
    def get_date(self):
        return self.datetime