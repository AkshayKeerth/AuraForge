# import random

# class GameAPI:
#     def __init__(self, economy, database):
#         self.economy = economy
#         self.db = database

#     def get_user_data(self):
#         """Called when the app loads to show current money/stats"""
#         return {
#             "balance": self.economy.get_current_balance(),
#             "passive_rate": self.economy.passive_rate
#         }

#     def roll_item(self):
#         """The core 'Gacha' mechanic"""
#         roll_cost = 50 # Example cost

#         if not self.economy.spend_money(roll_cost):
#             return {"status": "error", "message": "Not enough fake money!"}

#         # Rarity Logic: 1 in 1000 for Legendary, 1 in 100 for Rare
#         chance = random.randint(1, 1000)

#         if chance == 1:
#             item = {"name": "Omega Brainrot", "rarity": "Legendary", "color": "#ff00ff"}
#         elif chance <= 50:
#             item = {"name": "Rare Aura", "rarity": "Rare", "color": "#00dbff"}
#         else:
#             item = {"name": "Standard Meme", "rarity": "Common", "color": "#ffffff"}

#         self.db.add_to_inventory(item['name'], item['rarity'])
#         return {"status": "success", "item": item, "new_balance": self.economy.get_current_balance()}


import random

class GameAPI:
    def __init__(self, economy, database):
        self.economy = economy
        self.db = database
        self.current_user = None

    # def login(self, username, password):
    #     user = self.db.verify_user(username, password)
    #     if user:
    #         self.current_user = username
    #         self.economy.balance = user[1]
    #         self.economy.passive_rate = user[2]
    #         return {"status": "success", "username": username}
    #     return {"status": "error", "message": "Invalid username or password"}
    def login(self, username, password):
        user = self.db.verify_user(username, password)
        if user:
            self.current_user = username
            # This line is what sends the data to the economy manager
            self.economy.load_user(user)
            return {"status": "success", "username": username}
        return {"status": "error", "message": "Invalid username or password"}

    def signup(self, username, password):
        if not username or not password:
            return {"status": "error", "message": "Fields cannot be empty"}
        if self.db.create_user(username, password):
            return self.login(username, password)
        return {"status": "error", "message": "Username already taken"}

    def get_sync_data(self):
        if not self.current_user:
            return None
        # Periodically save to DB through the economy pulse
        self.db.update_user_stats(self.current_user, self.economy.balance, self.economy.passive_rate)
        return {
            "balance": self.economy.get_current_balance(),
            "username": self.current_user
        }

    def roll_item(self):
        if not self.current_user:
            return {"status": "error", "message": "Not logged in"}

        cost = 50
        if not self.economy.spend_money(cost):
            return {"status": "error", "message": "Insufficient funds!"}

        chance = random.randint(1, 1000)
        if chance == 1:
            item = {"name": "Giga Brainrot", "rarity": "Mythic", "color": "#ff3e3e"}
        elif chance <= 50:
            item = {"name": "Rare Aura", "rarity": "Rare", "color": "#00dbff"}
        else:
            item = {"name": "Common Meme", "rarity": "Common", "color": "#ffffff"}

        self.db.add_to_inventory(self.current_user, item['name'], item['rarity'])
        return {"status": "success", "item": item, "new_balance": self.economy.get_current_balance()}
