import sqlite3

def connect_db():
    """to connect and retrive data from the SQLite database"""
    try:
        conn = sqlite3.connect(r'C:\Users\purez\OneDrive\Desktop\COM430\parana.db')
        return conn
    except Exception as e:
        print(f"failing to connect to database: {e}")
        return None


def validate_shopper():
    """to prompt user for shopper ID and validate"""
    conn = connect_db()
    cursor = conn.cursor()

    while True:
        shopper_id = input("\nEnter your Shopper ID: ")
        cursor.execute("SELECT shopper_first_name FROM Shoppers WHERE shopper_id = ?", (shopper_id,))
        result = cursor.fetchone()

        if result:
            print(f"\nWelcome, {result[0]}!")
            return shopper_id
        else:
            print(f"Error: Shopper ID '{shopper_id}' not found. Please try again.")


def display_menu():
    """main menu"""
    print("\nPARANÁ – SHOPPER MAIN MENU")
    print("\n" + "-" * 100000)
    print("1. Display your order history")
    print("2. Add an item to your basket")
    print("3. View your basket")
    print("4. Change the quantity of an item in your basket")
    print("5. Remove an item from your basket")
    print("6. Checkout")
    print("7. Exit")

    return input("\nEnter the number of the option you'd like to choose: ")


def main():
    """Main function to run the shopper menu."""
    shopper_id = validate_shopper()

    while True:
        choice = display_menu()

        if choice == "1":
            print("Display your order history")
        elif choice == "2":
            print("Add an item to your basket")
        elif choice == "3":
            print("View your basket")
        elif choice == "4":
            print("Change the quantity of an item in your basket")
        elif choice == "5":
            print("Remove an item from your basket")
        elif choice == "6":
            print("6.	Checkout")
        elif choice == "7":
            print("Exit")
            break
        else:
            print("\nInvalid choice. Please try again")


if __name__ == "__main__":
    main()