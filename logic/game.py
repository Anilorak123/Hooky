import time
import json
import os

class GameState:
    def __init__(self):
        self.coins = 0
        self.item_in_progress = None
        self.craft_start_time = None
        self.inventory = []

    # --- SZYDEŁKOWANIE ---
    def start_crafting(self, item):
        if self.item_in_progress is not None:
            return "Już coś robisz!"
        self.item_in_progress = item
        self.craft_start_time = time.time()
        return f"Zaczęłaś robić: {item['name']}"

    def check_crafting(self):
        if self.item_in_progress is None:
            return None
        elapsed = time.time() - self.craft_start_time
        if elapsed >= self.item_in_progress["time"]:
            finished = self.item_in_progress
            self.inventory.append(finished)
            self.item_in_progress = None
            self.craft_start_time = None
            return f"{finished['name']} gotowe! Trafia do ekwipunku."
        remaining = self.item_in_progress["time"] - elapsed
        return f"Zostało: {int(remaining)}s"

    # --- SPRZEDAŻ ---
    def sell_item(self, item_name):
        for item in self.inventory:
            if item["name"] == item_name:
                self.inventory.remove(item)
                self.coins += item["price"]
                return f"Sprzedano {item['name']} za {item['price']} monet!"
        return "Nie masz tego przedmiotu."

    # --- ZAPIS ---
    def save(self):
        data = {
            "coins": self.coins,
            "inventory": self.inventory,
        }
        os.makedirs("saves", exist_ok=True)
        with open("saves/save.json", "w") as f:
            json.dump(data, f)

    def load(self):
        if os.path.exists("saves/save.json"):
            with open("saves/save.json") as f:
                data = json.load(f)
            self.coins = data.get("coins", 0)
            self.inventory = data.get("inventory", [])