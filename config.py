"""config.py - Configuration file for the application
   Author: Kim Khang Hoang
   Date created: 09/08/2023"""

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

APP_NAME = 'Employee Management System - Contacts'

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SYSTEM_SENDER_EMAIL = os.getenv('SYSTEM_SENDER_EMAIL')
SYSTEM_SENDER_PASSWORD = os.getenv('SYSTEM_SENDER_PASSWORD')
SYSTEM_RECEIVER_EMAIL = os.getenv('SYSTEM_RECEIVER_EMAIL')
