import sqlite3

conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

class Customer:
    def __init__(self, first_name, last_name, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def get_by_id(cls, id):
        cursor.execute("SELECT * FROM customers WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2])
        return None

    @classmethod
    def create(cls, first_name, last_name):
        cursor.execute("INSERT INTO customers (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
        conn.commit()
        return cls(first_name, last_name)

    def save(self):
        cursor.execute("UPDATE customers SET first_name = ?, last_name = ? WHERE id = ?", (self.first_name, self.last_name, self.id))
        conn.commit()

    def delete(self):
        cursor.execute("DELETE FROM customers WHERE id = ?", (self.id,))
        conn.commit()

    def reviews(self):
        from models.review import Review  # Avoid circular import
        cursor.execute("SELECT * FROM reviews WHERE customer_id = ?", (self.id,))
        return [Review.get_by_id(row[0]) for row in cursor.fetchall()]

    def restaurants(self):
        from models.restaurant import Restaurant  # Avoid circular import
        cursor.execute("SELECT DISTINCT restaurant_id FROM reviews WHERE customer_id = ?", (self.id,))
        return [Restaurant.get_by_id(row[0]) for row in cursor.fetchall()]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
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
            from models.restaurant import Restaurant  # Avoid circular import
            return Restaurant.get_by_id(row[0])
        return None

    def add_review(self, restaurant, rating):
        from models.review import Review  # Avoid circular import
        new_review=Review.create(rating, restaurant.id, self.id,)
        return new_review
        

    def delete_reviews(self, restaurant):
        cursor.execute("DELETE FROM reviews WHERE customer_id = ? AND restaurant_id = ?", (self.id, restaurant.id))
        conn.commit()