"""menu.py - The menu of the application inherited from tk.Menu
   Author: Kim Khang Hoang
   Date created: 27/07/2023"""

import tkinter as tk
from tkinter import messagebox
from destroy_current_page import DestroyCurrentPage

class Menu(tk.Menu):
    # Constructor
    def __init__(self, root):
        # Call the constructor of the tk.Menu parent class
        super().__init__(root)

        # Create the menu level 1
        root.config(menu=self)

        # Create the menu level 2 for the menu level 1
        sub_menu = tk.Menu(self, tearoff=False)

        # Create the menu level 3 for the menu level 2
        child_sub_menu = tk.Menu(sub_menu, tearoff=False)

        # Add items to the menu level 1
        self.add_cascade(label='File', menu=sub_menu)
        self.add_command(label='About', command=lambda: messagebox.showinfo("About", "This is an Employee Management System"))
        self.add_command(label='Help', command=lambda: messagebox.showinfo("Help", "Please contact the system administrator for help"))
        self.add_command(label='Contact', command=self.open_contact_page)

        # Add items to the menu level 2 (File)
        sub_menu.add_cascade(label='New', menu=child_sub_menu)
        child_sub_menu.add_command(label='Office', command=lambda: messagebox.showinfo("Info","New Office functionality not implemented yet"))
        child_sub_menu.add_command(label='Branch', command=lambda: messagebox.showinfo("Info","New Branch functionality not implemented yet"))
        sub_menu.add_separator()
        sub_menu.add_command(label='Open', command=lambda: messagebox.showinfo("Info", "Open functionality not implemented yet"))
        sub_menu.add_separator()
        sub_menu.add_command(label='Employee List', command=self.open_employee_page)
        sub_menu.add_separator()
        sub_menu.add_command(label='User List', command=self.open_user_page)
        sub_menu.add_separator()
        sub_menu.add_command(label='Import Employee', command=self.import_employee_page)

        # Add logout and exit button to the menu level 2 (File)
        sub_menu.add_separator()
        sub_menu.add_command(label=f'Logout ({self.master.logged_username})', command=self.logout)
        sub_menu.add_separator()
        sub_menu.add_command(label='Exit', command=root.quit)

    # Redirect to the Login page
    def logout(self):
        from login_page import Login
        DestroyCurrentPage(self.master)
        Login(self.master)
        self.master.logged_username = ""
        self.destroy()

    # Redirect to the Contact page
    def open_contact_page(self):
        from contact_page import ContactPage
        DestroyCurrentPage(self.master)
        ContactPage(self.master)

    # Redirect to the Employee page
    def open_employee_page(self):
        from employee_page import EmployeePage
        DestroyCurrentPage(self.master)
        EmployeePage(self.master)

    # Redirect to the User page
    def open_user_page(self):
        from user_page import UserPage
        DestroyCurrentPage(self.master)
        UserPage(self.master)

    # Redirect to the Import Employee page
    def import_employee_page(self):
        from import_employee_page import ImportEmployeePage
        DestroyCurrentPage(self.master)
        ImportEmployeePage(self.master)
