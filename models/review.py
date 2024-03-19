import sqlite3

conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

class Review:
    def __init__(self, star_rating, restaurant_id, customer_id, id=None):
        self.id = id
        self.star_rating = star_rating
        self.restaurant_id = restaurant_id
        self.customer_id = customer_id

    @classmethod
    def create(cls, star_rating, restaurant_id, customer_id):
        # Execute SQL query
        cursor.execute("INSERT INTO reviews (star_rating, restaurant_id, customer_id) VALUES (?, ?, ?)", (star_rating, restaurant_id, customer_id))
        conn.commit()

        # Get the last inserted row id
        last_row_id = cursor.lastrowid

        # Return a new instance of Review with the correct id, star_rating, customer_id, and restaurant_id
        return cls(last_row_id, star_rating, restaurant_id, customer_id)

    @classmethod
    def get_by_id(cls, id):
        cursor.execute("SELECT * FROM reviews WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return cls(row[0], row[1], row[2], row[3])
        return None

    def customer(self):
        from models.customer import Customer  # Avoid circular import
        return Customer.get_by_id(self.customer_id)

    def restaurant(self):
        from models.restaurant import Restaurant  # Avoid circular import
        return Restaurant.get_by_id(self.restaurant_id)

    def full_review(self):
        customer = self.customer()
        restaurant = self.restaurant()
        return f"Review for {restaurant.name} by {customer.full_name()}: {self.star_rating} stars."