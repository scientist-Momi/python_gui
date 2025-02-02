# Program and theme requires TK version 9.0.1. If there is any issue getting this version, 
# you can manually change the versions to your preffered versions in these two files.
# ./theme/dark.tcl  line 5
# ./theme/light.tcl  line 5


# All requirements are in the requirements.txt
# To install them all, Run 
# pip install -r requirements.txt


# Some hidden functionality
# To link patient to their family member - Add new patient with an existing surname in the patient file and follow prompt.
# To reveal Patient's family members - click on a specific patient on the table
# To reveal Doctor's patients - click on a specific doctor on the table
# To change to dark mode and back - click on button on the bottom right 




import tkinter as tk
from Admin import Admin

def main():
    root = tk.Tk()

    # I USED THE AZURE THEME WHICH ACCEPTS TKINTER 9.0.1
    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "light")
    except Exception:
        print("Theme file not found. Using default theme.")
    app = Admin(root, 'admin', '123', 'B1 1AB')
    app.pack(fill="both", expand=True)
    root.update()
    width = root.winfo_width()
    height = root.winfo_height()
    x_cordinate = (root.winfo_screenwidth() // 2) - (width // 2)
    y_cordinate = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x_cordinate}+{y_cordinate - 20}")
    root.minsize(378, 275)
    root.mainloop()

if __name__ == "__main__":
    main()
