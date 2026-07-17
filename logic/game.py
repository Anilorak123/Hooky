import time
import json
import os


class GameState:
    def __init__(self):
        self.coins = 0
        self.item_in_progress = None
        self.craft_start_time = None
        self.inventory = []
        self.upgrades = set()
        self.time_multiplier = 1.0   # im mniejszy tym szybciej
        self.price_multiplier = 1.0  # im większy tym drożej
        self.extra_slot = False

    def start_crafting(self, item):
        if self.item_in_progress is not None:
            return "Already crafting something!"
        self.item_in_progress = item
        self.craft_start_time = time.time()
        return f"Started crafting: {item['name']}"

    def check_crafting(self):
        if self.item_in_progress is None:
            return None
        actual_time = self.item_in_progress["time"] * self.time_multiplier
        elapsed = time.time() - self.craft_start_time
        if elapsed >= actual_time:
            finished = self.item_in_progress
            self.inventory.append(finished)
            self.item_in_progress = None
            self.craft_start_time = None
            return f"{finished['name']} ready!"
        remaining = actual_time - elapsed
        return f"Remaining: {int(remaining)}s"

    def sell_item(self, item_name):
        for item in self.inventory:
            if item["name"] == item_name:
                self.inventory.remove(item)
                price = int(item["price"] * self.price_multiplier)
                self.coins += price
                return f"Sold {item['name']} for {price} coins!"
        return "You don't have that item."

    def apply_upgrade(self, upgrade):
        if "multiplier" in upgrade:
            self.time_multiplier *= upgrade["multiplier"]
        if "price_bonus" in upgrade:
            self.price_multiplier += upgrade["price_bonus"]
        if upgrade.get("extra_slot"):
            self.extra_slot = True

    def save(self):
        data = {
            "coins": self.coins,
            "inventory": self.inventory,
            "upgrades": list(self.upgrades),
            "time_multiplier": self.time_multiplier,
            "price_multiplier": self.price_multiplier,
            "extra_slot": self.extra_slot,
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
            self.upgrades = set(data.get("upgrades", []))
            self.time_multiplier = data.get("time_multiplier", 1.0)
            self.price_multiplier = data.get("price_multiplier", 1.0)
            self.extra_slot = data.get("extra_slot", False)