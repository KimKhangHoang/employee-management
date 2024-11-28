"""create_user_page.py - The page for creating a new user
   Author: Kim Khang Hoang
   Date created: 31/08/2023"""

import re
import bcrypt
import tkinter as tk
from tkinter import messagebox

class CreateUserPage(tk.Frame):
    # Constructor
    def __init__(self, root):
        # Call the constructor of the tk.Frame parent class
        super().__init__(root)

        # Add the frame to the root window
        self.grid(row=0, column=0, sticky='we', padx=20)

        # Show the form to create a new user
        self.showForm()

        # Set the window's size to full screen
        self.master.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # The create user form
    def showForm(self):
        # Set the font format
        font_format = tk.font.Font(size=16, weight='bold', family='Helvetica')
        self.label_title = tk.Label(self, text='Add user', font=font_format)
        self.label_title.grid(row=0, column=0, pady=(20, 20))

        # Name
        self.label_name = tk.Label(self, text='Name')
        self.label_name.grid(row=1, column=0, pady=(5, 5), sticky='w')
        self.entry_name = tk.Entry(self, width=40)
        self.entry_name.grid(row=2, column=0, pady=(5, 5), sticky='w')

        # Username
        self.label_username = tk.Label(self, text='Username')
        self.label_username.grid(row=3, column=0, pady=(5, 5), sticky='w')
        self.entry_username = tk.Entry(self, width=40)
        self.entry_username.grid(row=4, column=0, pady=(5, 5), sticky='w')

        # Password
        self.label_password = tk.Label(self, text='Password')
        self.label_password.grid(row=7, column=0, pady=(5, 5), sticky='w')
        self.entry_password = tk.Entry(self, width=40, show='*')
        self.entry_password.grid(row=8, column=0, pady=(5, 5), sticky='w')

        # Password confirmation
        self.label_password_confirmation = tk.Label(self, text='Password confirmation')
        self.label_password_confirmation.grid(row=9, column=0, pady=(5, 5), sticky='w')
        self.entry_password_confirmation = tk.Entry(self, width=40, show='*')
        self.entry_password_confirmation.grid(row=10, column=0, pady=(5, 5), sticky='w')

        # Save Button
        self.btn_submit = tk.Button(self, text="Save", padx=20, command=self.save)
        self.btn_submit.grid(row=11, column=0, pady=(5,5), sticky='w')

    # Save the new user to the database
    def save(self):
        try:
            # Save to the database
            from connect_data import cursor
            from connect_data import conn
            name = self.entry_name.get()
            username = self.entry_username.get()
            password = self.entry_password.get()
            password_confirmation = self.entry_password_confirmation.get()

            # Check if the entries are empty (condition 1)
            entry_error = []
            if not name:
                entry_error.append('Name')
            if not username:
                entry_error.append('Username')
            if not password:
                entry_error.append('Password')
            if not password_confirmation:
                entry_error.append('Password confirmation')
            if len(entry_error) > 0:
                messagebox.showerror('Error', 'Please fill in all information')
                return

            # Check if the username already exists (condition 2)
            sql = f"SELECT * FROM users WHERE [username]='{username}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                messagebox.showerror('Error', f'The username {username} has already existed. Please choose another username')
                return

            # Check if the password and password confirmation are the same (condition 3)
            if password != password_confirmation:
                messagebox.showerror('Error', f'The passwords do not match')
                return

            # Check if the password meets the requirements (condition 4)
            regex = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
            if not re.match(regex, password):
                messagebox.showerror('Error', f'The password must contain at least 8 characters, including uppercase, lowercase, number, and special character')
                return

            # Hash the password using bcrypt
            byte_password = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(byte_password, salt)
            readable_hashed_password = hashed_password.decode('utf-8')

            # Insert the new user to the database
            sql = f"INSERT INTO users (username, password, name) VALUES(N'{username}', '{readable_hashed_password}', N'{name}')"
            cursor.execute(sql)
            cursor.commit()

            messagebox.showinfo('Database', 'User has been created successfully')

            # Redirect to the user page
            from user_page import  UserPage
            from destroy_current_page import DestroyCurrentPage
            DestroyCurrentPage(self.master)
            UserPage(self.master)

        except Exception as e:
            messagebox.showerror('Database', f'An error has occurred: {e}')
