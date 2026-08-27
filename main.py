import json
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from sympy import root
from logic.game import GameState
from screens.title_screen import TitleScreen
from screens.upgrades_screen import UpgradesScreen


with open("data/items.json", encoding="utf-8") as f:
    ITEMS = json.load(f)

class GameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = GameState()
        self.game.load()

        # Check for offline earnings
        earnings, seconds = self.game.calculate_offline_earnings()
        if earnings > 0:
            self.game.coins += earnings
            self.game.save()
            self._offline_earnings_msg = None


        root = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12,
            md_bg_color="#F5EEF8"
        )

        header = MDCard(
            padding=16,
            radius=[16],
            md_bg_color="#7B4FA6",
            size_hint_y=None,
            height=80
        )
        self.coins_label = MDLabel(
            text=f"Coins: {self.game.coins}",
            font_style="H5",
            theme_text_color="Custom",
            text_color="#FFFFFF",
            halign="center"
        )
        header.add_widget(self.coins_label)
        root.add_widget(header)

        self.cps_label = MDLabel(
            text="0 coins/sec",
            font_style="Caption",
            theme_text_color="Custom",
            text_color="#4A235A",
            halign="center",
            size_hint_y=None,
            height=25
        )
        root.add_widget(self.cps_label)

        self.status_label = MDLabel(
            text="Choose what to make:",
            halign="center",
            theme_text_color="Custom",
            text_color="#4A235A",
            size_hint_y=None,
            height=40
        )
        root.add_widget(self.status_label)

        scroll = ScrollView()
        items_layout = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None,
            padding=[0, 0, 0, 10]
        )
        items_layout.bind(minimum_height=items_layout.setter("height"))

        for item in ITEMS:
            card = MDCard(
                padding=12,
                radius=[12],
                md_bg_color="#FFFFFF",
                size_hint_y=None,
                height=90
            )
            row = MDBoxLayout(orientation="horizontal", spacing=10)
            info_col = MDBoxLayout(orientation="vertical")

            name_label = MDLabel(
                text=item["name"],
                font_style="H6",
                theme_text_color="Custom",
                text_color="#4A235A"
            )
            info_label = MDLabel(
                text=f"Time: {item['time']}s   |   Price: {item['price']} coins",
                theme_text_color="Custom",
                text_color="#888888",
                font_style="Caption"
            )
            btn = MDRaisedButton(
                text="Crochet",
                md_bg_color="#A05CC7",
                size_hint_x=None,
                width=140
            )
            btn.item = item
            btn.bind(on_press=self.on_craft)

            info_col.add_widget(name_label)
            info_col.add_widget(info_label)
            row.add_widget(info_col)
            row.add_widget(btn)
            card.add_widget(row)
            items_layout.add_widget(card)

        scroll.add_widget(items_layout)
        root.add_widget(scroll)

        inv_card = MDCard(
            padding=12,
            radius=[12],
            md_bg_color="#EDE0F5",
            size_hint_y=None,
            height=60
        )
        self.inventory_label = MDLabel(
            text="Inventory: empty",
            theme_text_color="Custom",
            text_color="#4A235A",
            halign="center"
        )
        inv_card.add_widget(self.inventory_label)
        root.add_widget(inv_card)

        sell_btn = MDRaisedButton(
            text="Sell All",
            md_bg_color="#1D9E75",
            size_hint_x=1,
            height=50
        )
        sell_btn.bind(on_press=self.on_sell_all)
        root.add_widget(sell_btn)

        upgrades_btn = MDRaisedButton(
            text="Upgrades",
            md_bg_color="#7B4FA6",
            size_hint_x=1,
            height=50
        )
        upgrades_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'upgrades'))
        root.add_widget(upgrades_btn)

        self.add_widget(root)
        Clock.schedule_interval(self.update, 1)

    def on_craft(self, btn):
        msg = self.game.start_crafting(btn.item)
        self.status_label.text = msg

    def on_sell_all(self, btn):
        if not self.game.inventory:
            self.status_label.text = "Inventory is empty!"
            return
        total = 0
        for item in list(self.game.inventory):
            self.game.sell_item(item["name"])
            total += item["price"]
        self.status_label.text = f"Sold everything for {total} coins!"
        self.game.save()

    def update(self, dt):
        msg = self.game.check_crafting()
        if msg:
            self.status_label.text = msg
        self.coins_label.text = f"Coins: {self.game.coins}"
        inv = [i["name"] for i in self.game.inventory]
        self.inventory_label.text = "Inventory: " + (", ".join(inv) if inv else "empty")
        # Show offline earnings message if applicable
        if hasattr(self, '_offline_earnings_msg') and self._offline_earnings_msg:
            self.status_label.text = self._offline_earnings_msg
            self._offline_earnings_msg = None  # Reset after showing once
        cps = self.game.coins_per_second()
        self.game.coins += cps
        self.cps_label.text = f"{cps} coins/sec"

class HookyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()
        sm.add_widget(TitleScreen(name="title"))
        sm.add_widget(GameScreen(name="game"))
        game_screen = GameScreen(name="game")
        sm.add_widget(TitleScreen(name="title"))
        sm.add_widget(game_screen)
        sm.add_widget(UpgradesScreen(game=game_screen.game, name="upgrades"))
        return sm
    
    def on_stop(self):
        # Save the game state when the app is closed
        game_screen = self.root.get_screen("game")
        game_screen.game.save_close_time()


if __name__ == "__main__":
    HookyApp().run()