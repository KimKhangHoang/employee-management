# Employee Management System

## Overview

The **Employee Management System** is a Python-based application for managing employees and users, built with SQL Server as the database. It includes features for creating, editing, and importing employee and user data, with an intuitive menu interface and support for user authentication.

---

## Features

- **Login** with user authentication.
- **Employee Management**: view employee list or add, edit, and import employee data.
- **User Management**: view user list or create and edit users.
- **Menu Navigation**: accessible options for managing employees and users. Additional options for contacting the system administrator via email and logging out.
- **Utility Functions**: money formatting and database connection management.

---

## Setup

### Prerequisites

- Python installed.
- SQL Server with a valid database configured based on the provided template `DB_Schema_Script.sql`.
- Required Python packages installed (e.g., `pyodbc`, `openpyxl`, `python_dotenv`, `bcrypt`, etc.).

### Environment Configuration

Create a `.env` file in the project directory with the format provided in the `.env.example` file for email credentials and database connection details.

### Installation

1. Clone the repository.
2. Set up the environment configuration as described above.
3. Install the required Python packages in the project.

---

## Running The Program

Run the `main.py` file to start the application. Explore the menu options to manage employees and users, and other features.

---

## Future Enhancements

- Integration of "New Office", "New Branch", and "Open" functionalities.
- Improved authentication and authorisation features.
- Detail testing and debugging for robustness and consistency.
