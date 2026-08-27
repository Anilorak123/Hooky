from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from logic.game import YARNS


class YarnScreen(MDScreen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.build_ui()

    def on_pre_enter(self):
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
            height=80
        )
        header_layout = MDBoxLayout(orientation="vertical")
        self.coins_label = MDLabel(
            text=f"Coins: {int(self.game.coins)}",
            font_style="H5",
            theme_text_color="Custom",
            text_color="#FFFFFF",
            halign="center"
        )
        current_yarn_name = next(
            (y["name"] for y in YARNS if y["id"] == self.game.current_yarn), "Acrylic"
        )
        self.yarn_label = MDLabel(
            text=f"Current yarn: {current_yarn_name}",
            font_style="Caption",
            theme_text_color="Custom",
            text_color="#DEC6F0",
            halign="center"
        )
        header_layout.add_widget(self.coins_label)
        header_layout.add_widget(self.yarn_label)
        header.add_widget(header_layout)
        root.add_widget(header)

        title = MDLabel(
            text="Yarn Shop",
            font_style="H6",
            theme_text_color="Custom",
            text_color="#4A235A",
            halign="center",
            size_hint_y=None,
            height=40
        )
        root.add_widget(title)

        scroll = ScrollView()
        items_layout = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None,
            padding=[0, 0, 0, 10]
        )
        items_layout.bind(minimum_height=items_layout.setter("height"))

        for yarn in YARNS:
            is_current = yarn["id"] == self.game.current_yarn
            is_unlocked = yarn["id"] in self.game.unlocked_yarns

            card = MDCard(
                padding=12,
                radius=[12],
                md_bg_color="#EDE0F5" if is_current else "#FFFFFF",
                size_hint_y=None,
                height=100
            )
            row = MDBoxLayout(orientation="horizontal", spacing=10)

            # Kolorowy pasek po lewej
            color_bar = MDCard(
                md_bg_color=yarn["color"],
                size_hint_x=None,
                width=8,
                radius=[8]
            )
            row.add_widget(color_bar)

            info_col = MDBoxLayout(orientation="vertical", spacing=4)
            name_label = MDLabel(
                text=yarn["name"] + (" (active)" if is_current else ""),
                font_style="H6",
                theme_text_color="Custom",
                text_color="#4A235A"
            )
            desc_label = MDLabel(
                text=f"{yarn['description']} • x{yarn['price_multiplier']} price",
                font_style="Caption",
                theme_text_color="Custom",
                text_color="#888888"
            )
            info_col.add_widget(name_label)
            info_col.add_widget(desc_label)

            if is_current:
                btn_text = "Selected"
                btn_color = "#1D9E75"
            elif is_unlocked:
                btn_text = "Select"
                btn_color = "#A05CC7"
            else:
                btn_text = f"Buy\n{yarn['cost']} coins"
                btn_color = "#A05CC7" if self.game.coins >= yarn["cost"] else "#CCCCCC"

            btn = MDRaisedButton(
                text=btn_text,
                md_bg_color=btn_color,
                size_hint_x=None,
                width=120,
                disabled=is_current
            )
            btn.yarn = yarn
            btn.bind(on_press=self.on_buy)

            row.add_widget(info_col)
            row.add_widget(btn)
            card.add_widget(row)
            items_layout.add_widget(card)

        scroll.add_widget(items_layout)
        root.add_widget(scroll)

        back_btn = MDRaisedButton(
            text="Back to game",
            md_bg_color="#1D9E75",
            size_hint_x=1,
            height=50
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "game"))
        root.add_widget(back_btn)

        self.add_widget(root)

    def on_buy(self, btn):
        success, msg = self.game.buy_yarn(btn.yarn)
        if success:
            self.build_ui()
        else:
            btn.text = "Not enough\ncoins!"