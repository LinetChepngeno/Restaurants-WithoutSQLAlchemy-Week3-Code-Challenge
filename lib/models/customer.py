from .models import conn, cursor

class Customer:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def get_by_id(cls, id):
        # Query the database to retrieve a customer by their id
        cursor.execute("SELECT * FROM customers WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            # If a row is found, create and return a Customer instance
            return cls(row[1], row[2])
        return None

    @classmethod
    def create(cls, first_name, last_name):
        # Insert a new customer into the database
        cursor.execute("INSERT INTO customers (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
        conn.commit()
        return cls(first_name, last_name)

    def save(self):
        # Update an existing customer in the database
        cursor.execute("UPDATE customers SET first_name = ?, last_name = ? WHERE id = ?", (self.first_name, self.last_name, self.id))
        conn.commit()

    def delete(self):
        # Delete a customer from the database
        cursor.execute("DELETE FROM customers WHERE id = ?", (self.id,))
        conn.commit()

    def reviews(self):
        from .review import Review  # Corrected import statement
        # Retrieve all reviews left by the current customer
        cursor.execute("SELECT * FROM reviews WHERE customer_id = ?", (self.id,))
        return [Review.get_by_id(row[0]) for row in cursor.fetchall()]

    def restaurants(self):
        from .restaurant import Restaurant  # Corrected import statement
        # Retrieve all restaurants reviewed by the current customer
        cursor.execute("SELECT DISTINCT restaurant_id FROM reviews WHERE customer_id = ?", (self.id,))
        return [Restaurant.get_by_id(row[0]) for row in cursor.fetchall()]

    def full_name(self):
        # Return the full name of the customer
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        # Retrieve the restaurant with the highest star rating for the current customer
        cursor.execute("""
            SELECT restaurant_id, MAX(star_rating) AS max_rating
            FROM reviews
            WHERE customer_id = ?
            GROUP BY restaurant_id
            ORDER BY max_rating DESC
            LIMIT 1
        """, (self.id,))
        row = cursor.fetchone()
        if row:
            from .restaurant import Restaurant  # Corrected import statement
            return Restaurant.get_by_id(row[0])
        return None

    def add_review(self, restaurant, rating):
        from .review import Review  # Corrected import statement
        # Insert a new review for the current customer and restaurant
        cursor.execute("INSERT INTO reviews (star_rating, restaurant_id, customer_id) VALUES (?, ?, ?)", (rating, restaurant.id, self.id))
        conn.commit()

    def delete_reviews(self, restaurant):
        # Delete all reviews left by the current customer for the given restaurant
        cursor.execute("DELETE FROM reviews WHERE customer_id = ? AND restaurant_id = ?", (self.id, restaurant.id))
        conn.commit()
