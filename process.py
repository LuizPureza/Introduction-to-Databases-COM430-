import sqlite3
import visual


def connect_db():
    """Connect to the SQLite database."""
    try:
        conn = sqlite3.connect(r'C:\Users\purez\OneDrive\Desktop\COM430\parana.db')  # Ensure this path is correct
        return conn
    except Exception as e:
        print(f"Error: Failed to connect to database - {e}")
        return None

def validate_shopper():
    """Prompt for shopper ID and validate it."""
    conn = connect_db()
    cursor = conn.cursor()

    while True:
        shopper_id = input("\nEnter your Shopper ID: ")

        cursor.execute("SELECT shopper_first_name FROM shoppers WHERE shopper_id = ?", (shopper_id,))
        result = cursor.fetchone()

        if result:
            conn.close()
            return shopper_id, result[0]  # ✅ Returns shopper_id & shopper_name
        else:
            print(f"Error: Shopper ID '{shopper_id}' not found. Please try again.")

def get_existing_basket(shopper_id):
    """Check if the shopper has an existing basket today and retrieve the most recent one."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT basket_id 
        FROM shopper_baskets 
        WHERE shopper_id = ? 
        AND DATE(basket_created_date_time) = DATE('now') 
        ORDER BY basket_created_date_time DESC 
        LIMIT 1
    """, (shopper_id,))

    basket = cursor.fetchone()
    conn.close()
    return basket[0] if basket else None  # ✅ Returns `basket_id` if found, else `None`


def get_order_history(shopper_id):
    """Retrieve order history for the given shopper."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT o.order_id,
               o.order_date,
               p.product_description,
               s.seller_name,
               op.price,
               op.quantity,
               op.ordered_product_status
        FROM shopper_orders o
        JOIN ordered_products op ON o.order_id = op.order_id
        JOIN products p ON op.product_id = p.product_id
        JOIN sellers s ON op.seller_id = s.seller_id
        WHERE o.shopper_id = ?
        ORDER BY o.order_date DESC
    """, (shopper_id,))

    orders = cursor.fetchall()
    conn.close()

    return orders  # ✅ Returns list of (order_id, order_date, product_description, seller_name, price, quantity, status)


def get_product_categories():
    """Retrieve product categories in alphabetical order."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT category_id, category_description FROM categories ORDER BY category_description ASC")
    categories = cursor.fetchall()
    conn.close()

    return categories  # ✅ Returns (category_id, category_description) tuples


def get_products_by_category(category_id):
    """Retrieve products in the selected category."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT product_id, product_description
                   FROM products
                   WHERE category_id = ?
                   ORDER BY product_description ASC
                   """, (category_id,))

    products = cursor.fetchall()
    conn.close()

    return products  # ✅ Returns list of (product_id, product_description)


def get_sellers_by_product(product_id):
    """Retrieve sellers and prices for the selected product."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT product_sellers.seller_id, sellers.seller_name, product_sellers.price
                   FROM product_sellers
                            JOIN sellers ON product_sellers.seller_id = sellers.seller_id
                   WHERE product_sellers.product_id = ?
                   ORDER BY sellers.seller_name ASC
                   """, (product_id,))

    sellers = cursor.fetchall()
    conn.close()

    return sellers  # ✅ Returns list of (seller_id, seller_name, price)


def get_basket_contents(basket_id):
    """Retrieve all items in the shopper's basket."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT bc.product_id, p.product_description, s.seller_name, bc.quantity, bc.price
                   FROM basket_contents bc
                            JOIN products p ON bc.product_id = p.product_id
                            JOIN sellers s ON bc.seller_id = s.seller_id
                   WHERE bc.basket_id = ?
                   ORDER BY p.product_description ASC
                   """, (basket_id,))

    basket_items = cursor.fetchall()

    # Calculate total basket cost
    total_cost = sum(item[3] * item[4] for item in basket_items) if basket_items else 0.0

    conn.close()

    return basket_items, total_cost  # ✅ Returns basket items + total cost


def get_or_create_basket(shopper_id):
    """Retrieve the most recent basket or create a new one."""
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the shopper has an existing basket today
    cursor.execute("""
                   SELECT basket_id
                   FROM shopper_baskets
                   WHERE shopper_id = ?
                     AND DATE (basket_created_date_time) = DATE ('now')
                   ORDER BY basket_created_date_time DESC
                       LIMIT 1
                   """, (shopper_id,))

    basket = cursor.fetchone()

    if basket:
        conn.close()
        return basket[0]  # ✅ Use existing basket ID

    # If no basket exists, get the next basket_id from sqlite_sequence
    cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='shopper_baskets'")
    next_basket_id = cursor.fetchone()[0] + 1  # ✅ Get the next available basket_id

    # Create a new basket for the shopper
    cursor.execute("""
                   INSERT INTO shopper_baskets (basket_id, shopper_id, basket_created_date_time)
                   VALUES (?, ?, CURRENT_TIMESTAMP)
                   """, (next_basket_id, shopper_id))
    conn.commit()

    conn.close()
    return next_basket_id  # ✅ Return the newly created basket ID

def add_to_basket(basket_id, product_id, seller_id, quantity, price):
    """Insert the product into the basket or update its quantity if it already exists."""
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the item already exists in the basket
    cursor.execute("""
        SELECT quantity FROM basket_contents 
        WHERE basket_id = ? AND product_id = ?
    """, (basket_id, product_id))

    existing_item = cursor.fetchone()

    if existing_item:
        # ✅ If item exists, update quantity
        new_quantity = existing_item[0] + quantity
        cursor.execute("""
            UPDATE basket_contents
            SET quantity = ?
            WHERE basket_id = ? AND product_id = ?
        """, (new_quantity, basket_id, product_id))
    else:
        # ✅ If item doesn't exist, insert a new row
        cursor.execute("""
            INSERT INTO basket_contents (basket_id, product_id, seller_id, quantity, price)
            VALUES (?, ?, ?, ?, ?)
        """, (basket_id, product_id, seller_id, quantity, price))

    conn.commit()  # ✅ Commit the transaction before closing
    conn.close()

    print("\nItem added to your basket successfully!")


def update_basket_item(basket_id, product_id, new_quantity):
    """Update the quantity of a product in the shopper's basket."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE basket_contents
        SET quantity = ?
        WHERE basket_id = ? AND product_id = ?
    """, (new_quantity, basket_id, product_id))

    conn.commit()  # ✅ Ensure changes are saved
    conn.close()

    print("\nItem quantity updated successfully!")
