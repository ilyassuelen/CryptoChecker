import crypto_storage_sql as storage
import random
import statistics


# ---------------
# Program Menu
# ---------------
def interface(user_id):
    while True:
        print("""
Menu:
0. Exit
1. List all Cryptocurrencies
2. Add Cryptocurrency
3. Delete Cryptocurrency
4. Stats
5. Search Cryptocurrency
6. Cryptos sorted by biggest daily change
7. Cryptos sorted by Source Exchange
""")
        choice = input("Enter choice (0-7): ")

        if choice == "0":
            print(f"Bye {user_id}!")
            break
        elif choice == "1":
            list_cryptos(user_id)
        elif choice == "2":
            add_crypto(user_id)
        elif choice == "3":
            delete_crypto(user_id)
        elif choice == "4":
            crypto_stats(user_id)
        elif choice == "5":
            search_crypto(user_id)
        elif choice == "6":
            cryptos_sorted_by_biggest_daily_change(user_id)
        elif choice == "7":
            cryptos_sorted_by_source_exchange(user_id)
        else:
            print("Invalid choice, please enter a number between 0 and 7")

        input("\nPress Enter to continue...")


# ----------------
# Functions
# ----------------
def select_user():
    """Let the user select an existing user or create a new one."""
    users = storage.list_users()

    print("Welcome to CryptoChecker!\n")
    if not users:
        print("No users found. Let's create one!")
        name = input("Enter your name: ")
        storage.add_user(name)
        users = storage.list_users()

    print("Select a user: ")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user[1]}")
    print(f"{len(users)+1}. Create new user")

    choice = int(input("Enter choice: "))

    if choice == len(users) + 1:
        name = input("Enter new user name: ")
        storage.add_user(name)
        users = storage.list_users()
        return next(user[0] for user in users if user[1] == name)

    return users[choice - 1][0]

def main():
    """Main program loop for the Cryptocurrency Database application."""
    # Choose user
    user_id = select_user()

    # Run the Menu
    interface(user_id)


if __name__ == "__main__":
    main()