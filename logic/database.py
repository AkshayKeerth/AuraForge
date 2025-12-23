# import sqlite3
# import os

# class Database:
#     def __init__(self, db_path="data/user_save.db"):
#         self.db_path = db_path
#         # Ensure the data directory exists
#         os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
#         self.init_db()

#     def init_db(self):
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         # Table for user stats
#         cursor.execute('''CREATE TABLE IF NOT EXISTS stats
#                           (id INTEGER PRIMARY KEY, balance REAL, passive_rate REAL)''')
#         # Table for collected items
#         cursor.execute('''CREATE TABLE IF NOT EXISTS inventory
#                           (id INTEGER PRIMARY KEY, item_name TEXT, rarity TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

#         # Check if first-time user
#         cursor.execute("SELECT COUNT(*) FROM stats")
#         if cursor.fetchone()[0] == 0:
#             cursor.execute("INSERT INTO stats (balance, passive_rate) VALUES (0.0, 1.0)")

#         conn.commit()
#         conn.close()

#     def get_stats(self):
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         cursor.execute("SELECT balance, passive_rate FROM stats WHERE id = 1")
#         result = cursor.fetchone()
#         conn.close()
#         return {"balance": result[0], "passive_rate": result[1]}

#     def save_stats(self, balance, passive_rate):
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         cursor.execute("UPDATE stats SET balance = ?, passive_rate = ? WHERE id = 1", (balance, passive_rate))
#         conn.commit()
#         conn.close()

#     def add_to_inventory(self, name, rarity):
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO inventory (item_name, rarity) VALUES (?, ?)", (name, rarity))
#         conn.commit()
#         conn.close()


import sqlite3
import os

class Database:
    def __init__(self, db_path="data/user_save.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Create users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (username TEXT PRIMARY KEY, password TEXT, balance REAL, passive_rate REAL)''')
        # Create inventory table
        cursor.execute('''CREATE TABLE IF NOT EXISTS inventory
                          (username TEXT, item_name TEXT, rarity TEXT)''')
        conn.commit()
        conn.close()

    def create_user(self, username, password):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users VALUES (?, ?, 0.0, 1.0)", (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False # User already exists
        finally:
            conn.close()

    def verify_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT username, balance, passive_rate FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user # Returns None if not found

    def update_user_stats(self, username, balance, passive_rate):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = ?, passive_rate = ? WHERE username = ?", (balance, passive_rate, username))
        conn.commit()
        conn.close()

    def add_to_inventory(self, username, name, rarity):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (username, item_name, rarity) VALUES (?, ?, ?)", (username, name, rarity))
        conn.commit()
        conn.close()
