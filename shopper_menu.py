import process
import visual

def main():
    """Main function to run the shopper menu."""
    shopper_id, shopper_name = process.validate_shopper()
    visual.display_welcome(shopper_name)

    basket_id = process.get_existing_basket(shopper_id)
    if basket_id:
        print(f"\nYou have an existing basket (ID: {basket_id}) from today.")

    while True:
        choice = visual.display_menu()

        if choice == "1":  # Display Order History
            orders = process.get_order_history(shopper_id)
            visual.display_order_history(orders)

        if choice == "2":  # Add item to basket
            categories = process.get_product_categories()
            category_id = visual.display_categories(categories)

            print(f"\nSelected Category ID: {category_id}")  # Debugging step

            if category_id:
                products = process.get_products_by_category(category_id)
                product_id = visual.display_products(products)

                print(f"\nSelected Product ID: {product_id}")  # Debugging step

                if product_id:
                    sellers = process.get_sellers_by_product(product_id)
                    seller_id, price = visual.display_sellers(sellers)

                    print(f"\nSelected Seller ID: {seller_id}, Price: £{price:.2f}")  # Debugging step

                    if seller_id:  # ✅ Your code should go here
                        quantity = visual.prompt_quantity()
                        print(f"\nSelected Quantity: {quantity}")  # Debugging step

                        basket_id = process.get_or_create_basket(shopper_id)  # ✅ Ensure the shopper has a basket
                        print(f"\nUsing Basket ID: {basket_id}")  # Debugging step

                    if basket_id:
                        process.add_to_basket(basket_id, product_id, seller_id, quantity,
                                              price)  # ✅ Insert item into database
                        print("\nItem added to your basket!")  # ✅ Confirmation message


        elif choice == "3":  # View Basket
            basket_id = process.get_existing_basket(shopper_id)  # ✅ Retrieve current basket
            if basket_id:
                basket_items, total_cost = process.get_basket_contents(basket_id)
                visual.display_basket_contents(basket_items, total_cost)
            else:
                print("\nYour basket is empty.")

        elif choice == "4":  # Change Item Quantity
            basket_id = process.get_existing_basket(shopper_id)  # ✅ Retrieve current basket

            if not basket_id:
                print("\nYour basket is empty.")
                return

            basket_items, total_cost = process.get_basket_contents(basket_id)

            if not basket_items:
                print("\nYour basket is empty.")
                return

            visual.display_basket_contents(basket_items, total_cost)  # ✅ Show basket contents

            # Select the basket item to modify
            item_index = visual.select_basket_item(basket_items) - 1  # ✅ Convert item number to index
            product_id = basket_items[item_index][0]  # ✅ Retrieve corresponding product_id

            # Prompt for new quantity
            new_quantity = visual.prompt_new_quantity()
            # Update basket contents
            process.update_basket_item(basket_id, product_id, new_quantity)
            # Retrieve and display updated basket with recalculated total
            basket_items, total_cost = process.get_basket_contents(basket_id)
            visual.display_basket_contents(basket_items, total_cost)  # ✅ Show updated basket







        elif choice == "7":
            print("Exiting the program...")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()


