import time
import json
import os

WORKERS = [
    {
        "id": "beanie_worker",
        "name": "Beanie Crocheter",
        "description": "Automatically makes beanies",
        "coins_per_second": 2,
        "cost": 500,
        "emoji": "🧶"
    },
    {
        "id": "scarf_worker",
        "name": "Scarf Crocheter",
        "description": "Automatically makes scarves",
        "coins_per_second": 5,
        "cost": 1500,
        "emoji": "🧣"
    },
    {
        "id": "socks_worker",
        "name": "Socks Crocheter",
        "description": "Automatically makes socks",
        "coins_per_second": 10,
        "cost": 4000,
        "emoji": "🧦"
    },
    {
        "id": "amigurumi_artist",
        "name": "Amigurumi Artist",
        "description": "Makes cute plushies",
        "coins_per_second": 25,
        "cost": 12000,
        "emoji": "🐻"
    },
    {
        "id": "workshop_manager",
        "name": "Workshop Manager",
        "description": "Manages the whole workshop",
        "coins_per_second": 75,
        "cost": 40000,
        "emoji": "👩"
    },
]


class GameState:
    def __init__(self):
        self.coins = 0
        self.item_in_progress = None
        self.craft_start_time = None
        self.inventory = []
        self.upgrades = set()
        self.workers = {}  # id -> count
        self.time_multiplier = 1.0
        self.price_multiplier = 1.0

    def coins_per_second(self):
        total = 0
        for worker in WORKERS:
            count = self.workers.get(worker["id"], 0)
            total += worker["coins_per_second"] * count
        return total

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

    def buy_worker(self, worker):
        cost = self.worker_cost(worker)
        if self.coins >= cost:
            self.coins -= cost
            self.workers[worker["id"]] = self.workers.get(worker["id"], 0) + 1
            self.save()
            return True
        return False

    def worker_cost(self, worker):
        count = self.workers.get(worker["id"], 0)
        # każdy kolejny pracownik kosztuje 15% więcej
        return int(worker["cost"] * (1.15 ** count))

    def calculate_offline_earnings(self):
        if not os.path.exists("saves/save.json"):
            return 0, 0
        try:
            with open("saves/save.json") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return 0, 0
        close_time = data.get("close_time", None)
        if close_time is None:
            return 0, 0
        seconds_away = time.time() - close_time
        seconds_away = min(seconds_away, 8 * 3600)
        earnings = int(seconds_away * self.coins_per_second())
        return earnings, int(seconds_away)

    def save(self):
        data = {
            "coins": self.coins,
            "inventory": self.inventory,
            "upgrades": list(self.upgrades),
            "workers": self.workers,
            "time_multiplier": self.time_multiplier,
            "price_multiplier": self.price_multiplier,
            "close_time": time.time()
        }
        os.makedirs("saves", exist_ok=True)
        with open("saves/save.json", "w") as f:
            json.dump(data, f)

    def load(self):
        if os.path.exists("saves/save.json"):
            try:
                with open("saves/save.json") as f:
                    data = json.load(f)
                self.coins = data.get("coins", 0)
                self.inventory = data.get("inventory", [])
                self.upgrades = set(data.get("upgrades", []))
                self.workers = data.get("workers", {})
                self.time_multiplier = data.get("time_multiplier", 1.0)
                self.price_multiplier = data.get("price_multiplier", 1.0)
            except json.JSONDecodeError:
                print("Save file corrupted, starting fresh!")