"""employee_page.py - The employee page of the application inherited from tk.Frame
   Author: Kim Khang Hoang
   Date created: 02/08/2023"""

import tkinter as tk
from tkinter import ttk
from format_money import FormatMoney
from tkinter import messagebox
from destroy_current_page import DestroyCurrentPage
from edit_employee_page import EditEmployeePage
from create_employee_page import CreateEmployeePage

class EmployeePage(tk.Frame):
    # Constructor
    def __init__(self, root):
        # Call the constructor of the tk.Frame parent class
        super().__init__(root)

        # Add the frame to the root window
        self.grid(row=0, column=0, sticky='we')

        # Name the window's title
        root.title('Employee list')

        # Set the window's size to full screen
        root.state('zoom')
        self.master.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Show a list of employees
        self.ShowEmployee()

    # Get the employees from the database and display them in a table
    def ShowEmployee(self):
        # Set the font format
        font_format = tk.font.Font(size=16, weight='bold', family='Helvetica')
        self.label_title = tk.Label(self, text='Employee list', font=font_format)
        self.label_title.grid(row=0, column=0, pady=(20, 20))

        # Create the button to add a new employee
        self.btn_create = tk.Button(self, text='Add new employee', command=self.open_create_employee_page)
        self.btn_create.grid(row=1, column=0, pady=(20, 20))

        # Create the table with columns to display the employees
        self.tree = ttk.Treeview(self, show='headings')
        self.tree['column'] = ('employee_id', 'name', 'birthday', 'gender', "salary")

        # Set the column headings
        self.tree.heading('employee_id', text='Employee ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('birthday', text='Birthday')
        self.tree.heading('gender', text='Gender')
        self.tree.heading('salary', text='Salary')

        # Set the column alignment to center
        self.tree.column('employee_id', anchor='center')
        self.tree.column('name', anchor='center')
        self.tree.column('birthday', anchor='center')
        self.tree.column('gender', anchor='center')
        self.tree.column('salary', anchor='center')

        # Add the table to the frame
        self.tree.grid(row=2, column=0, sticky='ew', pady=(20,0), padx=(20,20))

        # Execute the SQL query to get the employees from the database
        from connect_data import cursor
        cursor.execute('SELECT * FROM employees')
        for row in cursor:
            # Format the money to display in the table
            list_row = list(row)
            money = list_row[4]
            f_money = FormatMoney(money)
            list_row[4] = f_money

            # Change the row to a tuple and insert it into the table
            self.tree.insert("", tk.END, values=tuple(list_row))

        # Create the context menu
        self.context_menu = tk.Menu(self.master, tearoff=False)
        self.context_menu.add_command(label='Edit', command=self.edit_item)
        self.context_menu.add_command(label='Delete', command=self.delete_item)
        self.tree.bind("<Button-3>", self.show_context_menu)

    # Show the context menu where the right mouse button is clicked
    def show_context_menu(self, event):
        select_item = self.tree.selection()
        if select_item:
            self.context_menu.post(event.x_root, event.y_root)

    # Edit the selected employee
    def edit_item(self):
        # Get the selected item id from the table
        selected_item = self.tree.selection()
        row_id = selected_item[0]

        # Get the values of the selected item
        row_info = self.tree.item(row_id)
        employee = row_info['values']

        # Get the employee id
        employee_id = employee[0]

        # Redirect to the EditEmployeePage with the employee id
        DestroyCurrentPage(self.master)
        EditEmployeePage(self.master, employee_id)

    # Delete the selected employee
    def delete_item(self):
        try:
            # Get the selected items from the table
            selected_items = self.tree.selection()
            employee_ids = []

            # Get the employee id of the selected items and add them to the list
            for row_id in selected_items:
                row_info = self.tree.item(row_id)
                employee = row_info['values']
                employee_id = employee[0]
                employee_ids.append(employee_id)

            # Ask for confirmation before deleting the employee
            answer = messagebox.askyesno('Confirmation', 'Are you sure you want to delete the selected employee(s)?')
            if not answer:
                return

            # Convert the list of employee ids to a tuple
            employee_ids = tuple(employee_ids)

            # Create the SQL query to delete the selected employee(s)
            from connect_data import cursor
            if len(employee_ids) > 1:
                sql = f'DELETE FROM employees WHERE [employee_id] IN {employee_ids}'
            else:
                sql = f'DELETE FROM employees WHERE [employee_id] = {employee_ids[0]}'

            # Execute the SQL query
            cursor.execute(sql)
            cursor.commit()
            messagebox.showinfo('Database', 'The employee(s) has been deleted successfully')

            # Redirect to the EmployeePage
            DestroyCurrentPage(self.master)
            EmployeePage(self.master)

        except Exception as e:
            messagebox.showerror('Database', f'An error occurred: {e}')

    # Redirect to the CreateEmployeePage
    def open_create_employee_page(self):
        DestroyCurrentPage(self.master)
        CreateEmployeePage(self.master)
