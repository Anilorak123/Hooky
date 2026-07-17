from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView


UPGRADES = [
    {
        "id": "faster_hands",
        "name": "Faster Hands",
        "description": "You craft twice as fast",
        "cost": 100,
        "multiplier": 0.5,  # multiplies crafting time by 0.5
    },
    {
        "id": "better_yarn",
        "name": "Better Yarn",
        "description": "Items are worth 50% more",
        "cost": 200,
        "price_bonus": 0.5,
    },
    {
        "id": "second_hook",
        "name": "Second Hook",
        "description": "You can craft two items at a time",
        "cost": 500,
        "extra_slot": True,
    },
]


class UpgradesScreen(MDScreen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        root = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12,
            md_bg_color="#F5EEF8"
        )

        # Nagłówek
        header = MDCard(
            padding=16,
            radius=[16],
            md_bg_color="#7B4FA6",
            size_hint_y=None,
            height=70
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

        title = MDLabel(
            text="Workshop Upgrades",
            font_style="H6",
            theme_text_color="Custom",
            text_color="#4A235A",
            halign="center",
            size_hint_y=None,
            height=40
        )
        root.add_widget(title)

        # Lista ulepszeń
        scroll = ScrollView()
        items_layout = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None,
            padding=[0, 0, 0, 10]
        )
        items_layout.bind(minimum_height=items_layout.setter("height"))

        for upgrade in UPGRADES:
            card = MDCard(
                padding=12,
                radius=[12],
                md_bg_color="#FFFFFF",
                size_hint_y=None,
                height=100
            )
            row = MDBoxLayout(orientation="horizontal", spacing=10)
            info_col = MDBoxLayout(orientation="vertical", spacing=4)

            name_label = MDLabel(
                text=upgrade["name"],
                font_style="H6",
                theme_text_color="Custom",
                text_color="#4A235A"
            )
            desc_label = MDLabel(
                text=upgrade["description"],
                font_style="Caption",
                theme_text_color="Custom",
                text_color="#888888"
            )

            already_bought = upgrade["id"] in self.game.upgrades

            btn = MDRaisedButton(
                text="Purchased" if already_bought else f"{upgrade['cost']} coins",
                md_bg_color="#AAAAAA" if already_bought else "#A05CC7",
                size_hint_x=None,
                width=150,
                disabled=already_bought
            )
            btn.upgrade = upgrade
            btn.bind(on_press=self.on_buy)

            info_col.add_widget(name_label)
            info_col.add_widget(desc_label)
            row.add_widget(info_col)
            row.add_widget(btn)
            card.add_widget(row)
            items_layout.add_widget(card)

        scroll.add_widget(items_layout)
        root.add_widget(scroll)

        # Przycisk powrotu
        back_btn = MDRaisedButton(
            text="Back to Game",
            md_bg_color="#1D9E75",
            size_hint_x=1,
            height=50
        )
        back_btn.bind(on_press=self.go_back)
        root.add_widget(back_btn)

        self.add_widget(root)

    def on_buy(self, btn):
        upgrade = btn.upgrade
        if self.game.coins >= upgrade["cost"]:
            self.game.coins -= upgrade["cost"]
            self.game.upgrades.add(upgrade["id"])
            self.game.apply_upgrade(upgrade)
            self.game.save()
            self.build_ui()  # odśwież ekran
        else:
            btn.text = "Not enough coins!"

    def go_back(self, btn):
        self.manager.current = "game"