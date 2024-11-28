"""main.py - The main file that starts the application
   Author: Kim Khang Hoang
   Date created: 26/07/2023"""

import tkinter as tk
import login_page

# Create the main window
window = tk.Tk()

# Initialize the login page by passing the window object
login_page.Login(window)

# Start the Tkinter event loop
window.mainloop()
