"""contact_page.py - The contact page of the application inherited from tk.Frame
   Author: Kim Khang Hoang
   Date created: 09/08/2023"""

import tkinter as tk
import tkinter.font as tk_font
from tkinter import messagebox

import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ContactPage(tk.Frame):
    # Constructor
    def __init__(self, root):
        super().__init__(root)

        # Add the frame to the root window
        self.grid(row=0, column=0, sticky='we', padx=20)

        # Show the contact form to send an email
        self.showForm()

        # Set the window's size to full screen
        self.master.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # The form to send an email
    def showForm(self):
        # Set the font format
        font_format = tk_font.Font(size=16, weight='bold', family='Helvetica')  # Fix: Use tkfont
        self.label_title = tk.Label(self, text='Contact details', font=font_format)
        self.label_title.grid(row=0, column=0, pady=(20, 20))

        # Name
        self.label_name = tk.Label(self, text='Name')
        self.label_name.grid(row=1, column=0, pady=(5, 5), sticky='w')
        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=2, column=0, pady=(5, 5), sticky='w')

        # Email
        self.label_email = tk.Label(self, text='Email')
        self.label_email.grid(row=3, column=0, pady=(5, 5), sticky='w')
        self.entry_email = tk.Entry(self)
        self.entry_email.grid(row=4, column=0, pady=(5, 5), sticky='w')

        # Mobile number
        self.label_mobile = tk.Label(self, text='Mobile number')
        self.label_mobile.grid(row=5, column=0, pady=(5, 5), sticky='w')
        self.entry_mobile = tk.Entry(self)
        self.entry_mobile.grid(row=6, column=0, pady=(5, 5), sticky='w')

        # Message
        self.label_message = tk.Label(self, text='Message')
        self.label_message.grid(row=7, column=0, pady=(5, 5), sticky='w')
        self.text_message = tk.Text(self, height=10, width=60)
        self.text_message.grid(row=8, column=0, pady=(5, 5), sticky='w')

        # Send Button
        self.btn_submit = tk.Button(self, text="Send", padx=20, command=self.sendEmail)
        self.btn_submit.grid(row=9, column=0, pady=(5,5), sticky='w')

    # Send an email
    def sendEmail(self):
        # Email account information to send the email
        try:
            system_sender_email = config.SYSTEM_SENDER_EMAIL
            system_sender_password = config.SYSTEM_SENDER_PASSWORD
            system_receiver_email = config.SYSTEM_RECEIVER_EMAIL
            subject = config.APP_NAME

        except AttributeError as e:
            messagebox.showinfo("Mail sender", f"Configuration error: {e}")
            return

        # Get and format the message
        message = self.text_message.get("1.0", "end-1c").replace('\n', '<br>')
        content = f"""
            Hello admin, <br>
            Below are the user's contact details: <br>
            Name: {self.entry_name.get()}<br>
            Email: {self.entry_email.get()}<br>
            Mobile number: {self.entry_mobile.get()}<br>
            Message: <br>
            {message}<br>
            ------------------------<br>
            This email was sent from the Employee Management system.
        """

        # Create and send the email
        msg = MIMEMultipart()
        msg['From'] = system_sender_email
        msg['To'] = system_receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'html'))

        try:
            with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
                server.starttls()
                server.login(system_sender_email, system_sender_password)
                server.sendmail(system_sender_email, system_receiver_email, msg.as_string())

            messagebox.showinfo('Mail sender', 'The email has been sent successfully')

            # Clear the form after a successful email is sent
            self.entry_name.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_mobile.delete(0, tk.END)
            self.text_message.delete("1.0", tk.END)

        except Exception as e:
            messagebox.showinfo('Mail sender', f'An error has occurred: {e}')
