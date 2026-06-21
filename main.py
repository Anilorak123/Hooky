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
from logic.game import GameState
from screens.title_screen import TitleScreen

with open("data/items.json", encoding="utf-8") as f:
    ITEMS = json.load(f)

class GameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = GameState()
        self.game.load()

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
            text=f"Monety: {self.game.coins}",
            font_style="H5",
            theme_text_color="Custom",
            text_color="#FFFFFF",
            halign="center"
        )
        header.add_widget(self.coins_label)
        root.add_widget(header)

        self.status_label = MDLabel(
            text="Wybierz co chcesz zrobic:",
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
                text=f"Czas: {item['time']}s   |   Cena: {item['price']} monet",
                theme_text_color="Custom",
                text_color="#888888",
                font_style="Caption"
            )
            btn = MDRaisedButton(
                text="Szydelkuj",
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
            text="Ekwipunek: pusty",
            theme_text_color="Custom",
            text_color="#4A235A",
            halign="center"
        )
        inv_card.add_widget(self.inventory_label)
        root.add_widget(inv_card)

        sell_btn = MDRaisedButton(
            text="Sprzedaj wszystko",
            md_bg_color="#1D9E75",
            size_hint_x=1,
            height=50
        )
        sell_btn.bind(on_press=self.on_sell_all)
        root.add_widget(sell_btn)

        self.add_widget(root)
        Clock.schedule_interval(self.update, 1)

    def on_craft(self, btn):
        msg = self.game.start_crafting(btn.item)
        self.status_label.text = msg

    def on_sell_all(self, btn):
        if not self.game.inventory:
            self.status_label.text = "Ekwipunek jest pusty!"
            return
        total = 0
        for item in list(self.game.inventory):
            self.game.sell_item(item["name"])
            total += item["price"]
        self.status_label.text = f"Sprzedano wszystko za {total} monet!"
        self.game.save()

    def update(self, dt):
        msg = self.game.check_crafting()
        if msg:
            self.status_label.text = msg
        self.coins_label.text = f"Monety: {self.game.coins}"
        inv = [i["name"] for i in self.game.inventory]
        self.inventory_label.text = "Ekwipunek: " + (", ".join(inv) if inv else "pusty")


class HookeyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()
        sm.add_widget(TitleScreen(name="title"))
        sm.add_widget(GameScreen(name="game"))
        return sm


if __name__ == "__main__":
    HookeyApp().run()