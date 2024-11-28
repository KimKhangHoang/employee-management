"""login_page.py - The login page of the application inherited from tk.Frame
   Author: Kim Khang Hoang
   Date created: 26/07/2023"""

import bcrypt
import tkinter as tk
from tkinter import messagebox
from connect_data import cursor
from menu import Menu
from destroy_current_page import DestroyCurrentPage
from employee_page import EmployeePage

class Login(tk.Frame):
    # Constructor
    def __init__(self, root):
        # Call the constructor of the tk.Frame parent class
        super().__init__(root)

        # Add the frame to the root window
        self.grid(row=0, column=0)

        # Name the window's title
        self.master.title('Login')

        # Set the window's size
        root.state('normal')

        # Username entry
        self.label_username = tk.Label(self, text="Username")
        self.label_username.grid(row=0, column=0)
        self.entry_username = tk.Entry(self)
        self.entry_username.grid(row=0, column=1)

        # Force focus on the username entry
        self.entry_username.focus_force()

        # Password entry
        self.label_password = tk.Label(self, text="Password")
        self.label_password.grid(row=1, column=0)
        self.entry_password = tk.Entry(self, show='*')
        self.entry_password.grid(row=1, column=1)

        # Login using button
        self.button_login = tk.Button(self, text='Login', command=self.login)
        self.button_login.grid(row=2, column=0, columnspan=2, sticky='ew')

        # Login using Enter key
        self.entry_password.bind("<Return>", lambda event: self.login())

        # Get the window's width and height
        window_width = self.master.winfo_screenwidth()
        window_height = self.master.winfo_screenheight()

        # Get the form's width and height
        form_width = self.master.winfo_reqwidth()
        form_height = self.master.winfo_reqheight()

        # Calculate the x and y positions of the form
        position_x = int((window_width - form_width)/2)
        position_y = int((window_height - form_height)/2)

        # Set the form's position
        self.master.geometry(f'+{position_x}+{position_y}')

    # Process the login action
    def login(self):
        # Get the entered username and password
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if the username and password are correct
        if not self.authenticate(username, password):
            messagebox.showerror('Login failed', 'Invalid username or password.')
            return

        # Destroy the current page and direct to the employee page if the login is successful
        DestroyCurrentPage(self.master)
        EmployeePage(self.master)

        # Set the logged username in the master window
        self.master.logged_username = username

        # Add the menu into the master window
        Menu(self.master)

    # Authenticate the user login details
    def authenticate(self, username, password):
        # Get the user info from the database
        user = self.get_user(username)

        # Check if the user exists and the password is correct
        if user is None:
            return False
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return True
        return False

    # Get the user info from the database
    def get_user(self, username):
        # Execute the SQL query
        cursor.execute(f"SELECT * FROM users WHERE username='{username}'")

        # Retrieve all users from the database
        rows = cursor.fetchall()

        # Return the first user if exists
        if len(rows) > 0:
            return rows[0]
        return None
