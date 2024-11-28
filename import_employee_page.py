"""import_employee_page.py - The import employee page of the application inherited from tk.Frame
   Author: Kim Khang Hoang
   Date created: 17/08/2023"""

import os.path
import tkinter as tk
import pandas as pd
from tkinter import messagebox
from tkinter import filedialog

class ImportEmployeePage(tk.Frame):
    # Constructor
    def __init__(self, root):
        # Call the constructor of the tk.Frame parent class
        super().__init__(root)

        # Center the frame horizontally
        root.grid_columnconfigure(0, weight=1)

        # Add the frame to the root window
        self.grid(row=0, column=0, padx=20, pady=20)

        # Show the form to import the employee data
        self.showForm()

    # The import form
    def showForm(self):
        # Set the font format
        font_format = tk.font.Font(size=16, weight='bold', family='Helvetica')
        self.label_title = tk.Label(self, text='Import employee', font=font_format)
        self.label_title.grid(row=0, column=0, pady=(20, 20))

        # Browse file
        self.entry_path = tk.Entry(self, width=80)
        self.button_browse = tk.Button(self, text='Browse', command=self.open_file_dialog)

        # Path to the file
        self.entry_path.grid(row=1, column=0, pady=(5,5), sticky='w')
        self.button_browse.grid(row=1, column=1, pady=(5,5), sticky='w')

        # Import Button
        self.btn_submit = tk.Button(self, text="Import", padx=20, command=self.import_excel)
        self.btn_submit.grid(row=2, column=0, pady=(5,5), sticky='w')

    # Open file dialog to select the file
    def open_file_dialog(self):
        # Get the file path
        file_path = filedialog.askopenfilename()

        # Display the path to the entry
        self.entry_path.delete(0, tk.END)
        self.entry_path.insert(0, file_path)

    # Import Excel file
    def import_excel(self):
        try:
            # Save to the database
            from connect_data import cursor
            file_path = self.entry_path.get()

            # Check if the file is selected
            if not file_path:
                messagebox.showerror('Error', 'Please select a file')
                return
            # Check if the file exists
            if not os.path.isfile(file_path):
                messagebox.showerror('Error', 'This file does not exist')
                return
            # Check if the file is an Excel file
            if not file_path.endswith('.xlsx'):
                messagebox.showerror('Error', 'This file is not an Excel file')
                return

            # Read and validate the Excel file
            df = pd.read_excel(file_path)
            for index, row in df.iterrows():
                if not 'Name' in row:
                    messagebox.showerror('Error', 'The Excel file must have a column named \'Name\'')
                    return
                if not 'Birthday' in row:
                    messagebox.showerror('Error', 'The Excel file must have a column named \'Birthday\'')
                    return
                if not 'Gender' in row:
                    messagebox.showerror('Error', 'The Excel file must have a column named \'Gender\'')
                    return
                if not 'Salary' in row:
                    messagebox.showerror('Error', 'The Excel file must have a column named \'Salary\'')
                    return

                # Get the data from the Excel file
                name = row['Name']
                birthday = row['Birthday']
                gender = row['Gender']
                salary = row['Salary']

                # Insert the data into the database
                sql = f"INSERT INTO employees (name, birthday, gender, salary) VALUES('{name}', N'{birthday}', N'{gender}', {salary})"
                cursor.execute(sql)
                cursor.commit()

            messagebox.showinfo('Database', 'Employee data have been imported successfully')

            # Redirect to the employee page
            from employee_page import  EmployeePage
            from destroy_current_page import DestroyCurrentPage
            DestroyCurrentPage(self.master)
            EmployeePage(self.master)

        except Exception as e:
            messagebox.showerror('Database', f'An error has occurred: {e}')
