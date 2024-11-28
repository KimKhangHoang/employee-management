"""create_employee_page.py - The page for creating a new employee
   Author: Kim Khang Hoang
   Date created: 23/08/2023"""

import tkinter as tk
import tkcalendar
from tkinter import ttk
from tkinter import messagebox

class CreateEmployeePage(tk.Frame):
    # Constructor
    def __init__(self, root):
        # Call the constructor of the tk.Frame parent class
        super().__init__(root)

        # Add the frame to the root window
        self.grid(row=0, column=0, sticky='we', padx=20)

        # Show the form to create a new employee
        self.showForm()

        # Set the window's size to full screen
        self.master.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # The create employee form
    def showForm(self):
        # Set the font format
        font_format = tk.font.Font(size=16, weight='bold', family='Helvetica')
        self.label_title = tk.Label(self, text='Add employee', font=font_format)
        self.label_title.grid(row=0, column=0, pady=(20, 20))

        # Name
        self.label_name = tk.Label(self, text='Name')
        self.label_name.grid(row=1, column=0, pady=(5, 5), sticky='w')
        self.entry_name = tk.Entry(self, width=40)
        self.entry_name.grid(row=2, column=0, pady=(5, 5), sticky='w')

        # Birthday
        self.label_birthday = tk.Label(self, text='Birthday')
        self.label_birthday.grid(row=3, column=0, pady=(5, 5), sticky='w')
        self.calendar_birthday = tkcalendar.Calendar(self, date_pattern='yyyy-mm-dd')
        self.calendar_birthday.grid(row=4, column=0, pady=(5, 5), sticky='w')

        # Gender
        self.label_gender = tk.Label(self, text='Gender')
        self.label_gender.grid(row=5, column=0, pady=(5, 5), sticky='w')
        options = ["male", "female", "prefer not to say"]
        self.entry_gender = ttk.Combobox(self, values=options, state='readonly')
        self.entry_gender.grid(row=6, column=0, pady=(5, 5), sticky='w')

        # Salary
        self.label_salary = tk.Label(self, text='Salary')
        self.label_salary.grid(row=7, column=0, pady=(5, 5), sticky='w')
        self.entry_salary = tk.Entry(self)
        self.entry_salary.grid(row=8, column=0, pady=(5, 5), sticky='w')

        # Save Button
        self.btn_submit = tk.Button(self, text="Save", padx=20, command=self.save)
        self.btn_submit.grid(row=9, column=0, pady=(5,5), sticky='w')

    # Save the new employee to the database
    def save(self):
        try:
            # Save to the database
            from connect_data import cursor
            from connect_data import conn
            name = self.entry_name.get()
            birthday = self.calendar_birthday.get_date()
            gender = self.entry_gender.get()
            salary = self.entry_salary.get()

            # Check if any entry is empty
            entry_error = []
            if not name:
                entry_error.append('Name')
            if not birthday:
                entry_error.append('Birthday')
            if not gender:
                entry_error.append('Gender')
            if not salary:
                entry_error.append('Salary')
            if len(entry_error) > 0:
                messagebox.showerror('Error', 'Please fill in all information')
                return

            # Check if the salary is a number
            if not salary.isnumeric():
                messagebox.showerror('Error', 'Please enter a number for salary')
                self.entry_salary.focus_force()
                return

            # Insert the data into the database
            sql = f"INSERT INTO employees (name, birthday, gender, salary) VALUES(N'{name}', '{birthday}', N'{gender}', {salary})"
            cursor.execute(sql)
            cursor.commit()

            messagebox.showinfo('Database', 'Employee has been added successfully')

            # Redirect to the employee page
            from employee_page import  EmployeePage
            from destroy_current_page import DestroyCurrentPage
            DestroyCurrentPage(self.master)
            EmployeePage(self.master)

        except Exception as e:
            messagebox.showerror('Database', f'An error has occurred: {e}')
