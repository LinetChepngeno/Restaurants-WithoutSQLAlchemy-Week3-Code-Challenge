from restaurant import Restaurant
from customer import Customer
from review import Review

# Create the tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT
    )
""")

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

# Create some sample data
restaurant1 = Restaurant.create("Sarova Stanley", 20)
restaurant2 = Restaurant.create("Pride Inn", 30)

customer1 = Customer.create("Leah", "Mokeira")
customer2 = Customer.create("Daisy", "Chebet")

customer1.add_review(restaurant1, 4)
customer1.add_review(restaurant2, 3)
customer2.add_review(restaurant1, 5)

# Test methods
print("Restaurant reviews:")
for review in restaurant1.reviews():
    print(review.full_review())

print("\nCustomer reviews:")
for review in customer1.reviews():
    print(review.full_review())

print("\nFanciest restaurant:")
fanciest = Restaurant.fanciest()
print(fanciest.name, fanciest.price)
