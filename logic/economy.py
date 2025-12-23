import threading
import time

class EconomyManager:
    def __init__(self, database):
        self.db = database
        self.balance = 0.0
        self.passive_rate = 0.0
        self.running = True
        self.current_user = None

        # Start the background thread for passive income
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

    def load_user(self, user_data):
        """Called by API when a user successfully logs in"""
        # user_data format from DB: (username, balance, passive_rate)
        self.current_user = user_data[0]
        self.balance = user_data[1]
        self.passive_rate = user_data[2]

    def _update_loop(self):
        while self.running:
            time.sleep(1) # Tick every second
            if self.current_user:
                self.balance += self.passive_rate

                # Optional: Save to DB every 30 seconds to be safe
                if int(self.balance) % 30 == 0:
                    self.db.update_user_stats(self.current_user, self.balance, self.passive_rate)

    def get_current_balance(self):
        return round(self.balance, 2)

    def add_money(self, amount):
        self.balance += amount

    def spend_money(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False
