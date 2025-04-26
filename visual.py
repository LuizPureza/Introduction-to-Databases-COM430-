

def display_menu():
    """Display the main menu."""
    print("\nPARANÁ – SHOPPER MAIN MENU")
    print("\u2500"*10000)
    print("1. Display your order history")
    print("2. Add an item to your basket")
    print("3. View your basket")
    print("4. Change the quantity of an item in your basket")
    print("5. Remove an item from your basket")
    print("6. Checkout")
    print("7. Exit")

    return input("\nEnter the number of the option you'd like to choose: ")

def display_welcome(shopper_name):
    """Show a welcome message for validated shoppers."""
    print(f"\nWelcome, {shopper_name}!")



def display_order_history(orders):
    """Format and display order history in a table format."""
    print("\n" + "="*60)
    print("              ORDER HISTORY             ")
    print("="*60)

    if not orders:
        print("\nNo orders placed by this shopper.")
        return

    print("\n{:<10} | {:<12} | {:<40} | {:<20} | {:<7} | {:<4} | {:<10}".format(
        "OrderID", "Order Date", "Product Description", "Seller", "Price", "Qty", "Status"
    ))
    print("-" * 110)

    for order in orders:
        order_id, order_date, product_description, seller_name, price, quantity, status = order
        print("{:<10} | {:<12} | {:<40} | {:<20} | £{:<6.2f} | {:<4} | {:<10}".format(
            order_id, order_date, product_description[:40], seller_name, price, quantity, status
        ))

    print("\nReturning to main menu...")

def display_categories(categories):
    """Show product categories using the _display_options helper function."""
    return _display_options(categories, "Select a Product Category", "category")


def _display_options(all_options, title, type):
    """Display a numbered list of options and return the ID of the selected option."""
    option_num = 1
    option_list = []
    print("\n", title, "\n")

    for option in all_options:
        code = option[0]  # ID of the option
        desc = option[1]  # Description of the option
        print("{0}.\t{1}".format(option_num, desc))
        option_num += 1
        option_list.append(code)

    selected_option = 0
    while selected_option not in range(1, len(option_list) + 1):
        try:
            selected_option = int(input(f"Enter the number against the {type} you want to choose: "))
            if 1 <= selected_option <= len(option_list):
                return option_list[selected_option - 1]  # ✅ Return correct ID
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def display_products(products):
    """Show products using the _display_options helper function."""
    return _display_options(products, "Select a Product", "product")

def display_sellers(sellers):
    """Show sellers and prompt user for selection."""
    print("\n" + "="*40)
    print("       SELECT A SELLER       ")
    print("="*40)

    for num, (_, seller_name, price) in enumerate(sellers, 1):
        print(f"{num}. {seller_name} - £{price:.2f}")

    selected_option = 0
    while selected_option not in range(1, len(sellers) + 1):
        try:
            selected_option = int(input("\nEnter the number of the seller you want to buy from: "))
            if 1 <= selected_option <= len(sellers):
                return sellers[selected_option - 1][0], sellers[selected_option - 1][2]  # ✅ Returns seller_id & price
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def prompt_quantity():
    """Prompt user to enter the quantity of the selected product and validate input."""
    while True:
        try:
            quantity = int(input("\nEnter the quantity of the product you wish to order: "))
            if quantity > 0:
                return quantity  # ✅ Valid quantity
            else:
                print("The quantity must be greater than 0. Please enter a valid amount.")
        except ValueError:
            print("Invalid input. Please enter a number.")



def display_basket_contents(basket_items, total_cost):
    """Format and display basket contents with proper column alignment."""
    print("\nBasket Contents")
    print("-" * 100)

    if not basket_items:
        print("\nYour basket is empty.")
        return

    # Header row with correct spacing
    print("\n{:<5} {:<75} {:<15} {:<8} {:<10} {:<10}".format(
        "Item", "Product Description", "Seller Name", "Qty", "Price", "Total"
    ))
    print("-" * 100)

    # Display each item with precise spacing
    for num, item in enumerate(basket_items, 1):
        product_id, product_description, seller_name, quantity, price = item
        total_price = quantity * price
        print("{:<5} {:<75} {:<15} {:<8} £{:>9.2f} £{:>9.2f}".format(
            num, product_description[:75], seller_name, quantity, price, total_price
        ))

    print("-" * 100)
    print("\n{:<5} {:<75} {:<15} {:<8} {:<10} £{:>9.2f}".format("", "", "Basket Total", "", "", total_cost))









def select_basket_item(basket_items):
    """Prompt user to select the basket item they wish to modify."""
    if len(basket_items) == 1:
        print("\nOnly one item in your basket—this will be updated.")
        return 1  # ✅ Auto-select the only item

    while True:
        try:
            choice = int(input("\nEnter the basket item no. of the item you want to change: "))
            if 1 <= choice <= len(basket_items):
                return choice  # ✅ Valid selection
            else:
                print("\nThe basket item no. you have entered is invalid.")
        except ValueError:
            print("\nInvalid input. Enter a number.")


def prompt_new_quantity():
    """Prompt the user to enter a new quantity for the selected item and validate input."""
    while True:
        try:
            new_quantity = int(input("\nEnter the new quantity for the item: "))
            if new_quantity > 0:
                return new_quantity  # ✅ Valid quantity
            else:
                print("The quantity must be greater than 0. Please enter a valid amount.")
        except ValueError:
            print("Invalid input. Please enter a number.")
