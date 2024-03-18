import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

def create_tables():
    """
    Create the necessary tables in the database if they don't exist.
    """
    # Create the restaurants table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price INTEGER
        )
    """)

    # Create the customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT
        )
    """)

    # Create the reviews table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            star_rating INTEGER,
            restaurant_id INTEGER,
            customer_id INTEGER,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)

    conn.commit()

# Call the create_tables function to create the tables when the module is imported
create_tables()