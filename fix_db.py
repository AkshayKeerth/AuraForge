import sqlite3

def fix():
    try:
        conn = sqlite3.connect('data/user_save.db')
        cursor = conn.cursor()

        print("Attempting to upgrade database...")
        # This adds the missing column to your existing table
        cursor.execute("ALTER TABLE inventory ADD COLUMN username TEXT")

        conn.commit()
        print("Success! The 'username' column has been added.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Database is already up to date!")
        else:
            print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix()
