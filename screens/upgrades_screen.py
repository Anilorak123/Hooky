from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from logic.game import WORKERS


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
        header_layout = MDBoxLayout(orientation="vertical")
        self.coins_label = MDLabel(
            text=f"Coins: {self.game.coins}",
            font_style="H5",
            theme_text_color="Custom",
            text_color="#FFFFFF",
            halign="center"
        )
        self.cps_label = MDLabel(
            text=f"{self.game.coins_per_second()} coins/sec",
            font_style="Caption",
            theme_text_color="Custom",
            text_color="#DEC6F0",
            halign="center"
        )
        header_layout.add_widget(self.coins_label)
        header_layout.add_widget(self.cps_label)
        header.add_widget(header_layout)
        root.add_widget(header)

        title = MDLabel(
            text="Hire Workers",
            font_style="H6",
            theme_text_color="Custom",
            text_color="#4A235A",
            halign="center",
            size_hint_y=None,
            height=40
        )
        root.add_widget(title)

        # Lista pracowników
        scroll = ScrollView()
        items_layout = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None,
            padding=[0, 0, 0, 10]
        )
        items_layout.bind(minimum_height=items_layout.setter("height"))

        for worker in WORKERS:
            card = MDCard(
                padding=12,
                radius=[12],
                md_bg_color="#FFFFFF",
                size_hint_y=None,
                height=100
            )
            row = MDBoxLayout(orientation="horizontal", spacing=10)
            info_col = MDBoxLayout(orientation="vertical", spacing=4)

            count = self.game.workers.get(worker["id"], 0)
            cost = self.game.worker_cost(worker)
            can_afford = self.game.coins >= cost

            name_label = MDLabel(
                text=f"{worker['name']}  x{count}",
                font_style="H6",
                theme_text_color="Custom",
                text_color="#4A235A"
            )
            desc_label = MDLabel(
                text=f"{worker['description']} • {worker['coins_per_second']} coins/sec each",
                font_style="Caption",
                theme_text_color="Custom",
                text_color="#888888"
            )

            btn = MDRaisedButton(
                text=f"Hire\n{cost} coins",
                md_bg_color="#A05CC7" if can_afford else "#CCCCCC",
                size_hint_x=None,
                width=120
            )
            btn.worker = worker
            btn.bind(on_press=self.on_hire)

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
            text="Back to game",
            md_bg_color="#1D9E75",
            size_hint_x=1,
            height=50
        )
        back_btn.bind(on_press=self.go_back)
        root.add_widget(back_btn)

        self.add_widget(root)

    def on_hire(self, btn):
        success = self.game.buy_worker(btn.worker)
        if success:
            self.build_ui()
        else:
            btn.text = "Not enough\ncoins!"
    
    def on_pre_enter(self):
        """Called every time you enter the screen"""
        self.build_ui()

    def go_back(self, btn):
        self.manager.current = "game"