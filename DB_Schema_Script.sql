-- Create 'employees' table
CREATE TABLE dbo.employees (
    employee_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(50),
    birthday DATE,
    gender NVARCHAR(20),
    salary BIGINT
);
GO

-- Create 'users' table
CREATE TABLE dbo.users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50),
    password NVARCHAR(200),
    name NVARCHAR(50)
);
GO