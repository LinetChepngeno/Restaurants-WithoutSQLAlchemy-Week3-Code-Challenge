from restaurant import Restaurant
from customer import Customer
from review import Review
from database import conn, cursor

def main():
    # Create some sample data
    restaurant1 = Restaurant.create("Pizza Place", 20)
    restaurant2 = Restaurant.create("Sushi Bar", 30)

    customer1 = Customer.create("John", "Doe")
    customer2 = Customer.create("Jane", "Smith")

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

    # ... Add more test cases as needed

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()