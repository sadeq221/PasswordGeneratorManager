from helpers import *

def main():

    # Check if it's the first use of the App
    if get_master_password() == "None":
        intialize_accounts()
        set_master_password()
    else:
        ask_master_password()


if __name__ == "__main__":
    main()
