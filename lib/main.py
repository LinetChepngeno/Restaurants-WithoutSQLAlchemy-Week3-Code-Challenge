#!/usr/bin/env python3
from lib.models.database import conn, cursor
from models.customer import Customer
from models.restaurant import Restaurant
from models.review import Review

def main():
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


    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()