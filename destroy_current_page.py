"""destroy_current_page.py - A module that contains a function to destroy the current page
   Author: Kim Khang Hoang
   Date created: 27/07/2023"""

import tkinter as tk
def DestroyCurrentPage(root):
    # Get all the children of the root window
    children = root.winfo_children()

    # Get all the frames from the children
    frames = [child for child in children if isinstance(child, tk.Frame)]

    # Destroy all the frames
    for frame in frames:
        frame.destroy()
