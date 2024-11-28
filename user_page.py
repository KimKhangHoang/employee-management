"""user_page.py - The user page of the application inherited from tk.Frame
   Author: Kim Khang Hoang
   Date created: 16/08/2023"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from destroy_current_page import DestroyCurrentPage
from edit_user_page import EditUserPage
from create_user_page import CreateUserPage

class UserPage(tk.Frame):
    # Constructor
    def __init__(self, root):
        # Call the constructor of the tk.Frame parent class
        super().__init__(root)

        # Name the window's title
        root.title('User list')

        # Add the frame to the root window
        self.grid(row=0, column=0, sticky='we')

        # Set the window's size to full screen
        root.state('zoom')
        self.master.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Show a list of users
        self.ShowUser()

    # Get the users from the database and display them in a table
    def ShowUser(self):
        # Set the font format
        font_format = tk.font.Font(size=16, weight='bold', family='Helvetica')
        self.label_title = tk.Label(self, text='User list', font=font_format)
        self.label_title.grid(row=0, column=0, pady=(20, 20))

        # Create the button to add a new user
        self.btn_create = tk.Button(self, text='Add user', command=self.open_create_user_page)
        self.btn_create.grid(row=1, column=0, pady=(20, 20))

        # Create the table with columns to display the users
        self.tree = ttk.Treeview(self, show='headings')
        self.tree['column'] = ('user_id', 'username', 'name')

        # Set the column headings
        self.tree.heading('user_id', text='User ID')
        self.tree.heading('username', text='Username')
        self.tree.heading('name', text='Name')

        # Set the column alignment to center
        self.tree.column('user_id', anchor='center')
        self.tree.column('username', anchor='center')
        self.tree.column('name', anchor='center')

        # Add the table to the frame
        self.tree.grid(row=2, column=0, sticky='ew', pady=(20,0), padx=(20,20))

        # Execute the SQL query to get the users from the database
        from connect_data import cursor
        cursor.execute('SELECT * FROM users')
        for row in cursor:
            # Format the name to display in the table
            list_row = list(row)
            del list_row[2]

            # Change the row to a tuple and insert it into the table
            self.tree.insert("", tk.END, values=tuple(list_row))

        # Create the context menu
        self.context_menu = tk.Menu(self.master, tearoff=False)
        self.context_menu.add_command(label='Edit', command=self.edit_item)
        self.context_menu.add_command(label='Delete', command=self.delete_item)
        self.tree.bind("<Button-3>", self.show_context_menu)

    # Show the context menu where right-clicking on the table
    def show_context_menu(self, event):
        select_item = self.tree.selection()
        if select_item:
            self.context_menu.post(event.x_root, event.y_root)

    # Edit the selected user
    def edit_item(self):
        # Get the selected item id from the table
        selected_item = self.tree.selection()
        row_id = selected_item[0]

        # Get the values of the selected item
        row_info = self.tree.item(row_id)
        user = row_info['values']

        # Get the user id
        user_id = user[0]

        # Redirect to the EditUserPage with the user id
        DestroyCurrentPage(self.master)
        EditUserPage(self.master, user_id)

    # Delete the selected user
    def delete_item(self):
        try:
            # Get the selected items from the table
            selected_items = self.tree.selection()
            user_ids = []

            # Get the user id of the selected items and add them to the list
            for row_id in selected_items:
                row_info = self.tree.item(row_id)
                user = row_info['values']
                user_id = user[0]
                user_ids.append(user_id)

            # Ask for confirmation before deleting the employee
            answer = messagebox.askyesno('Confirmation', 'Are you sure you want to delete the selected user(s)?')
            if not answer:
                return

            # Convert the list of user ids to a tuple
            user_ids = tuple(user_ids)

            # Create the SQL query to delete the selected user(s)
            from connect_data import cursor
            if len(user_ids)>1:
                sql = f'DELETE FROM users WHERE [user_id] IN {user_ids}'
            else:
                sql = f'DELETE FROM users WHERE [user_id] = {user_ids[0]}'

            # Execute the SQL query
            cursor.execute(sql)
            cursor.commit()
            messagebox.showinfo('Database', 'The user(s) has been deleted successfully')

            # Redirect to the UserPage
            DestroyCurrentPage(self.master)
            UserPage(self.master)

        except Exception as e:
            messagebox.showerror('Database', f'An error occurred: {e}')

    # Redirect to the CreateUserPage
    def open_create_user_page(self):
        DestroyCurrentPage(self.master)
        CreateUserPage(self.master)
