import os
import users
import keys
import db

from user_manager import UserManager
from key_manager import KeysManager
from constants import API, VERSION, DATABASE

print("-" * 72)
print("OpenSkyCity Users and Keys Manager (Console Edition)".center(72))
print("-" * 72)
print(f"Version: {VERSION}")
print(f"Database: {DATABASE}")
print(f"API: {API}")
print("-" * 72)

dm = db.DatabaseManager.from_file("keys.db")
dm.generate_tables()

um = UserManager()

km = KeysManager()

dev = False
logged_in = False

def print_menu():
    print("Main Menu")
    print("1. Register")
    print(f"2. {'Login' if not logged_in else 'Logout'}")
    if logged_in:
        print("3. Buy a key")
        print("4. List all owned keys")
        print("5. Print your account details")
        if dev:
            print("6. List all users")
            print("7. List all keys")
            print("8. Print info about a specific user")
    print("*: Exit")
    print("0: Print this menu")

print_menu()
menu_option = input("Enter an option: ")
try:
    while menu_option != "*":
        logged_in = bool(um.logged_user)
        logged_user = um.logged_user
        if logged_user:
            dev = logged_user.type == users.UserType.DEVELOPER
        if menu_option != "*":
            if not logged_in and int(menu_option) > 2:
                print("This option does not exist")
                menu_option = input("Enter an option: ")
                continue
            if not dev and logged_in and int(menu_option) > 5:
                print("This option does not exist")
                menu_option = input("Enter an option: ")
                continue
            if dev and int(menu_option) > 8:
                print("This option does not exist")
                menu_option = input("Enter an option: ")
                continue


        match menu_option:
            case "1":
                print("Register")
                name = input("Name: ")
                password = input("Password: ")
                um.create_user(name, users.UserType.BASIC, password)
                print("User created successfully!")

            case "2":
                print("Login")
                name = input("Name: ")
                pw = input("Password: ")

                if um.login(name, pw):
                    print("Logged in successfully!")
                else:
                    print("Failed to login, check the credentials!")
                
            case "3":
                print("Buy a key")
                if not logged_user:
                    print("You are not logged in!")
                    menu_option = input("Enter an option: ")
                    continue
                print("Key Menu")
                print("1. Premium")
                print("2. Special Sandbox")
                key_type = keys.KeyType(
                    int(input("Which key would you like to buy?: "))
                )
                key = km.create_key(key_type)
                print(f"The generated key: {key}")
                logged_user.add_key(key)

            case "4":
                print("Listing all owned keys...")
                if not logged_user:
                    print("Please login to view your owned keys")
                    menu_option = input("Enter an option: ")
                    continue
                    
                for key in logged_user.keys:
                    print(key.value, key.type)
            
            case "5":
                if not logged_user:
                    print("This should not happen, crashing!")
                    continue

                print("Printing your account details")
                print(logged_user.name, logged_user.type)
            case "6":
                print("Listing all users...")
                from pprint import pprint
                all_users = um.list_all_users()
                pprint([user.to_tuple() for user in all_users])
            
            case "7":
                print("Listing all keys...")
                from pprint import pprint
                all_keys = km.list_all_keys()
                pprint([key.to_tuple() for key in all_keys])
            case "8":
                from pprint import pprint
                print("Printing user details...")
                name = input("Enter the user name: ")
                pprint(um.get_user(name))

            case "0":
                print_menu()
            
            case _:
                print("Not implemented!")
            
        menu_option = input("Enter an option: ")

except Exception as e:
    import traceback
    traceback.print_exception(e)
    os.system("pause")
    quit()

print("Saving all changes")
um._save()
km._save()
print("Thank you for using the system!")
os.system("pause")
