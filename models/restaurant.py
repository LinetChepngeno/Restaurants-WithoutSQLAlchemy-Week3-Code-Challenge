import sqlite3
from models.review import Review  

conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

class Restaurant:
    def __init__(self, name, price, id=None):
        self.id = id
        self.name = name
        self.price = price

    @classmethod
    def get_by_id(cls, id):
        cursor.execute("SELECT * FROM restaurants WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2])
        return None

    @classmethod
    def create(cls, name, price):
        cursor.execute("INSERT INTO restaurants (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
       # Get the last inserted row id
        last_row_id = cursor.lastrowid

        # Return a new instance of Restaurant with the correct id, name, and price
        return cls(last_row_id, name, price)

    def save(self):
        cursor.execute("UPDATE restaurants SET name = ?, price = ? WHERE id = ?", (self.name, self.price, self.id))
        conn.commit()

    def delete(self):
        cursor.execute("DELETE FROM restaurants WHERE id = ?", (self.id,))
        conn.commit()

    def reviews(self):
        from models.review import Review 
        cursor.execute("SELECT * FROM reviews WHERE restaurant_id = ?", (self.id,))
        return [Review.get_by_id(row[0]) for row in cursor.fetchall()]

    def customers(self):
        #from models.customer import Customer  
        cursor.execute("SELECT DISTINCT customer_id FROM reviews WHERE restaurant_id = ?", (self.id,))
        return [Customer.get_by_id(row[0]) for row in cursor.fetchall()]

    @staticmethod
    def fanciest():
        cursor.execute("SELECT * FROM restaurants ORDER BY price DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            return Restaurant(row[1], row[2])
        return None

    def all_reviews(self):
        # from models.review import Review  
        reviews = self.reviews()
        return [review.full_review() for review in reviews]