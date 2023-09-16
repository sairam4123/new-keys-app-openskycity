import os
import users
import keys
import db

from user_manager import UserManager
from key_manager import KeysManager
from constants import API, VERSION, DATABASE

print(" " * 2 + "-" * 72 + " " * 2)
print("OpenSkyCity Users and Keys Manager (Console Edition)".center(78))
print(" " * 2 + "-" * 72 + " " * 2)
print(f"Version: {VERSION}")
print(f"Database: {DATABASE}")
print(f"API: {API}")
print(" " * 2 + "-" * 72 + " " * 2)
dm = db.DatabaseManager.from_file("keys.db")
dm.generate_tables()

um = UserManager()

km = KeysManager()

dev_mode = False
dev = False
logged_in = False


def print_menu():
    print("Main Menu")
    print("1. Register")
    print(f"2. {'Login' if not logged_in else 'Logout'}")
    if logged_in:
        print("3. Buy a key")
        print("4. List all owned keys")
        print("5. Sell a key")
        print("6. Print your account details")
        if dev:
            print("7. List all users")
            print("8. List all keys")
            print("9. Print info about a specific user")
    print("*: Exit")
    print("0: Print this menu")

def save():
    um._save()
    km._save()


print_menu()
menu_option = ""
try:
    while menu_option != "*":

        logged_in = bool(um.logged_user)
        logged_user = um.logged_user
        if logged_user:
            dev = logged_user.type == users.UserType.DEVELOPER or dev_mode
        
        save()

        menu_option = input(f"{('(DEV CONSOLE) ' if dev else '')}Enter an option: ")

        if menu_option == "*":
            continue

        if menu_option == "DEV ACTIVATE":
            dev_mode = True
            print("Dev Mode activated, GG!")
            continue

        if menu_option != "*":
            try:
                if not logged_in and int(menu_option) > 2:
                    print("This option does not exist")
                    continue

                if not dev and logged_in and int(menu_option) > 6:
                    print("This option does not exist")
                    continue
                    
                if dev and int(menu_option) > 9:
                    print("This option does not exist")
                    continue
                
            except Exception as e:
                print(e)
                continue

        match menu_option:
            case "1":
                print("Register")
                name = input("Name: ")
                password = input("Password: ")
                um.create_user(name, users.UserType.BASIC, password)
                print("User created successfully!")

            case "2":
                if logged_in:
                    if um.logout():
                        print("Logged out successfully")
                    else:
                        print("Failed to logout... are you sure you logged in?")
                    continue

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
                    continue
                print("Key Menu")
                print("1. Premium")
                print("2. Special Sandbox")
                key_type = keys.KeyType(
                    int(input("Which key would you like to buy?: "))
                )
                key = km.create_key(key_type)
                print(f"The alotted key: {key}")
                logged_user.add_key(key)

            case "4":
                print("Listing all owned keys...")
                if not logged_user:
                    print("Please login to view your owned keys")
                    continue

                for key in logged_user.keys:
                    print(key.value, key.type)

            case "5":
                if not logged_user:
                    print("You cannot sell a key if you are not logged in.")
                    continue
                
                for idx, key in enumerate(logged_user.keys, 1):
                    print(str(idx) + ".", key.value)
                sell_option = input("Enter the option which you want to sell: ")
                if int(sell_option) > len(logged_user.keys):
                    print("The key you want to sell does not exist.")
                    
                    continue

                key = logged_user.keys[int(sell_option)-1]
                confirm = input("Are you sure you want to sell this key?: ")
                if not confirm.lower().startswith("y"):
                    print("Cancelled the action!")
                    
                    continue

                logged_user.remove_key(key)
                print("Key sold successfully! You won't be able to buy this key again!")


            case "6":
                if not logged_user:
                    print("This should not happen, crashing!")
                    continue

                print("Printing your account details")
                print(logged_user.name, logged_user.type)
            case "7":
                print("Listing all users...")
                from pprint import pprint

                all_users = um.list_all_users()
                pprint([user.to_tuple() for user in all_users])

            case "8":
                print("Listing all keys...")
                from pprint import pprint

                all_keys = km.list_all_keys()
                pprint([key.to_tuple() for key in all_keys])
            case "9":
                from pprint import pprint

                print("Printing user details...")
                name = input("Enter the user name: ")
                pprint(um.get_user(name))

            case "0":
                print_menu()

            case _:
                print("Not implemented!")

        

except Exception as e:
    import traceback

    traceback.print_exception(e)
    os.system("pause")
    quit()

print("Saving all changes")
save()
print("Thank you for using the system!")
os.system("pause")
