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


YARNS = [
    {
        "id": "acrylic",
        "name": "Acrylic",
        "description": "Basic yarn, good for beginners",
        "price_multiplier": 1.0,
        "cost": 0,
        "color": "#A8A8A8"
    },
    {
        "id": "cotton",
        "name": "Cotton",
        "description": "Soft and breathable",
        "price_multiplier": 1.5,
        "cost": 300,
        "color": "#F5CBA7"
    },
    {
        "id": "wool",
        "name": "Wool",
        "description": "Warm and cozy",
        "price_multiplier": 2.5,
        "cost": 1000,
        "color": "#C39BD3"
    },
    {
        "id": "alpaca",
        "name": "Alpaca",
        "description": "Incredibly soft luxury yarn",
        "price_multiplier": 4.0,
        "cost": 5000,
        "color": "#85C1E9"
    },
    {
        "id": "silk",
        "name": "Silk Blend",
        "description": "The finest yarn available",
        "price_multiplier": 8.0,
        "cost": 20000,
        "color": "#F9E79F"
    },
]

LEVELS = [
    {"level": 1, "xp_required": 0, "reward": None, "title": "Beginner Crocheter"},
    {"level": 2, "xp_required": 100, "reward": {"coins": 50}, "title": "Yarn Enthusiast"},
    {"level": 3, "xp_required": 300, "reward": {"coins": 150}, "title": "Hook Master"},
    {"level": 4, "xp_required": 600, "reward": {"coins": 400}, "title": "Craft Artist"},
    {"level": 5, "xp_required": 1000, "reward": {"coins": 800}, "title": "Wool Wizard"},
    {"level": 6, "xp_required": 2000, "reward": {"coins": 2000}, "title": "Amigurumi Expert"},
    {"level": 7, "xp_required": 4000, "reward": {"coins": 5000}, "title": "Crochet Entrepreneur"},
    {"level": 8, "xp_required": 8000, "reward": {"coins": 12000}, "title": "Yarn Tycoon"},
    {"level": 9, "xp_required": 15000, "reward": {"coins": 30000}, "title": "Crochet Legend"},
    {"level": 10, "xp_required": 30000, "reward": {"coins": 100000}, "title": "Grand Master"},
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
        self.current_yarn = "acrylic"
        self.unlocked_yarns = {"acrylic"}
        self.xp = 0
        self.level = 1
        self.level_up_message = None

    def coins_per_second(self):
        total = 0
        for worker in WORKERS:
            count = self.workers.get(worker["id"], 0)
            total += worker["coins_per_second"] * count
        return int(total * self.get_yarn_multiplier())

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
                price = int(item["price"] * self.price_multiplier * self.get_yarn_multiplier())
                self.coins += price
                self.add_xp(item["price"] // 10)  # XP = 10% of base price
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

    def buy_yarn(self, yarn):
        if yarn["id"] in self.unlocked_yarns:
            self.current_yarn = yarn["id"]
            return True, "Switched to " + yarn["name"] + "!"
        if self.coins >= yarn["cost"]:
            self.coins -= yarn["cost"]
            self.unlocked_yarns.add(yarn["id"])
            self.current_yarn = yarn["id"]
            self.save()
            return True, yarn["name"] + " unlocked!"
        return False, "Not enough coins!"

    def get_yarn_multiplier(self):
        for yarn in YARNS:
            if yarn["id"] == self.current_yarn:
                return yarn["price_multiplier"]
        return 1.0

    def add_xp(self, amount):
        self.xp += amount
        # Check if leveled up
        for level_data in LEVELS:
            if level_data["level"] == self.level + 1:
                if self.xp >= level_data["xp_required"]:
                    self.level += 1
                    if level_data["reward"]:
                        self.coins += level_data["reward"]["coins"]
                    self.level_up_message = (
                        f"Level up! You are now level {self.level}!\n"
                        f"{level_data['title']}\n"
                        f"Reward: {level_data['reward']['coins']} coins!"
                        if level_data["reward"]
                        else f"Level up! You are now level {self.level}!\n{level_data['title']}"
                    )
                    return True
        return False

    def get_current_level_data(self):
        for level_data in LEVELS:
            if level_data["level"] == self.level:
                return level_data
        return LEVELS[-1]

    def get_next_level_data(self):
        for level_data in LEVELS:
            if level_data["level"] == self.level + 1:
                return level_data
        return None

    def xp_progress(self):
        current = self.get_current_level_data()
        next_level = self.get_next_level_data()
        if next_level is None:
            return 1.0
        current_xp = self.xp - current["xp_required"]
        needed_xp = next_level["xp_required"] - current["xp_required"]
        return min(current_xp / needed_xp, 1.0)

    def save(self):
        data = {
            "coins": self.coins,
            "inventory": self.inventory,
            "upgrades": list(self.upgrades),
            "workers": self.workers,
            "time_multiplier": self.time_multiplier,
            "price_multiplier": self.price_multiplier,
            "close_time": time.time(),
            "current_yarn": self.current_yarn,
            "unlocked_yarns": list(self.unlocked_yarns),
            "xp": self.xp,
            "level": self.level,
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
                self.current_yarn = data.get("current_yarn", "acrylic")
                self.unlocked_yarns = set(data.get("unlocked_yarns", ["acrylic"]))
                self.xp = data.get("xp", 0)
                self.level = data.get("level", 1)
            except json.JSONDecodeError:
                print("Save file corrupted, starting fresh!")