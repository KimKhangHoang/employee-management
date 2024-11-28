"""edit_employee_page.py - The page for editing an existing employee
   Author: Kim Khang Hoang
   Date created: 30/08/2023"""

import tkinter as tk
import tkcalendar
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class EditEmployeePage(tk.Frame):
    # Constructor
    def __init__(self, root, employee_id):
        # Call the constructor of the tk.Frame parent class
        super().__init__(root)

        # Store the employee ID
        self.employee_id = employee_id

        # Add the frame to the root window
        self.grid(row=0, column=0, sticky='we', padx=20)

        # Show the form to edit an existing employee
        self.showForm()

        # Set the window's size to full screen
        self.master.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # The edit employee form
    def showForm(self):
        # Set the font format
        font_format = tk.font.Font(size=16, weight='bold', family='Helvetica')
        self.label_title = tk.Label(self, text='Edit employee', font=font_format)
        self.label_title.grid(row=0, column=0, pady=(20, 20))

        # Get the employee's information from the database
        from connect_data import cursor
        cursor.execute(f'SELECT * FROM employees WHERE employee_id={self.employee_id}')
        employee = cursor.fetchone()
        name = employee[1]
        birthday = employee[2]
        gender = employee[3]
        salary = employee[4]

        # Name
        self.label_name = tk.Label(self, text='Name')
        self.label_name.grid(row=1, column=0, pady=(5, 5), sticky='w')
        self.entry_name = tk.Entry(self, textvariable=tk.StringVar(value=name))
        self.entry_name.grid(row=2, column=0, pady=(5, 5), sticky='w')

        # Birthday
        date_time = datetime.strptime(birthday, "%Y-%m-%d")
        self.label_birthday = tk.Label(self, text='Birthday')
        self.label_birthday.grid(row=3, column=0, pady=(5, 5), sticky='w')
        self.calendar_birthday = tkcalendar.Calendar(self, date_pattern='yyyy-mm-dd', year=date_time.year, day=date_time.day, month=date_time.month)
        self.calendar_birthday.grid(row=4, column=0, pady=(5, 5), sticky='w')

        # Gender (set default value if left empty)
        self.label_gender = tk.Label(self, text='Gender')
        self.label_gender.grid(row=5, column=0, pady=(5, 5), sticky='w')
        options = ["male", "female", "prefer not to say"]
        self.entry_gender = ttk.Combobox(self, values=options, state='readonly')
        self.entry_gender.set(gender)
        self.entry_gender.grid(row=6, column=0, pady=(5, 5), sticky='w')

        # Salary
        self.label_salary = tk.Label(self, text='Salary')
        self.label_salary.grid(row=7, column=0, pady=(5, 5), sticky='w')
        self.entry_salary = tk.Entry(self, textvariable=tk.StringVar(value=salary))
        self.entry_salary.grid(row=8, column=0, pady=(5, 5), sticky='w')

        # Save Button
        self.btn_submit = tk.Button(self, text="Save", padx=20, command=self.update)
        self.btn_submit.grid(row=9, column=0, pady=(5,5), sticky='w')

    # Save the new employee to the database
    def update(self):
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

            # Update the employee in the database
            sql = (f"UPDATE employees SET [name]=N'{name}', [birthday]='{birthday}', [gender]=N'{gender}', salary='{salary}'"
                   f"WHERE employee_id={self.employee_id}")
            cursor.execute(sql)
            cursor.commit()

            messagebox.showinfo('Database', 'Employee has been updated successfully')

            # Redirect to the employee page
            from employee_page import EmployeePage
            from destroy_current_page import DestroyCurrentPage
            DestroyCurrentPage(self.master)
            EmployeePage(self.master)

        except Exception as e:
            messagebox.showerror('Database', f'An error has occurred: {e}')
