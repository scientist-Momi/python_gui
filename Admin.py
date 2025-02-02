from Doctor import Doctor
from Patient import Patient
from Appointment import Appointment

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import matplotlib.pyplot as plt
# To install Matplotlib, run: pip install matplotlib

import csv
from collections import defaultdict, Counter


class Admin(ttk.Frame):
    def __init__(self, parent, username, password, address=""):
        ttk.Frame.__init__(self, parent)

        self.parent = parent
        self.login_window = None  
        self.dashboard_window = None 
        self.__username = username
        self.__password = password
        self.__address = address
        self.photo_image = tk.PhotoImage(file="graphics/logo.png").subsample(7, 7)
        self.doctor_icon = tk.PhotoImage(file="graphics/doctor.png").subsample(3, 3)
        self.patient_icon = tk.PhotoImage(file="graphics/patient.png").subsample(3, 3)
        self.dashboard_icon = tk.PhotoImage(file="graphics/dashboard.png").subsample(3, 3)
        self.logout_icon = tk.PhotoImage(file="graphics/logout.png").subsample(4, 4)
        self.darkmode_icon = tk.PhotoImage(file="graphics/darkmode.png").subsample(4, 4)
        self.lightmode_icon = tk.PhotoImage(file="graphics/light_mode.png").subsample(4, 4)
        self.new_icon = tk.PhotoImage(file="graphics/b_add.png").subsample(4, 4)
        self.search_icon = tk.PhotoImage(file="graphics/b_search.png").subsample(4, 4)
        self.update_icon = tk.PhotoImage(file="graphics/b_edit.png").subsample(4, 4)
        self.delete_icon = tk.PhotoImage(file="graphics/delete.png").subsample(4, 4)
        self.discharge_icon = tk.PhotoImage(file="graphics/discharge.png").subsample(4, 4)
        self.link_icon = tk.PhotoImage(file="graphics/link.png").subsample(4, 4)
        self.appointment_icon = tk.PhotoImage(file="graphics/appointment.png").subsample(4, 4)
        self.appointment_all = tk.PhotoImage(file="graphics/appointment_all.png").subsample(3, 3)
        self.delete_appointment_icon = tk.PhotoImage(file="graphics/delete_app.png").subsample(4, 4)
        self.profile_icon = tk.PhotoImage(file="graphics/profile.png").subsample(3, 3)
        self.setup_login()
        
        self.doctors = [Doctor('John','Smith','Internal Med.'), Doctor('Jone','Smith','Pediatrics'), Doctor('Jone','Carlos','Cardiology')]
        self.doctor_specialisations = [
            "",
            "Cardiology",
            "Dermatology",
            "Pediatrics",
            "Neurology",
            "Oncology",
            "Orthopedics",
            "Gastroenterology",
            "Psychiatry",
            "Radiology",
            "Ophthalmology"
        ]
        
        # self.patients = [Patient('Sara','Smith', 20, '07012345678','B1 234'), Patient('Mike','Jones', 37,'07555551234','L2 2AB'), Patient('Daivd','Smith', 15, '07123456789','C1 ABC')]
        self.patients = []
        self.discharged_patients = []
        
        self.symptom_choices = [
            "Fever", "Cough", "Fatigue", "Headache",
            "Sore Throat", "Shortness of Breath", "Nausea",
            "Diarrhea", "Chest Pain", "Loss of Smell"
        ]
        
        self.appointments = []
        
        self.data_file = "patients_data.csv" 

        self.load_patients_from_file()
        
# GETTER AND SETTERS FOR ADMIN
    def get_username(self):
        return self.__username
    def set_username(self, new_username):
        self.__username = new_username
    def get_password(self):
        return self.__password
    def set_password(self, new_Password):
        self.__password = new_Password
    def get_address(self):
        return self.__address
    def set_address(self, new_address):
        self.__address = new_address
        
        
# GUI FUNCTIONS

    def setup_login(self):
        self.parent.title("Hospital Management System")
        self.parent.iconphoto(True, self.photo_image)
        self.image_label = ttk.Label(image=self.photo_image)
        self.image_label.pack(padx=10, pady=10, anchor="center")
        self.login_frame = ttk.LabelFrame(self.parent, text="Login", padding=(20, 10))
        self.login_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.username_label = ttk.Label(self.login_frame, text="Username:")
        self.username_label.pack(anchor="w", padx=5, pady=5)
        self.username_entry = ttk.Entry(self.login_frame, width=30)
        self.username_entry.pack(padx=5, pady=5)

        self.password_label = ttk.Label(self.login_frame, text="Password:")
        self.password_label.pack(anchor="w", padx=5, pady=5)
        self.password_entry = ttk.Entry(self.login_frame, width=30, show="*")
        self.password_entry.pack(padx=5, pady=5)

        self.login_button = ttk.Button(
            self.login_frame, text="Login", style="Accent.TButton", command=self.check_login
        )
        self.login_button.pack(pady=10)

    def check_login(self):
        entered_username = self.username_entry.get().strip()
        entered_password = self.password_entry.get().strip()
        
        if not entered_username and not entered_password:
            messagebox.showerror(
                "Login Failed", "Fields cannot be empty. Please fill fields."
            )
            return

        if entered_username == self.__username and entered_password == self.__password:
            self.open_dashboard()
        else:
            messagebox.showerror(
                "Login Failed", "Invalid credentials. Please try again."
            )
    
    def change_theme(self):
        # Function that allows changing between dark and light theme
        current_theme = self.parent.tk.call("ttk::style", "theme", "use")
        if current_theme == "azure-light":
            self.parent.tk.call("set_theme", "dark")
            self.change_theme_button.config(image=self.lightmode_icon)
        else:
            self.parent.tk.call("set_theme", "light")
            self.change_theme_button.config(image=self.darkmode_icon)

    def open_dashboard(self):
        self.parent.withdraw()
        self.dashboard_window = tk.Toplevel(self.parent)
        self.dashboard_window.title("Hospital Management System - Dashboard")
        self.setup_window(self.dashboard_window, 1200, 900, True)
        self.setup_dashboard_ui(self.dashboard_window)
        
    def setup_window(self, window, width, height, resize):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x_position = (screen_width // 2) - (width // 2)
        y_position = (screen_height // 2) - (height // 2)

        window.resizable(resize, resize)
        # if not resize:
        #     window.update_idletasks()
        window.geometry(f"{width}x{height}+{x_position}+{y_position}")
        window.wm_minsize(width, height)
     
     
    #  Setting up different UIs
    def setup_dashboard_ui(self, window):
        self.notebook = ttk.Notebook(window)
        self.notebook.pack(fill="both", expand=True)

        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="Dashboard", padding=20, image=self.dashboard_icon, compound="left")
        self.setup_dashboard_view(self.dashboard_frame)

        self.patient_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.patient_frame, text="Patients", padding=20, image=self.patient_icon, compound="left")
        self.setup_patient_view(self.patient_frame)

        self.doctor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.doctor_frame, text="Doctors", padding=20, image=self.doctor_icon, compound="left")
        self.setup_doctor_view(self.doctor_frame)
        
        self.appointment_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.appointment_frame, text="Appointments", padding=20, image=self.appointment_all, compound="left")
        self.setup_appointment_view(self.appointment_frame)
        
        self.profile_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.profile_frame, text="Admin Profile", padding=20, image=self.profile_icon, compound="left")
        self.setup_profile_view(self.profile_frame)
        
        self.bottom_frame = ttk.Frame(window, padding=10)
        self.bottom_frame.pack(side="bottom", anchor="e", padx=10, pady=5, fill="x")

        self.change_theme_button = ttk.Button(self.bottom_frame, image=self.darkmode_icon, command=self.change_theme)
        self.change_theme_button.pack(side="right", padx=5)

        self.logout_button = ttk.Button(self.bottom_frame, image=self.logout_icon, command=self.logout)
        self.logout_button.pack(side="right", padx=5)
        
    def setup_new_patient_ui(self, window):
        welcome_label = ttk.Label(
            window, text="New Patient Form", font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)
        
        reg_patient_frame = ttk.LabelFrame(window, text="Patient Data", padding=(20, 10))
        reg_patient_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        firstname_label = ttk.Label(reg_patient_frame, text="First Name:")
        firstname_label.pack(anchor="w", padx=5, pady=5)
        firstname_entry = ttk.Entry(reg_patient_frame, width=30)
        firstname_entry.pack(padx=5, pady=5)

        lastname_label = ttk.Label(reg_patient_frame, text="Last Name:")
        lastname_label.pack(anchor="w", padx=5, pady=5)
        lastname_entry = ttk.Entry(reg_patient_frame, width=30)
        lastname_entry.pack(padx=5, pady=5)
        
        age_label = ttk.Label(reg_patient_frame, text="Age:")
        age_label.pack(anchor="w", padx=5, pady=5)
        age_entry = ttk.Entry(reg_patient_frame, width=30)
        age_entry.pack(padx=5, pady=5)
        
        mobile_label = ttk.Label(reg_patient_frame, text="Mobile Number:")
        mobile_label.pack(anchor="w", padx=5, pady=5)
        mobile_entry = ttk.Entry(reg_patient_frame, width=30)
        mobile_entry.pack(padx=5, pady=5)
        
        postcode_label = ttk.Label(reg_patient_frame, text="Postcode:")
        postcode_label.pack(anchor="w", padx=5, pady=5)
        postcode_entry = ttk.Entry(reg_patient_frame, width=30)
        postcode_entry.pack(padx=5, pady=5)
        
        reg_patient_button = ttk.Button(
            reg_patient_frame, text="Submit", style="Accent.TButton", command=lambda: self.add_patient(firstname_entry, lastname_entry, age_entry, mobile_entry, postcode_entry, window)
        )
        reg_patient_button.pack(pady=10)
        
    def setup_new_doctor_ui(self, window):
        welcome_label = ttk.Label(
            window, text="New Doctor Form", font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)
        
        reg_doctor_frame = ttk.LabelFrame(window, text="Doctor", padding=(20, 10))
        reg_doctor_frame.pack(padx=20, pady=20, fill="both", expand=True)

        firstname_label = ttk.Label(reg_doctor_frame, text="First Name:")
        firstname_label.pack(anchor="w", padx=5, pady=5)
        firstname_entry = ttk.Entry(reg_doctor_frame, width=30)
        firstname_entry.pack(padx=5, pady=5)

        lastname_label = ttk.Label(reg_doctor_frame, text="Last Name:")
        lastname_label.pack(anchor="w", padx=5, pady=5)
        lastname_entry = ttk.Entry(reg_doctor_frame, width=30)
        lastname_entry.pack(padx=5, pady=5)
        
        spec_label = ttk.Label(reg_doctor_frame, text="Specialization:")
        spec_label.pack(anchor="w", padx=5, pady=5)
        default_spec = tk.StringVar(value=self.doctor_specialisations[1])
        spec_options = ttk.OptionMenu(
            reg_doctor_frame, default_spec, *self.doctor_specialisations
        )
        spec_options.config(width=28)
        spec_options.pack(padx=5, pady=5)

        reg_doctor_button = ttk.Button(
            reg_doctor_frame, text="Submit", style="Accent.TButton", command=lambda: self.add_doctor(firstname_entry, lastname_entry, default_spec, window)
        )
        reg_doctor_button.pack(pady=10)
        
    def setup_update_doctor_ui(self, window):
        welcome_label = ttk.Label(
            window, text="Update Doctor Form", font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)

        update_doctor_frame = ttk.LabelFrame(window, text="Update Doctor", padding=(20, 10))
        update_doctor_frame.pack(padx=20, pady=20, fill="both", expand=True)

        doctor_id_label = ttk.Label(update_doctor_frame, text="Doctor ID:")
        doctor_id_label.pack(anchor="w", padx=5, pady=5)
        doctor_id_entry = ttk.Entry(update_doctor_frame, width=30)
        doctor_id_entry.pack(padx=5, pady=5)
        
        # Function to load doctor's data into the fields
        def load_doctor_info():
            try:
                doctor_index = int(doctor_id_entry.get()) 
                if doctor_index <= 0:
                    messagebox.showerror(
                        "Update Failed", "Invalid Doctor ID or Doctor not found!"
                    )
                    return
                doctor = self.doctors[doctor_index-1] 
                firstname_entry.delete(0, tk.END)
                firstname_entry.insert(0, doctor.get_firstname())
                lastname_entry.delete(0, tk.END)
                lastname_entry.insert(0, doctor.get_surname())
                default_spec.set(doctor.get_speciality())
                
                update_doctor_button.config(state="normal")

            except (ValueError, IndexError):
                messagebox.showerror(
                    "Update Failed", "Invalid Doctor ID or Doctor not found!"
                )

        load_button = ttk.Button(update_doctor_frame, text="Load Doctor Info", command=load_doctor_info)
        load_button.pack(pady=5)

        firstname_label = ttk.Label(update_doctor_frame, text="First Name:")
        firstname_label.pack(anchor="w", padx=5, pady=5)
        firstname_entry = ttk.Entry(update_doctor_frame, width=30)
        firstname_entry.pack(padx=5, pady=5)

        lastname_label = ttk.Label(update_doctor_frame, text="Last Name:")
        lastname_label.pack(anchor="w", padx=5, pady=5)
        lastname_entry = ttk.Entry(update_doctor_frame, width=30)
        lastname_entry.pack(padx=5, pady=5)

        spec_label = ttk.Label(update_doctor_frame, text="Specialization:")
        spec_label.pack(anchor="w", padx=5, pady=5)
        default_spec = tk.StringVar(value=self.doctor_specialisations[1])
        spec_options = ttk.OptionMenu(
            update_doctor_frame, default_spec, *self.doctor_specialisations
        )
        spec_options.config(width=28)
        spec_options.pack(padx=5, pady=5)

        update_doctor_button = ttk.Button(
            update_doctor_frame, text="Update", style="Accent.TButton", state="disabled", command=lambda: self.update_doctor(
                doctor_id_entry, firstname_entry, lastname_entry, default_spec, window
            )
        )
        update_doctor_button.pack(pady=10)
        
    def setup_update_patient_ui(self, window):
        welcome_label = ttk.Label(
            window, text="Update Patient Form", font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)

        update_patient_frame = ttk.LabelFrame(window, text="Patient Details", padding=(20, 10))
        update_patient_frame.pack(padx=20, pady=20, fill="both", expand=True)

        patient_id_label = ttk.Label(update_patient_frame, text="Patient ID:")
        patient_id_label.pack(anchor="w", padx=5, pady=5)
        patient_id_entry = ttk.Entry(update_patient_frame, width=30)
        patient_id_entry.pack(padx=5, pady=5)
        
        # Function to load patient's data into the fields
        def load_patient_info():
            try:
                patient_index = int(patient_id_entry.get()) 
                if patient_index <= 0:
                    messagebox.showerror(
                        "Update Failed", "Invalid Patient ID or Patient not found!"
                    )
                    return
                patient = self.patients[patient_index-1] 
                firstname_entry.delete(0, tk.END)
                firstname_entry.insert(0, patient.get_firstname())
                lastname_entry.delete(0, tk.END)
                lastname_entry.insert(0, patient.get_surname())
                age_entry.delete(0, tk.END)
                age_entry.insert(0, patient.get_age())
                mobile_entry.delete(0, tk.END)
                mobile_entry.insert(0, patient.get_mobile())
                postcode_entry.delete(0, tk.END)
                postcode_entry.insert(0, patient.get_postcode())
                patient_symptoms = patient.get_symptoms()  
                for symptom, var in symptom_vars.items():
                    var.set(symptom in patient_symptoms)
                
                update_patient_button.config(state="normal")

            except (ValueError, IndexError):
                messagebox.showerror(
                    "Update Failed", "Invalid Patient ID or Patient not found!"
                )

        load_button = ttk.Button(update_patient_frame, text="Load Patient Info", command=load_patient_info)
        load_button.pack(pady=5)

        firstname_label = ttk.Label(update_patient_frame, text="First Name:")
        firstname_label.pack(anchor="w", padx=5, pady=5)
        firstname_entry = ttk.Entry(update_patient_frame, width=30)
        firstname_entry.pack(padx=5, pady=5)

        lastname_label = ttk.Label(update_patient_frame, text="Last Name:")
        lastname_label.pack(anchor="w", padx=5, pady=3)
        lastname_entry = ttk.Entry(update_patient_frame, width=30)
        lastname_entry.pack(padx=5, pady=3)

        age_label = ttk.Label(update_patient_frame, text="Age:")
        age_label.pack(anchor="w", padx=5, pady=3)
        age_entry = ttk.Entry(update_patient_frame, width=30)
        age_entry.pack(padx=5, pady=3)
        
        mobile_label = ttk.Label(update_patient_frame, text="Mobile Number:")
        mobile_label.pack(anchor="w", padx=5, pady=3)
        mobile_entry = ttk.Entry(update_patient_frame, width=30)
        mobile_entry.pack(padx=5, pady=3)
        
        postcode_label = ttk.Label(update_patient_frame, text="Postcode:")
        postcode_label.pack(anchor="w", padx=5, pady=3)
        postcode_entry = ttk.Entry(update_patient_frame, width=30)
        postcode_entry.pack(padx=5, pady=3)
        
        update_patient_symptoms_frame = ttk.LabelFrame(window, text="Patient Symptoms", padding=(20, 10))
        update_patient_symptoms_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        symptoms_label = ttk.Label(update_patient_symptoms_frame, text="Symptoms:")
        symptoms_label.pack(anchor="w", padx=5, pady=3)
        
        symptom_vars = {}
        columns_per_row = 5
        symptoms_frame = ttk.Frame(update_patient_symptoms_frame)
        symptoms_frame.pack(fill="both", expand=True, padx=5, pady=3)
        row, col = 0, 0
        for symptom in self.symptom_choices:
            var = tk.BooleanVar()
            symptom_vars[symptom] = var
            ttk.Checkbutton(
                symptoms_frame,
                text=symptom,
                variable=var
            ).grid(row=row, column=col, padx=5, pady=3, sticky="w")
            
            col += 1
            if col >= columns_per_row: 
                col = 0
                row += 1
        
        update_patient_button = ttk.Button(
            update_patient_symptoms_frame, text="Update", style="Accent.TButton", state="disabled", command=lambda: self.update_patient(
                patient_id_entry, firstname_entry, lastname_entry, age_entry, mobile_entry, postcode_entry, symptom_vars, window
            )
        )
        update_patient_button.pack(pady=10)
        
    def setup_delete_doctor_ui(self, window):
        welcome_label = ttk.Label(
            window, text="Delete Doctor Form", font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)

        delete_doctor_frame = ttk.LabelFrame(window, text="Delete Doctor", padding=(20, 10))
        delete_doctor_frame.pack(padx=20, pady=20, fill="both", expand=True)

        doctor_id_label = ttk.Label(delete_doctor_frame, text="Doctor ID:")
        doctor_id_label.pack(anchor="w", padx=5, pady=5)
        doctor_id_entry = ttk.Entry(delete_doctor_frame, width=30)
        doctor_id_entry.pack(padx=5, pady=5)

        delete_doctor_button = ttk.Button(
            delete_doctor_frame, text="Delete", style="Accent.TButton", command=lambda: self.delete_doctor(
                doctor_id_entry, window
            )
        )
        delete_doctor_button.pack(pady=10)
        
    def setup_delete_appointment_ui(self, window):
        welcome_label = ttk.Label(
            window, text="Delete Appointmnet Form", font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)

        delete_appointment_frame = ttk.LabelFrame(window, text="Delete Appointment", padding=(20, 10))
        delete_appointment_frame.pack(padx=20, pady=20, fill="both", expand=True)

        appointment_id_label = ttk.Label(delete_appointment_frame, text="Appointment ID:")
        appointment_id_label.pack(anchor="w", padx=5, pady=5)
        appointment_id_entry = ttk.Entry(delete_appointment_frame, width=30)
        appointment_id_entry.pack(padx=5, pady=5)

        delete_appointment_button = ttk.Button(
            delete_appointment_frame, text="Delete", style="Accent.TButton", command=lambda: self.delete_appointment(
                appointment_id_entry, window
            )
        )
        delete_appointment_button.pack(pady=10)
        
    def setup_new_appointment_ui(self, window):
        welcome_label = ttk.Label(
            window, text="New Appointment Form", font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)

        reg_appointment_frame = ttk.LabelFrame(window, text="Appointment Data", padding=(20, 10))
        reg_appointment_frame.pack(padx=20, pady=20, fill="both", expand=True)

        doctor_id_label = ttk.Label(reg_appointment_frame, text="Doctor ID:")
        doctor_id_label.pack(anchor="w", padx=5, pady=5)
        doctor_id_entry = ttk.Entry(reg_appointment_frame, width=30)
        doctor_id_entry.pack(padx=5, pady=5)

        patient_id_label = ttk.Label(reg_appointment_frame, text="Patient ID:")
        patient_id_label.pack(anchor="w", padx=5, pady=5)
        patient_id_entry = ttk.Entry(reg_appointment_frame, width=30)
        patient_id_entry.pack(padx=5, pady=5)

        date_label = ttk.Label(reg_appointment_frame, text="Appointment Date (YYYY-MM-DD):")
        date_label.pack(anchor="w", padx=5, pady=5)

        date_frame = ttk.Frame(reg_appointment_frame)
        date_frame.pack(padx=5, pady=5)

        current_year = datetime.now().year
        year_spinbox = ttk.Spinbox(date_frame, from_=2025, to=current_year + 10, width=8, justify="center")
        year_spinbox.set(2025)
        year_spinbox.grid(row=0, column=0, padx=5)

        month_spinbox = ttk.Spinbox(date_frame, from_=1, to=12, width=6, justify="center")
        month_spinbox.set(1)
        month_spinbox.grid(row=0, column=1, padx=5)

        day_spinbox = ttk.Spinbox(date_frame, from_=1, to=31, width=6, justify="center")
        day_spinbox.set(1)
        day_spinbox.grid(row=0, column=2, padx=5)

        time_label = ttk.Label(reg_appointment_frame, text="Appointment Time (HH:MM):")
        time_label.pack(anchor="w", padx=5, pady=5)

        time_frame = ttk.Frame(reg_appointment_frame)
        time_frame.pack(padx=5, pady=5)

        hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, width=6, justify="center")
        hour_spinbox.set(12)
        hour_spinbox.grid(row=0, column=0, padx=5)

        minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, width=6, justify="center")
        minute_spinbox.set(0)
        minute_spinbox.grid(row=0, column=1, padx=5)

        # Function that gets the day and time values and concatenate them before saving the appointent
        def get_appointment_datetime():
            year = year_spinbox.get()
            month = month_spinbox.get()
            day = day_spinbox.get()
            hour = hour_spinbox.get()
            minute = minute_spinbox.get()
            try:
                appointment_datetime = f"{year}-{int(month):02d}-{int(day):02d} {int(hour):02d}:{int(minute):02d}"
                return appointment_datetime
            except ValueError:
                messagebox.showerror("Invalid Date/Time", "Please select a valid date and time.")
                return None

        reg_appointment_button = ttk.Button(
            reg_appointment_frame, text="Submit", style="Accent.TButton", command=lambda: self.add_appointment(
                doctor_id_entry, patient_id_entry, get_appointment_datetime(), window
            )
        )
        reg_appointment_button.pack(pady=10)

    def setup_assign_doctor_ui(self, window):
        welcome_label = ttk.Label(
            window, text="Assign Doctor Form", font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)

        pick_patient_frame = ttk.LabelFrame(window, text="Pick Patient", padding=(20, 10))
        pick_patient_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        patient_id_label = ttk.Label(pick_patient_frame, text="Patient ID:")
        patient_id_label.pack(anchor="w", padx=5, pady=5)
        patient_id_entry = ttk.Entry(pick_patient_frame, width=30)
        patient_id_entry.pack(padx=5, pady=5)

        pick_doctor_frame = ttk.LabelFrame(window, text="Pick Doctor", padding=(20, 10))
        pick_doctor_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.setup_doctor_table_for_patient(pick_doctor_frame)
        
        doctor_id_label = ttk.Label(pick_doctor_frame, text="Doctor ID:")
        doctor_id_label.pack(anchor="w", padx=5, pady=5)
        doctor_id_entry = ttk.Entry(pick_doctor_frame, width=30)
        doctor_id_entry.pack(padx=5, pady=5)

        assign_doctor_button = ttk.Button(
            pick_doctor_frame, text="Assign", style="Accent.TButton", command=lambda: self.assign_doctor(
                patient_id_entry, doctor_id_entry, window
            )
        )
        assign_doctor_button.pack(pady=10)
        
    def setup_discharge_patient_ui(self, window):
        welcome_label = ttk.Label(
            window, text="Discharge Patient Form", font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)

        discharge_patient_frame = ttk.LabelFrame(window, text="Discharge Patient", padding=(20, 10))
        discharge_patient_frame.pack(padx=20, pady=20, fill="both", expand=True)

        patient_id_label = ttk.Label(discharge_patient_frame, text="Patient ID:")
        patient_id_label.pack(anchor="w", padx=5, pady=5)
        patient_id_entry = ttk.Entry(discharge_patient_frame, width=30)
        patient_id_entry.pack(padx=5, pady=5)

        discharge_patient_button = ttk.Button(
            discharge_patient_frame, text="Discharge", style="Accent.TButton", command=lambda: self.discharge_patient(
                patient_id_entry, window
            )
        )
        discharge_patient_button.pack(pady=10)
        
    def setup_single_patient_ui(self, window, patient):
        welcome_label = ttk.Label(
            window, text="Patient Details", font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)
        
        family_frame = ttk.LabelFrame(window, text="Family Members", padding=(20, 10))
        family_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.setup_family_table(family_frame, patient)
        
    def setup_single_doctor_ui(self, window, doctor):
        welcome_label = ttk.Label(
            window, text="Doctor Details", font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)
        
        patient_frame = ttk.LabelFrame(window, text="Assigned Patients", padding=(20, 10))
        patient_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.setup_assigned_patients_table(patient_frame, doctor)


    # Settng up different views/pages
    def setup_dashboard_view(self, frame):
        welcome_label = ttk.Label(
            frame, text="Welcome to the Dashboard!", font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)

        logout_button = ttk.Button(frame, text="Logout", command=self.logout)
        logout_button.pack(pady=10)

        stats_frame = ttk.Frame(frame)
        stats_frame.pack(padx=20, pady=20, fill="x")

        doctors_frame = ttk.LabelFrame(stats_frame, text="Total Doctors", padding=(20, 10))
        doctors_frame.pack(side="left", padx=10, fill="both", expand=True)

        doctors_icon = ttk.Label(doctors_frame, text="🩺", font=("Helvetica", 30))
        doctors_icon.pack()

        self.total_doctors_label = ttk.Label(doctors_frame, text=str(len(self.doctors)), font=("Helvetica", 24))
        self.total_doctors_label.pack()

        patients_frame = ttk.LabelFrame(stats_frame, text="Total Patients", padding=(20, 10))
        patients_frame.pack(side="left", padx=10, fill="both", expand=True)

        patients_icon = ttk.Label(patients_frame, text="👥", font=("Helvetica", 30))
        patients_icon.pack()

        self.total_patients_label = ttk.Label(patients_frame, text=str(len(self.patients)), font=("Helvetica", 24))
        self.total_patients_label.pack()

        appointments_frame = ttk.LabelFrame(stats_frame, text="Total Appointments", padding=(20, 10))
        appointments_frame.pack(side="left", padx=10, fill="both", expand=True)

        appointments_icon = ttk.Label(appointments_frame, text="📅", font=("Helvetica", 30))
        appointments_icon.pack()

        self.total_appointments_label = ttk.Label(appointments_frame, text=str(len(self.appointments)), font=("Helvetica", 24))
        self.total_appointments_label.pack()
        
        table_frame = ttk.Frame(frame)
        table_frame.pack(padx=20, pady=20, fill="both", expand=True)

        table_frame.columnconfigure(0, weight=1)
        table_frame.columnconfigure(1, weight=1)
        table_frame.columnconfigure(2, weight=1)

        patients_frame = ttk.LabelFrame(
            table_frame, text="Total Number of Patients per Doctor", padding=(20, 10)
        )
        patients_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        button_one_frame = ttk.Frame(patients_frame)
        button_one_frame.pack(padx=5, pady=5, fill="x")
        show_one_button = ttk.Button(button_one_frame, text="View Diagram", command=self.plot_patient_per_doctor)
        show_one_button.pack(side="right", pady=10)
        self.setup_stat_one_table(patients_frame)

        appointments_frame = ttk.LabelFrame(
            table_frame, text="Total Appointments per Month per Doctor", padding=(20, 10)
        )
        appointments_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        button_two_frame = ttk.Frame(appointments_frame)
        button_two_frame.pack(padx=5, pady=5, fill="x")
        show_two_button = ttk.Button(button_two_frame, text="View Diagram", command=self.plot_appointments_per_month)
        show_two_button.pack(side="right", pady=10)
        self.setup_stat_two_table(appointments_frame)

        illness_frame = ttk.LabelFrame(
            table_frame, text="Patients Based on Illness Type", padding=(20, 10)
        )
        illness_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        button_three_frame = ttk.Frame(illness_frame)
        button_three_frame.pack(padx=5, pady=5, fill="x")
        show_three_button = ttk.Button(button_three_frame, text="View Diagram", command=self.plot_patients_by_illness)
        show_three_button.pack(side="right", pady=10)
        self.setup_stat_three_table(illness_frame)
        
    def setup_patient_view(self, frame):
        top_frame = ttk.Frame(frame)
        top_frame.pack(side="top", anchor="w", fill="x")
        
        patient_label = ttk.Label(
            top_frame, text="Manage Patients", font=("Helvetica", 16)
        )
        patient_label.pack(side="left", padx=5)
        
        discharge_patient_button = ttk.Button(top_frame,  text="Discharge", compound="left", padding=2, image=self.discharge_icon, command=self.open_discharge_patient)
        discharge_patient_button.pack(side="right", padx=5)
        assign_doctor_button = ttk.Button(top_frame, text="Assign", compound="left", padding=2, image=self.link_icon, command=self.open_assign_doctor)
        assign_doctor_button.pack(side="right", padx=5)
        edit_patient_button = ttk.Button(top_frame, text="Update", compound="left", padding=2, image=self.update_icon, command=self.open_update_patient)
        edit_patient_button.pack(side="right", padx=5)
        new_patient_button = ttk.Button(top_frame, image=self.new_icon, text="New", padding=2, compound="left", command=self.open_new_patient)
        new_patient_button.pack(side="right", padx=5)
        
        mid_frame = ttk.Frame(frame)
        mid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.setup_patient_table(mid_frame)
        
        top_frame2 = ttk.Frame(frame)
        top_frame2.pack(side="top", anchor="w", fill="x")
        
        discharged_patient_label = ttk.Label(
            top_frame2, text="Discharged Patients", font=("Helvetica", 16)
        )
        discharged_patient_label.pack(side="left", padx=5)
        
        mid_frame2 = ttk.Frame(frame)
        mid_frame2.pack(fill="both", expand=True, padx=10, pady=10)
        self.setup_discharged_patient_table(mid_frame2)
        
    def setup_doctor_view(self, frame):
        top_frame = ttk.Frame(frame)
        top_frame.pack(side="top", anchor="w", fill="x")
        
        doctor_label = ttk.Label(
            top_frame, text="Manage Doctors", font=("Helvetica", 16)
        )
        doctor_label.pack(side="left", padx=5)

        delete_doctor_button = ttk.Button(top_frame, text="Delete", compound="left", padding=2, image=self.delete_icon, command=self.open_delete_doctor)
        delete_doctor_button.pack(side="right", padx=5)
        edit_doctor_button = ttk.Button(top_frame, text="Update", compound="left", padding=2, image=self.update_icon, command=self.open_update_doctor)
        edit_doctor_button.pack(side="right", padx=5)
        new_doctor_button = ttk.Button(top_frame, text="New", compound="left", padding=2, image=self.new_icon, command=self.open_new_doctor)
        new_doctor_button.pack(side="right", padx=5)

        mid_frame = ttk.Frame(frame)
        mid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.setup_doctor_table(mid_frame)
        
    def setup_appointment_view(self, frame):
        top_frame = ttk.Frame(frame)
        top_frame.pack(side="top", anchor="w", fill="x")
        
        appointment_label = ttk.Label(
            top_frame, text="Manage Appointments", font=("Helvetica", 16)
        )
        appointment_label.pack(side="left", padx=5)

        delete_appointment_button = ttk.Button(top_frame, text="Delete", compound="left", padding=2, image=self.delete_appointment_icon, command=self.open_delete_appointment)
        delete_appointment_button.pack(side="right", padx=5)
        new_appointment_button = ttk.Button(top_frame, text="New", compound="left", padding=2, image=self.appointment_icon, command=self.open_new_appointment)
        new_appointment_button.pack(side="right", padx=5)

        mid_frame = ttk.Frame(frame)
        mid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.setup_appointment_table(mid_frame)
        
    def setup_profile_view(self, frame):
        top_frame = ttk.Frame(frame)
        top_frame.pack(side="top", anchor="w", fill="x")
        
        admin_label = ttk.Label(
            top_frame, text="Manage Admin", font=("Helvetica", 16)
        )
        admin_label.pack(side="left", padx=5)
        
        admin_details_frame = ttk.LabelFrame(frame, text="Admin Details", padding=(20, 10))
        admin_details_frame.pack(padx=20, pady=20, fill="both", expand=True)

        current_username = self.get_username() 
        current_address = self.get_address()    
        current_password = self.get_password()

        admin_username_label = ttk.Label(admin_details_frame, text="Admin Username:")
        admin_username_label.pack(anchor="w", padx=5, pady=5)
        admin_username_entry = ttk.Entry(admin_details_frame, width=30)
        admin_username_entry.insert(0, current_username) 
        admin_username_entry.pack(padx=5, pady=5)

        admin_address_label = ttk.Label(admin_details_frame, text="Admin Address:")
        admin_address_label.pack(anchor="w", padx=5, pady=5)
        admin_address_entry = ttk.Entry(admin_details_frame, width=30)
        admin_address_entry.insert(0, current_address)  
        admin_address_entry.pack(padx=5, pady=5)

        admin_password_label = ttk.Label(admin_details_frame, text="Admin Password:")
        admin_password_label.pack(anchor="w", padx=5, pady=5)
        admin_password_entry = ttk.Entry(admin_details_frame, width=30, show="*") 
        admin_password_entry.insert(0, current_password)  
        admin_password_entry.pack(padx=5, pady=5)

        update_button = ttk.Button(
            admin_details_frame, text="Update", style="Accent.TButton", command=lambda: self.update_admin_details(
                admin_username_entry, admin_address_entry, admin_password_entry
            )
        )
        update_button.pack(pady=10)
        
        
    # Functions for opening different mini windows(modals) that allows different operations
    def open_new_doctor(self):
        modal = self.open_modal("New Doctor", 450, 425)
        self.setup_new_doctor_ui(modal)
        
    def open_update_doctor(self):
        modal = self.open_modal("Update Doctor", 450, 550)
        self.setup_update_doctor_ui(modal)
        
    def open_delete_doctor(self):
        modal = self.open_modal("Delete a Doctor", 450, 300)
        self.setup_delete_doctor_ui(modal)
    
    def open_new_patient(self):
        modal = self.open_modal("New Patient", 470, 570)
        self.setup_new_patient_ui(modal)
        
    def open_patient_modal(self, patient):
        modal = self.open_modal(f"Patient {patient.full_name()}", 470, 570)
        self.setup_single_patient_ui(modal, patient)
        
    def open_doctor_modal(self, doctor):
        modal = self.open_modal(f"Doctor {doctor.full_name()}", 800, 570)
        self.setup_single_doctor_ui(modal, doctor)
        
    def open_discharge_patient(self):
        modal = self.open_modal("Discharge a Patient", 470, 300)
        self.setup_discharge_patient_ui(modal)
        
    def open_assign_doctor(self):
        modal = self.open_modal("Assign a Doctor", 670, 810)
        self.setup_assign_doctor_ui(modal)
        
    def open_update_patient(self):
        modal = self.open_modal("Update Patient", 670, 850)
        self.setup_update_patient_ui(modal)
        
    def open_new_appointment(self):
        modal = self.open_modal("New Appointment", 450, 525)
        self.setup_new_appointment_ui(modal)
        
    def open_delete_appointment(self):
        modal = self.open_modal("Delete an Appointment", 450, 300)
        self.setup_delete_appointment_ui(modal)
        
    def open_modal(self, title, width, height):
        modal = tk.Toplevel(self.dashboard_window)
        modal.title(title)

        parent_x = self.dashboard_window.winfo_x()
        parent_y = self.dashboard_window.winfo_y()
        parent_width = self.dashboard_window.winfo_width()
        parent_height = self.dashboard_window.winfo_height()

        x_position = parent_x + (parent_width // 2) - (width // 2)
        y_position = parent_y + (parent_height // 2) - (height // 2)

        modal.geometry(f"{width}x{height}+{x_position}+{y_position}")

        modal.transient(self.dashboard_window)  
        modal.grab_set()                       
        modal.resizable(False, False)          
        return modal
        

    # Function that refreshes the statistics shown on the dashboard view
    def refresh_statistics(self):
        self.total_doctors_label.config(text=str(len(self.doctors)))
        self.total_patients_label.config(text=str(len(self.patients)))
        self.total_appointments_label.config(text=str(len(self.appointments)))

        
    # Setting up all the tables used all over the application     
    def setup_doctor_table(self, frame):
        columns = ("id", "first_name", "last_name", "specialization")
        self.doctor_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        self.doctor_tree.heading("id", text="ID")
        self.doctor_tree.heading("first_name", text="First Name")
        self.doctor_tree.heading("last_name", text="Last Name")
        self.doctor_tree.heading("specialization", text="Specialization")

        self.doctor_tree.column("id", width=50, anchor="center")
        self.doctor_tree.column("first_name", width=150, anchor="center")
        self.doctor_tree.column("last_name", width=150, anchor="center")
        self.doctor_tree.column("specialization", width=200, anchor="center")

        self.update_doctor_treeview()
        self.doctor_tree.pack(fill="both", expand=True)
        
        self.doctor_tree.bind("<<TreeviewSelect>>", self.on_doctor_item_selected)
     
    def setup_appointment_table(self, frame):
        columns = ("id", "patient", "doctor", "datetime")
        self.appointment_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        self.appointment_tree.heading("id", text="ID")
        self.appointment_tree.heading("patient", text="Patient")
        self.appointment_tree.heading("doctor", text="Doctor")
        self.appointment_tree.heading("datetime", text="Date & Time")

        self.appointment_tree.column("id", width=50, anchor="center")
        self.appointment_tree.column("patient", width=150, anchor="center")
        self.appointment_tree.column("doctor", width=150, anchor="center")
        self.appointment_tree.column("datetime", width=200, anchor="center")

        self.update_appointment_treeview()
        self.appointment_tree.pack(fill="both", expand=True)
        
    def setup_doctor_table_for_patient(self, frame):
        columns = ("id", "fullname", "specialization")
        self.doctor_tree_for_patient = ttk.Treeview(frame, columns=columns, show="headings", height=7)

        self.doctor_tree_for_patient.heading("id", text="ID")
        self.doctor_tree_for_patient.heading("fullname", text="Name")
        self.doctor_tree_for_patient.heading("specialization", text="Specialization")

        self.doctor_tree_for_patient.column("id", width=50, anchor="center")
        self.doctor_tree_for_patient.column("fullname", width=150, anchor="center")
        self.doctor_tree_for_patient.column("specialization", width=200, anchor="center")

        self.update_doctor_treeview_for_patient()
        self.doctor_tree_for_patient.pack(fill="both", expand=True)
        
    def setup_family_table(self, frame, patient):
        columns = ("id", "fullname", "age", "mobile")
        self.family_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        self.family_tree.heading("id", text="ID")
        self.family_tree.heading("fullname", text="Name")
        self.family_tree.heading("age", text="Age")
        self.family_tree.heading("mobile", text="Mobile")

        self.family_tree.column("id", width=30, anchor="center")
        self.family_tree.column("fullname", width=120, anchor="center")
        self.family_tree.column("age", width=30, anchor="center")
        self.family_tree.column("mobile", width=100, anchor="center")

        self.update_family_treeview(patient)
        self.family_tree.pack(fill="both", expand=True)
        
    def setup_assigned_patients_table(self, frame, doctor):
        columns = ("id", "fullname", "age", "mobile", "symptoms")
        self.assigned_patients_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        self.assigned_patients_tree.heading("id", text="ID")
        self.assigned_patients_tree.heading("fullname", text="Name")
        self.assigned_patients_tree.heading("age", text="Age")
        self.assigned_patients_tree.heading("mobile", text="Mobile")
        self.assigned_patients_tree.heading("symptoms", text="Symptoms")

        self.assigned_patients_tree.column("id", width=20, anchor="center")
        self.assigned_patients_tree.column("fullname", width=100, anchor="center")
        self.assigned_patients_tree.column("age", width=25, anchor="center")
        self.assigned_patients_tree.column("mobile", width=100, anchor="center")
        self.assigned_patients_tree.column("symptoms", width=350, anchor="center")

        self.update_assigned_patients_treeview(doctor)
        self.assigned_patients_tree.pack(fill="both", expand=True)
        
    def setup_discharged_patient_table(self, frame):
        columns = ("id", "fullname", "doctor_name", "age", "mobile", "postcode", "symptoms")
        self.discharged_patient_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        self.discharged_patient_tree.heading("id", text="ID")
        self.discharged_patient_tree.heading("fullname", text="Name")
        self.discharged_patient_tree.heading("doctor_name", text="Doctor's Name")
        self.discharged_patient_tree.heading("age", text="Age")
        self.discharged_patient_tree.heading("mobile", text="Mobile")
        self.discharged_patient_tree.heading("postcode", text="Postcode")
        self.discharged_patient_tree.heading("symptoms", text="Symptoms")

        self.discharged_patient_tree.column("id", width=25, anchor="center")
        self.discharged_patient_tree.column("fullname", width=100, anchor="center")
        self.discharged_patient_tree.column("doctor_name", width=100, anchor="center")
        self.discharged_patient_tree.column("age", width=25, anchor="center")
        self.discharged_patient_tree.column("mobile", width=100, anchor="center")
        self.discharged_patient_tree.column("postcode", width=100, anchor="center")
        self.discharged_patient_tree.column("symptoms", width=450, anchor="center")

        self.update_discharged_patient_treeview()
        self.discharged_patient_tree.pack(fill="both", expand=True)
    
    def setup_patient_table(self, frame):
        columns = ("id", "fullname", "doctor_name", "age", "mobile", "postcode", "symptoms")
        self.patient_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        self.patient_tree.heading("id", text="ID")
        self.patient_tree.heading("fullname", text="Name")
        self.patient_tree.heading("doctor_name", text="Doctor's Name")
        self.patient_tree.heading("age", text="Age")
        self.patient_tree.heading("mobile", text="Mobile")
        self.patient_tree.heading("postcode", text="Postcode")
        self.patient_tree.heading("symptoms", text="Symptoms")

        self.patient_tree.column("id", width=25, anchor="center")
        self.patient_tree.column("fullname", width=100, anchor="center")
        self.patient_tree.column("doctor_name", width=100, anchor="center")
        self.patient_tree.column("age", width=25, anchor="center")
        self.patient_tree.column("mobile", width=100, anchor="center")
        self.patient_tree.column("postcode", width=100, anchor="center")
        self.patient_tree.column("symptoms", width=450, anchor="center")

        self.update_patient_treeview()
        self.patient_tree.pack(fill="both", expand=True)
        
        self.patient_tree.bind("<<TreeviewSelect>>", self.on_item_selected)

    
    # setting up the tables that hold the statistics on the dashboard view
    def setup_stat_one_table(self, frame):
        columns = ("id", "doctor_name", "no_of_patients")
        self.stat_one_tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)

        self.stat_one_tree.heading("id", text="ID")
        self.stat_one_tree.heading("doctor_name", text="Doctor")
        self.stat_one_tree.heading("no_of_patients", text="Number of Patients")

        self.stat_one_tree.column("id", width=50, anchor="center")
        self.stat_one_tree.column("doctor_name", width=200, anchor="center")
        self.stat_one_tree.column("no_of_patients", width=150, anchor="center")

        self.update_stat_one_treeview()
        self.stat_one_tree.pack(fill="both", expand=True)

    def setup_stat_two_table(self, frame):
        columns = ("id", "doctor_name", "month", "no_of_appointments")
        self.stat_two_tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)

        self.stat_two_tree.heading("id", text="ID")
        self.stat_two_tree.heading("doctor_name", text="Doctor")
        self.stat_two_tree.heading("month", text="Month")
        self.stat_two_tree.heading("no_of_appointments", text="Number of Appointments")

        self.stat_two_tree.column("id", width=50, anchor="center")
        self.stat_two_tree.column("doctor_name", width=200, anchor="center")
        self.stat_two_tree.column("month", width=100, anchor="center")
        self.stat_two_tree.column("no_of_appointments", width=150, anchor="center")

        self.update_stat_two_treeview()
        self.stat_two_tree.pack(fill="both", expand=True)

    def setup_stat_three_table(self, frame):
        columns = ("illness", "no_of_patients")
        self.stat_three_tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)

        self.stat_three_tree.heading("illness", text="Illness")
        self.stat_three_tree.heading("no_of_patients", text="Number of Patients")

        self.stat_three_tree.column("illness", width=300, anchor="center")
        self.stat_three_tree.column("no_of_patients", width=150, anchor="center")

        self.update_stat_three_treeview()
        self.stat_three_tree.pack(fill="both", expand=True)

        
    # Functions that trigger when a row is clicked on the patient and doctor table
    def on_item_selected(self, event):
        selected_items = self.patient_tree.selection()
        if not selected_items:
            return
        selected_item = selected_items[0]
        patient = next((p for p in self.patients if f"patient-{self.patients.index(p)}" == selected_item), None)
        if patient:
            self.open_patient_modal(patient)

    def on_doctor_item_selected(self, event):
        selected_items = self.doctor_tree.selection()
        if not selected_items:
            return
        selected_item = selected_items[0]
        doctor = next((d for d in self.doctors if f"doctor-{self.doctors.index(d)}" == selected_item), None)
        if doctor:
            self.open_doctor_modal(doctor)


    # Function that populates the different tables with data and reloads the data whenever an operation takes place
    def update_doctor_treeview(self):
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)

        for index, doctor in enumerate(self.doctors):
            doctor_id = f"doctor-{index}"
            first_name = doctor.get_firstname()
            last_name = doctor.get_surname()
            specialization = doctor.get_speciality()
            self.doctor_tree.insert("", "end", iid=doctor_id, values=(index+1, first_name, last_name, specialization))
            
    def update_stat_one_treeview(self):
        for item in self.stat_one_tree.get_children():
            self.stat_one_tree.delete(item)

        for index, doctor in enumerate(self.doctors):
            doctor_name = f"{doctor.get_firstname()} {doctor.get_surname()}"
            assigned_patients = doctor.get_patients()
            num_patients = len(assigned_patients) 
            self.stat_one_tree.insert("", "end", values=(index + 1, doctor_name, num_patients))

    def update_stat_two_treeview(self):
        for item in self.stat_two_tree.get_children():
            self.stat_two_tree.delete(item)
        
        monthly_appointments = {}

        for appointment in self.appointments:
            doctor = appointment.doctor 
            doctor_name = doctor.full_name() 
            month = appointment.get_date().strftime("%B")
            key = (doctor_name, month)
            monthly_appointments[key] = monthly_appointments.get(key, 0) + 1

        for index, ((doctor_name, month), count) in enumerate(monthly_appointments.items()):
            self.stat_two_tree.insert("", "end", values=(index + 1, doctor_name, month, count))

    def update_stat_three_treeview(self):
        for item in self.stat_three_tree.get_children():
            self.stat_three_tree.delete(item)

        illness_counts = {}
        for patient in self.patients:
            for symptom in patient.get_symptoms():
                illness_counts[symptom] = illness_counts.get(symptom, 0) + 1

        for illness, count in illness_counts.items():
            self.stat_three_tree.insert("", "end", values=(illness, count))
   
    def update_appointment_treeview(self):
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)

        for index, appointment in enumerate(self.appointments):
            appointment_id = f"appointment-{index}"
            patient_name = appointment.get_patient_fullname()
            doctor_name = appointment.get_doctor_fullname()
            datetime = appointment.get_date()
            self.appointment_tree.insert("", "end", iid=appointment_id, values=(index+1, patient_name, doctor_name, datetime))
            
    def update_doctor_treeview_for_patient(self):
        for item in self.doctor_tree_for_patient.get_children():
            self.doctor_tree_for_patient.delete(item)

        for index, doctor in enumerate(self.doctors):
            fullname = doctor.full_name()
            specialization = doctor.get_speciality()
            self.doctor_tree_for_patient.insert("", "end", iid=index, values=(index+1, fullname, specialization))
            
    def update_patient_treeview(self):
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)

        for index, patient in enumerate(self.patients):
            parent_id = f"patient-{index}"
            fullname = patient.full_name()
            doctor = patient.get_doctor()
            if doctor is not None:
                doctor_name = doctor.full_name()  
            else:
                doctor_name = "No doctor assigned"
            age = patient.get_age()
            mobile = patient.get_mobile()
            postcode = patient.get_postcode()
            symptoms = ", ".join(patient.get_symptoms())
            self.patient_tree.insert("", "end", iid=parent_id, values=(index+1, fullname, doctor_name, age, mobile, postcode, symptoms))
            
    def update_discharged_patient_treeview(self):
        for item in self.discharged_patient_tree.get_children():
            self.discharged_patient_tree.delete(item)

        for index, patient in enumerate(self.discharged_patients):
            parent_id = f"patient-{index}"
            fullname = patient.full_name()
            doctor = patient.get_doctor()
            if doctor is not None:
                doctor_name = doctor.full_name()  
            else:
                doctor_name = "No doctor assigned"
            age = patient.get_age()
            mobile = patient.get_mobile()
            postcode = patient.get_postcode()
            symptoms = ", ".join(patient.get_symptoms())
            self.discharged_patient_tree.insert("", "end", iid=parent_id, values=(index+1, fullname, doctor_name, age, mobile, postcode, symptoms))
            
    def update_family_treeview(self, patient):
        for item in self.family_tree.get_children():
            self.family_tree.delete(item)

        family_members = patient.get_family()
        for family_index, family_member in enumerate(family_members, start=1):
            fullname = f"{family_member['firstname']} {patient.get_surname()}"
            family_age = family_member["age"]
            family_mobile = family_member["mobile"]
            self.family_tree.insert("", "end", iid=family_index, values=(family_index, fullname, family_age, family_mobile))
            
    def update_assigned_patients_treeview(self, doctor):
        for item in self.assigned_patients_tree.get_children():
            self.assigned_patients_tree.delete(item)

        assigned_patients = doctor.get_patients()
        for ap_index, ap in enumerate(assigned_patients, start=1):
            fullname = ap.full_name()
            age = ap.get_age()
            mobile = ap.get_mobile()
            symptoms = ", ".join(ap.get_symptoms())
            self.assigned_patients_tree.insert("", "end", iid=ap_index, values=(ap_index, fullname, age, mobile, symptoms))
            
            
# Functions to perform core functionalities
    def logout(self):
        self.dashboard_window.destroy()
        self.dashboard_window = None
        self.parent.deiconify()
        
    def add_patient(self, firstname_entry, lastname_entry, age_entry, mobile_entry, postcode_entry, window):
        firstname = firstname_entry.get().capitalize()
        lastname = lastname_entry.get().capitalize()
        age = age_entry.get()
        mobile = mobile_entry.get()
        postcode = postcode_entry.get()
        if not firstname or not lastname or not age or not mobile or not postcode:
            messagebox.showerror(
                "Registration Failed", "All fields must be filled out."
            )
            return
        
        # Check if there is a patient with similar lastname and ask if admin wants to link them
        matching_patients = [patient for patient in self.patients if patient.get_surname() == lastname]

        if matching_patients:
            related = messagebox.askyesno(
                "Possible Family Member Found",
                f"A patient with the last name '{lastname}' already exists. Do you want to link them?"
            )
            if related:
                # Create the new patient
                new_patient = Patient(firstname, lastname, age, mobile, postcode)

                # Link new patient to all existing matching patients
                for patient in matching_patients:
                    patient.link_family_member(firstname, age, mobile, postcode)
                    # Link each existing patient to the new patient
                    new_patient.link_family_member(
                        patient.get_firstname(), patient.get_age(), patient.get_mobile(), patient.get_postcode()
                    )

                # Add the linked new patient to the list
                self.patients.append(new_patient)

                messagebox.showinfo(
                    "Patient Added",
                    "Patient has been added and linked to the existing family."
                )
            else:
                # Create and add a separate patient 
                new_patient = Patient(firstname, lastname, age, mobile, postcode)
                self.patients.append(new_patient)

                messagebox.showinfo(
                    "Patient Added",
                    "Patient has been added as a separate entry."
                )
        else:
            # No matching patients; add a completely new patient
            new_patient = Patient(firstname, lastname, age, mobile, postcode)
            self.patients.append(new_patient)

            messagebox.showinfo(
                "Patient Added",
                "Patient has been added successfully."
            )

        # Save updated patient list to file
        self.save_patients_to_file()

        # Updates the UI and refreshes all data
        self.update_patient_treeview()
        self.refresh_statistics()
        window.destroy()

    def discharge_patient(self, patient_id_entry, window):
        try:
            patient_id = int(patient_id_entry.get())
            if patient_id < 1 or patient_id > len(self.patients):
                messagebox.showerror("Error", "Invalid Patient ID")
                return

            index = patient_id - 1
            
            # Get the patient to discharge
            patient_to_discharge = self.patients.pop(index)
            
            # Save to the discharged patients list
            self.discharged_patients.append(patient_to_discharge)
            
            # Refesh the saved patients file to remove discharged patient
            self.save_patients_to_file()
            self.update_patient_treeview()
            self.update_discharged_patient_treeview()
            self.refresh_statistics()
            messagebox.showinfo("Success", f"Patient '{patient_to_discharge.full_name()}' has been discharged.")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric Patient ID.")
        except IndexError:
            messagebox.showerror("Error", "Patient not found.")
            
    def assign_doctor(self, patient_id_entry, doctor_id_entry, window):
        try:
            patient_id = int(patient_id_entry.get()) - 1
            doctor_id = int(doctor_id_entry.get()) - 1

            # Get patient and doctor with their ID
            patient = self.patients[patient_id]
            doctor = self.doctors[doctor_id]

            # Check if patient already has a doctor assigned and if yes remove and assign the new one
            current_doctor = patient.get_doctor()
            if current_doctor is not None:
                current_doctor.remove_patient(patient)

            doctor.add_patient(patient)
            patient.link(doctor)

            # Refresh all data
            self.save_patients_to_file()
            messagebox.showinfo("Success", f"Doctor assigned successfully.")
            self.update_patient_treeview()
            self.update_stat_one_treeview()
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to assign doctor: {str(e)}")

    def add_doctor(self, firstname_entry, lastname_entry, specialization_entry, window):
        firstname = firstname_entry.get().strip().capitalize()
        lastname = lastname_entry.get().strip().capitalize()
        specialization = specialization_entry.get().strip()
        
        if not firstname or not lastname or not specialization:
            messagebox.showerror(
                "Registration Failed", "All fields must be filled out."
            )
            return
        
        if self.check_doctor_exist(firstname, lastname):
            messagebox.showerror(
                "Registration Failed", "Doctor already exists."
            )
        else:
            new_doctor = Doctor(firstname, lastname, specialization)
            self.doctors.append(new_doctor)
            messagebox.showinfo(
                "Doctor Added",
                "Doctor has been added successfully."
            )
            self.update_doctor_treeview()
            self.update_stat_one_treeview()
            self.refresh_statistics()
            window.destroy()
        
    def check_doctor_exist(self, firstname, surname):
        firstname = firstname.lower()
        surname = surname.lower()
        for doctor in self.doctors:
            if firstname == doctor.get_firstname().lower() and surname == doctor.get_surname().lower():
                return True
        return False
    
    def update_doctor(self, doctor_id_entry, firstname_entry, lastname_entry, default_spec, window):
        try:
            doctor_index = int(doctor_id_entry.get())
            doctor = self.doctors[doctor_index-1] 

            firstname = firstname_entry.get().strip()
            lastname = lastname_entry.get().strip()
            specialisation = default_spec.get()
            
            if not firstname or not lastname:
                messagebox.showerror(
                    "Update Failed", "All fields must be filled!"
                )
                return

            doctor.set_firstname(firstname.capitalize())
            doctor.set_surname(lastname.capitalize())
            doctor.set_speciality(specialisation)
            
            self.update_doctor_treeview()
            self.update_stat_two_treeview()
            self.update_stat_one_treeview()
            window.destroy() 
        except (ValueError, IndexError):
            messagebox.showerror(
                "Update Failed", "Invalid Doctor ID or Doctor not found!"
            )
            
    def update_patient(self, patient_id_entry, firstname_entry, lastname_entry, age_entry, mobile_entry, postcode_entry, symptom_vars, window):
        try:
            patient_index = int(patient_id_entry.get()) - 1
            patient = self.patients[patient_index]

            firstname = firstname_entry.get()
            lastname = lastname_entry.get()
            age = age_entry.get()
            mobile = mobile_entry.get()
            postcode = postcode_entry.get().upper()
            selected_symptoms = [
                symptom for symptom, var in symptom_vars.items() if var.get()
            ]
            
            if not firstname or not lastname or not age or not mobile or not postcode:
                messagebox.showerror(
                    "Update Failed", "All fields must be filled out."
                )
                return
            
            patient.set_firstname(firstname.capitalize())
            patient.set_surname(lastname.capitalize())
            patient.set_age(age)
            patient.set_mobile(mobile)
            patient.set_postcode(postcode)
            patient.add_symptom(selected_symptoms)

            self.save_patients_to_file()
            messagebox.showinfo("Success", "Patient updated successfully.")
            self.update_patient_treeview()
            self.update_stat_three_treeview()
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update patient: {str(e)}")
            
    def delete_doctor(self, doctor_id_entry, window):
        try:
            doctor_index = int(doctor_id_entry.get()) 
            doctor_index = doctor_index - 1
            if doctor_index < 0 or doctor_index >= len(self.doctors):
                messagebox.showerror(
                    "Delete Failed", "Invalid Doctor ID or Doctor not found!"
                )
                return
            
            doctor = self.doctors[doctor_index]
            doctor_name = f"{doctor.get_firstname()} {doctor.get_surname()}"

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete Doctor {doctor_name} (ID: {doctor_index+1})?"
            )

            if confirm:
                del self.doctors[doctor_index]

                self.update_doctor_treeview()
                self.refresh_statistics()
                window.destroy()
                
                messagebox.showinfo("Delete Successful", f"Doctor {doctor_name} has been deleted.")
        except ValueError:
            messagebox.showerror("Delete Failed", "Invalid Doctor ID! Please enter a valid number.")
        except IndexError:
            messagebox.showerror("Delete Failed", "Doctor not found! Please check the ID.")

    def add_appointment(self, doctor_id_entry, patient_id_entry, date_entry, window):
        try:
            doctor_id = int(doctor_id_entry.get())
            patient_id = int(patient_id_entry.get())

            if doctor_id < 1 or doctor_id > len(self.doctors):
                messagebox.showerror("Error", "Invalid Doctor ID")
                return
            
            if patient_id < 1 or patient_id > len(self.patients):
                messagebox.showerror("Error", "Invalid Patient ID")
                return
            
            appointment_date = datetime.strptime(date_entry, "%Y-%m-%d %H:%M")

            doctor = self.doctors[doctor_id - 1] 
            patient = self.patients[patient_id - 1] 
            appointment = Appointment(doctor, patient, appointment_date)
            self.appointments.append(appointment)
            self.update_appointment_treeview()
            self.refresh_statistics()
            self.update_stat_two_treeview()
            messagebox.showinfo("Success", f"Appointment has been scheduled for {patient.full_name()} with Dr. {doctor.full_name()} on {appointment_date}.")
            window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric IDs.")
        except IndexError:
            messagebox.showerror("Error", "Doctor or Patient not found.")

    def delete_appointment(self, appointment_id_entry, window):
        try:
            appointment_index = int(appointment_id_entry.get()) 
            appointment_index = appointment_index - 1
            if appointment_index < 0 or appointment_index >= len(self.appointments):
                messagebox.showerror(
                    "Delete Failed", "Invalid Appointment ID or Appointment not found!"
                )
                return
            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete the appointment?"
            )

            if confirm:
                del self.appointments[appointment_index]

                self.update_appointment_treeview()
                self.refresh_statistics()
                self.update_stat_two_treeview()
                window.destroy()
                
                messagebox.showinfo("Delete Successful", "Appointment has been deleted.")
        except ValueError:
            messagebox.showerror("Delete Failed", "Invalid Appointment ID! Please enter a valid number.")
        except IndexError:
            messagebox.showerror("Delete Failed", "Appointment not found! Please check the ID.")
        
    def update_admin_details(self, admin_username_entry, admin_address_entry, admin_password_entry):
        try:
            updated_username = admin_username_entry.get().strip()
            updated_address = admin_address_entry.get().strip()
            updated_password = admin_password_entry.get().strip()

            if not updated_username or not updated_address or not updated_password:
                messagebox.showerror("Input Error", "All fields must be filled in.")
                return

            self.set_username(updated_username)
            self.set_address(updated_address)
            self.set_password(updated_password)

            messagebox.showinfo("Success", "Admin details updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
      
      
# Function for drawing different diagrams for the admin reports 
    def plot_patient_per_doctor(self):
        doctors = [doctor.full_name() for doctor in self.doctors]
        patient_counts = [len(doctor.get_patients()) for doctor in self.doctors]

        plt.figure(figsize=(10, 6))
        plt.bar(doctors, patient_counts, color='skyblue')
        plt.xlabel('Doctors')
        plt.ylabel('Number of Patients')
        plt.title('Total Number of Patients per Doctor')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        manager = plt.get_current_fig_manager()
        manager.window.geometry('800x600') 
        plt.show()
        
    def plot_appointments_per_month(self):
        appointments_per_month = defaultdict(lambda: defaultdict(int))

        for appointment in self.appointments:
            month = appointment.get_date().strftime('%B')
            doctor_name = appointment.get_doctor_fullname()
            appointments_per_month[doctor_name][month] += 1
            
        if not appointments_per_month:
            messagebox.showerror(
                    "Warning", "No data available for appointments."
                )
            return

        markers = ['o', 's', '^', 'D', 'x', '+', '*']

        for idx, (doctor_name, months) in enumerate(appointments_per_month.items()):
            months_sorted = sorted(months.items())
            months, counts = zip(*months_sorted)
            
            plt.plot(months, counts, label=doctor_name, marker=markers[idx % len(markers)], linestyle='-', markersize=8)

        plt.xlabel('Month')
        plt.ylabel('Number of Appointments')
        plt.title('Total Appointments per Month per Doctor')
        plt.legend()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def plot_patients_by_illness(self):
        illness_data = [illness for patient in self.patients for illness in patient.get_symptoms()]
        illness_counts = Counter(illness_data)

        plt.figure(figsize=(8, 8))
        plt.pie(illness_counts.values(), labels=illness_counts.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Patients Based on Illness Type')
        plt.show()


# Functions to both save patients data and load to a CSV file
    def save_patients_to_file(self):
        try:
            with open(self.data_file, 'w', newline='') as file:
                fieldnames = ['firstname', 'lastname', 'age', 'mobile', 'postcode', 'doctor', 'symptoms', 'family_members']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for patient in self.patients:
                    family_members = ";".join([
                        f"{member['firstname']}:{member['age']}:{member['mobile']}:{member['postcode']}"
                        for member in patient.get_family()
                    ])
                    writer.writerow({
                        'firstname': patient.get_firstname(),
                        'lastname': patient.get_surname(),
                        'age': patient.get_age(),
                        'mobile': patient.get_mobile(),
                        'postcode': patient.get_postcode(),
                        'doctor': patient.get_doctor().full_name() if patient.get_doctor() else "",
                        'symptoms': ",".join(patient.get_symptoms()),
                        'family_members': family_members
                    })
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save patients: {str(e)}")

    def load_patients_from_file(self):
        try:
            with open(self.data_file, 'r') as file:
                reader = csv.DictReader(file)
                self.patients = []

                for row in reader:
                    patient = Patient(
                        firstname=row['firstname'],
                        lastname=row['lastname'],
                        age=row['age'],
                        mobile=row['mobile'],
                        postcode=row['postcode'],
                    )

                    doctor_name = row['doctor']
                    if doctor_name:
                        doctor = next((doc for doc in self.doctors if doc.full_name() == doctor_name), None)
                        if doctor:
                            patient.link(doctor)
                            doctor.add_patient(patient)

                    symptoms = row['symptoms'].split(",") if row['symptoms'] else []
                    patient.add_symptom(symptoms)

                    if row['family_members']:
                        family_members = row['family_members'].split(";")
                        for member in family_members:
                            fname, age, mobile, postcode = member.split(":")
                            patient.link_family_member(fname, age, mobile, postcode)

                    self.patients.append(patient)
        except FileNotFoundError:
            messagebox.showinfo("Info", "No previous patient data found. Starting fresh.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patients: {str(e)}")
