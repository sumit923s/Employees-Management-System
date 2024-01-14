import re
import mysql.connector

class EmployeeManagementSystem:
    def __init__(self):
        # Making Connection to MySQL
        self.connection = mysql.connector.connect(
            host="localhost", user="root", password="root", database="Employee_Management_System")

        # Regular expression patterns
        self.email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = re.compile("(0|91)?[7-9][0-9]{9}")

    def check_employee_name(self, employee_name):
        sql = 'SELECT * FROM employee WHERE Name=%s'
        cursor = self.connection.cursor(buffered=True)
        data = (employee_name,)
        cursor.execute(sql, data)
        return cursor.rowcount == 1

    def check_employee(self, employee_id):
        sql = 'SELECT * FROM employee WHERE Id=%s'
        cursor = self.connection.cursor(buffered=True)
        data = (employee_id,)
        cursor.execute(sql, data)
        return cursor.rowcount == 1

    def add_employee(self):
        print("{:>60}".format("-->> Add Employee Record <<--"))
        employee_id = input("Enter Employee Id: ")

        if self.check_employee(employee_id):
            print("Employee ID Already Exists\nTry Again..")
            input("Press Any Key To Continue..")
            self.add_employee()

        employee_name = input("Enter Employee Name: ")
        if self.check_employee_name(employee_name):
            print("Employee Name Already Exists\nTry Again..")
            input("Press Any Key To Continue..")
            self.add_employee()

        email_id = input("Enter Employee Email ID: ")
        if re.fullmatch(self.email_regex, email_id):
            print("Valid Email")
        else:
            print("Invalid Email")
            input("Press Any Key To Continue..")
            self.add_employee()

        phone_number = input("Enter Employee Phone No.: ")
        if self.phone_pattern.match(phone_number):
            print("Valid Phone Number")
        else:
            print("Invalid Phone Number")
            input("Press Any Key To Continue..")
            self.add_employee()

        address = input("Enter Employee Address: ")
        post = input("Enter Employee Post: ")
        salary = input("Enter Employee Salary: ")

        data = (employee_id, employee_name, email_id, phone_number, address, post, salary)
        sql = 'INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor = self.connection.cursor()
        cursor.execute(sql, data)
        self.connection.commit()

        print("Successfully Added Employee Record")
        input("Press Any Key To Continue..")
        self.menu()

    def display_employees(self):
        print("{:>60}".format("-->> Display Employee Records <<--"))
        sql = 'SELECT * FROM employee'
        cursor = self.connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        for record in records:
            self.display_employee_details(record)

        input("Press Any Key To Continue..")
        self.menu()

    def display_employee_details(self, employee):
        print("Employee Id: ", employee[0])
        print("Employee Name: ", employee[1])
        print("Employee Email Id: ", employee[2])
        print("Employee Phone No.: ", employee[3])
        print("Employee Address: ", employee[4])
        print("Employee Post: ", employee[5])
        print("Employee Salary: ", employee[6])
        print("\n")

    def search_employee(self):
        print("{:>60}".format("-->> Search Employee Record <<--"))
        employee_id = input("Enter Employee Id: ")

        if not self.check_employee(employee_id):
            print("Employee Record Not exists\nTry Again")
            input("Press Any Key To Continue..")
            self.menu()
        else:
            sql = 'SELECT * FROM employee WHERE Id = %s'
            data = (employee_id,)
            cursor = self.connection.cursor()
            cursor.execute(sql, data)

            records = cursor.fetchall()
            for record in records:
                self.display_employee_details(record)

            input("Press Any Key To Continue..")
            self.menu()

    def menu(self):
        print("{:>100}".format("************************************"))
        print("{:>100}".format("-->> Employee Management System <<--"))
        print("{:>100}".format("************************************"))
        print("1. Add Employee")
        print("2. Display Employee Records")
        print("3. Update Employee Record")
        print("4. Promote Employee Record")
        print("5. Remove Employee Record")
        print("6. Search Employee Record")
        print("7. Exit\n")
        print("{:>60}".format("-->> Choice Options: [1/2/3/4/5/6/7] <<--"))

        choice = int(input("Enter your Choice: "))

        if choice == 1:
            self.add_employee()
        elif choice == 2:
            self.display_employees()
        elif choice == 6:
            self.search_employee()
        elif choice == 7:
            print("{:>60}".format("Have A Nice Day :)"))
            exit(0)
        else:
            print("Invalid Choice!")
            input("Press Any Key To Continue..")
            self.menu()

if __name__ == "__main__":
    emp_system = EmployeeManagementSystem()
    emp_system.menu()
