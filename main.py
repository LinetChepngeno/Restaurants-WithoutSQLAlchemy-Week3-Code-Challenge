from models.restaurant import Restaurant
from models.customer import Customer
from models.review import Review
from database import conn, cursor

def main():
    # Create some sample data
    restaurant1 = Restaurant.create("Sarova Stanley", 20)
    restaurant2 = Restaurant.create("Pride in", 30)

    customer1 = Customer.create("Daisy", "Chebet")
    customer2 = Customer.create("Leah", "Mokeira")

    
    # Assume customer1 and restaurant1 are instances of Customer and Restaurant classes respectively
    customer_id = customer1.id
    restaurant_id = restaurant1.id

    # Check if customer_id and restaurant_id are not None before creating the review
    if customer_id is not None and restaurant_id is not None:
        Review.create(5, customer_id, restaurant_id)
    else:
        print("Error: Customer ID or Restaurant ID is None")

    # Review.create(4, customer2.id, restaurant1.id)
    # Review.create(3, customer1.id, restaurant1.id)

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

    customer=Customer.get_by_id(1)
    print(customer.full_name())

    review=Review.get_by_id(1)
    print(review.full_review())



    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()