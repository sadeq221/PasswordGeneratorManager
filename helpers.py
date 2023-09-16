import sys
import platform
import csv
import os
import time
from pwinput import pwinput
from password_generator import generate

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


# Check the operation system to set the right "clear terminal" command
if platform.system() == "Windows":
    clean = "cls"
else:
    clean = 'clear'


# To get the master password from "master.csv" file
def get_master_password():
    with open(BASE_DIR / "csv/master.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            return row[1]
        

# Intialize the accounts database
def intialize_accounts():
    with open(BASE_DIR / "csv/accounts.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["number", "account", "password"])
        writer.writeheader()


# Set the master password
def set_master_password():
    # Clear Terminal
    os.system(clean)

    print("** Choose a Master Password for the App **\n\n")
    print(">>> Your password must be at least 8 characters including: ")
    print("    upper and lowercase letters, numbers, and symbols\n")

    while True:
        try:
            password = input("Enter Password: ")

            # Raises ValueError if the password is unacceptable
            Master_password_reuirements(password)

            # Password confirmation (Avoid empty input)
            confirm_password = False
            while not confirm_password:
                confirm_password = input("\nConfirm your Password: ")

            if confirm_password != password:
                sys.exit("\n* Passwords dont match ! *\n")

        # Reprompt for password
        except ValueError:
            pass
        else:
            # Save the Master password to the csv file
            with open(BASE_DIR / "csv/master.csv", "w") as f:
                f.write(f'master,"{password}"')

            # Go to the main page
            print("Password was successfully set")
            time.sleep(2)
            main_page()


# Master password requirements
def Master_password_reuirements(password):
    # Check length
    if len(password) < 8:
        print("\nThe password must be at least 8 characters\n")
        raise ValueError

    # Check number existence
    if not any(char.isdigit() for char in password):
        print("\nThe password must include at least one number\n")
        raise ValueError

    # Check lowercase existence
    if not any(char.islower() for char in password):
        print("\nThe password must include at least one lowercase letter\n")
        raise ValueError

    # Check uppercase existence
    if not any(char.isupper() for char in password):
        print("\nThe password must include at least one uppercase letter\n")
        raise ValueError

    # Check symbol existence
    if not any(not char.isalnum() for char in password):
        print("\nThe password must include at least one symbol\n")
        raise ValueError


def ask_master_password():
    # Clear Terminal
    os.system(clean)

    # Getting the master password from the user (Avoid Empty password)
    inp_password = False
    while not inp_password:
        inp_password = pwinput("\nEnter your password: ")

    # If Wrong Password
    if inp_password != get_master_password():
        sys.exit("\n** Wrong Password **\n")
    else:
        main_page()


def main_page():
    # Clear Terminal
    os.system(clean)

    print("** Welcome to PassworGM **")

    # Options Menu
    print("\n----------------------------------------")
    print("A. Add new account | S. Setting | E. Exit")
    print("----------------------------------------\n")

    # Get the current accounts from the database
    accounts = []
    with open(BASE_DIR / "csv/accounts.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            accounts.append(row)

    # If there are no saved accounts
    if not accounts:
        print("No Accounts yet !!")

    # Print the accounts as a list
    else:
        print("\nList of accounts: ")
        print("-------------------")
        for account in accounts:
            print(f"{account['number']}. {account['account']}")
            print("-------------------")

    # Listening for the user input
    while True:
        try:
            choice = input("\nSelect: ")

            if choice in ("E", "e"):
                # Clear Terminal and Exit the program
                os.system(clean)

                #Exit
                sys.exit()

            elif choice in ("S", "s"):
                return open_setting()

            # Adding a new account
            elif choice in ("A", "a"):
                # Intialize the new account dictionary
                new_account = {
                    "number": len(accounts) + 1,
                    "account": None,
                    "password": None
                }

                # Open the "add-account-new" page and pass the new account dictionary
                return set_new_account_name(new_account)

            # Choosing one of current accounts to get its details
            choice = int(choice)
            if 0 < choice <= len(accounts):
                # Open the "account-details" page and pass the selected account as a dictionary
                return account_details(accounts[choice - 1])

            # If none of the above
            raise ValueError

        except ValueError:
            print("Invalid Input")


def open_setting():
    # Clear Terminal
    os.system(clean)

    # Options Menu
    print("\n-----------------------------------------")
    print("B. Back | M. Change Master Password")
    print("-----------------------------------------\n")

    # Listening for user input
    while True:
        try:
            choice = input("\nSelect: ")

            # Back to main page
            if choice in ("B", "b"):
                return main_page()

            # Reload the password page (Regenerate password)
            elif choice in ("M", "m"):
                return set_master_password()

            # Invalid Input
            else:
                raise ValueError

        except ValueError:
            print("Invalid Input")


def set_new_account_name(account):
    # Clear Terminal
    os.system(clean)

    # Options Menu
    print("\n-----------------------------------------")
    print("B. back")
    print("-----------------------------------------\n")

    # Getting the new account name 
    choice = False
    while not choice:
        choice = input("Enter new account name: ")

    # Back to the main page
    if choice in ("B", "b"):
        main_page()
    else:
        # Add the "account name" to the new account dictionary
        account["account"] = choice

        # Go to "set-accout-password" page
        set_new_account_password(account)


def set_new_account_password(account):
    # Clear Terminal
    os.system(clean)

    # Options Menu
    print("\n-----------------------------------------")
    print("S. Save | R. Regenerate | B. Back")
    print("-----------------------------------------\n")

    # Generate Random password and Add it to the account dictionary
    account["password"] = generate()

    # Preview account Name and Password
    print(f"Account Name: {account['account']}\n")
    print(f"Password: {account['password']}\n")

    # Listening for user input
    while True:
        try:
            choice = input("\nSelect: ")

            # Back to "set-account-name" page
            if choice in ("B", "b"):
                set_new_account_name(account)
                return

            # Reload the password page (Regenerate password)
            elif choice in ("R", "r"):
                set_new_account_password(account)
                return

            # Save the new account
            elif choice in ("S", "s"):
                with open(BASE_DIR / "csv/accounts.csv", "a", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["number", "account", "password"])
                    writer.writerow(account)

                print("Successfuly Saved")
                time.sleep(2)
                # Go back to the main page
                main_page()
                return

            # Invalid Input
            else:
                raise ValueError

        except ValueError:
            print("Invalid Input")


def account_details(account):
    # Clear Terminal
    os.system(clean)

    # Options Menu
    print("\n-----------------------------------------")
    print("B. Back | N. Change Name | P. Change Password | D. Delete")
    print("-----------------------------------------\n")

    # Preview account Name and Password
    print(f"Account Name: {account['account']}\n")
    print(f"Password: {account['password']}\n")

    # Listening for user input
    while True:
        try:
            choice = input("\nSelect: ")

            # Back to "main-page"
            if choice in ("B", "b"):
                main_page()
                return

            # Go to "change-name" page
            if choice in ("N", "n"):
                change_account_name(account)
                return

            # Go to "change-password" page
            if choice in ("P", "p"):
                change_account_password(account)
                return

            # Go to "Delete-account" page
            if choice in ("D", "d"):
                delete_account(account)
                return

            # Invalid Input
            else:
                raise ValueError

        except ValueError:
            print("Invalid Input")


def change_account_name(account):
    # Clear Terminal
    os.system(clean)

    # Avoide empty input
    new_name = False
    while not new_name:
        new_name = input("Enter a new name: ")

    # Update the name in the account dictionary
    account["account"] = new_name

    # Update the database
    # Get the current list of accounts from the database
    accounts = []
    with open(BASE_DIR / "csv/accounts.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            accounts.append(row)

    # Update the list
    accounts[int(account['number']) - 1] = account

    # Write back the new list of accounts to the database
    with open(BASE_DIR / "csv/accounts.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["number", "account", "password"])
        writer.writeheader()
        writer.writerows(accounts)

    # Go back to main page
    print("Success: Name changed")
    time.sleep(2)
    main_page()


def change_account_password(account):
    # Clear Terminal
    os.system(clean)

    # Options Menu
    print("\n-----------------------------------------")
    print("S. Save | R. Regenerate | B. Back")
    print("-----------------------------------------\n")

    # Generate Random password and Add it to the account dictionary
    account["password"] = generate()

    # Preview account Name and Password
    print(f"New Password: {account['password']}\n")

    # Listening for user input
    while True:
        try:
            choice = input("\nSelect: ")

            # Back to "set-account-name" page
            if choice in ("B", "b"):
                account_details(account)
                return

            # Reload the password page (Regenerate password)
            elif choice in ("R", "r"):
                change_account_password(account)
                return

            # Save the new account
            elif choice in ("S", "s"):

                # Update the database
                # Get the current list of accounts from the database
                accounts = []
                with open(BASE_DIR / "csv/accounts.csv") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        accounts.append(row)

                # Update the list
                accounts[int(account['number']) - 1] = account

                # Write back the new list of accounts to the database
                with open(BASE_DIR / "csv/accounts.csv", "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["number", "account", "password"])
                    writer.writeheader()
                    writer.writerows(accounts)

                # Go back to "main-page"
                print("Success: Password changed")
                time.sleep(2)
                main_page()

                return

            # Invalid Input
            else:
                raise ValueError

        except ValueError:
            print("Invalid Input")


def delete_account(account):
    # Clear Terminal
    os.system(clean)

    # Options Menu
    print("\n-----------------------------------------")
    print("Y. Yes | N. No")
    print("-----------------------------------------\n")

    # Listening for user input
    while True:
        try:
            choice = input(f"\nAre you sure to DELETE {account['account']} ? ").lower()

            # Back to "set-account-name" page
            if choice in ("yes", "y"):
                # Update the database
                # Get the current list of accounts from the database
                accounts = []
                with open(BASE_DIR / "csv/accounts.csv") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Skip the current account
                        if not row == account:
                            accounts.append(row)

                # Update the numbers in the list
                for i in range(len(accounts)):
                    accounts[i]["number"] = i + 1

                # Write back the new list of accounts to the database
                with open(BASE_DIR / "csv/accounts.csv", "w", newline="") as file:
                    writer = csv.DictWriter(
                        file, fieldnames=["number", "account", "password"])
                    writer.writeheader()
                    writer.writerows(accounts)

                # Go back to main page
                main_page()

                return

            # Reload the password page (Regenerate password)
            elif choice in ("no", "n"):
                # Go back to the main page
                main_page()
                return

            # Invalid Input
            else:
                raise ValueError

        except ValueError:
            print("Invalid Input")