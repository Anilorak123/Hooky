from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.graphics import Color, Ellipse


class TitleScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = MDBoxLayout(
            orientation="vertical",
            padding=40,
            spacing=20,
            md_bg_color="#F5EEF8"
        )

        # Górna przestrzeń
        root.add_widget(MDBoxLayout(size_hint_y=0.1))

        # Karta z tytułem
        title_card = MDCard(
            padding=30,
            radius=[24],
            md_bg_color="#7B4FA6",
            size_hint_y=None,
            height=200
        )
        title_layout = MDBoxLayout(orientation="vertical", spacing=8)

        yarn_label = MDLabel(
            text="🧶",
            font_size="64sp",
            halign="center",
            size_hint_y=None,
            height=80
        )
        title_label = MDLabel(
            text="Hookey",
            font_style="H3",
            theme_text_color="Custom",
            text_color="#FFFFFF",
            halign="center",
            bold=True
        )
        subtitle_label = MDLabel(
            text="Cozy Crochet Idle Game",
            font_style="Caption",
            theme_text_color="Custom",
            text_color="#DEC6F0",
            halign="center"
        )

        title_layout.add_widget(yarn_label)
        title_layout.add_widget(title_label)
        title_layout.add_widget(subtitle_label)
        title_card.add_widget(title_layout)
        root.add_widget(title_card)

        # Środkowa przestrzeń
        root.add_widget(MDBoxLayout(size_hint_y=0.15))

        # Opis
        desc_label = MDLabel(
            text="Rozwijaj swój biznes rękodzielniczy,\njeden ścieg na raz!",
            halign="center",
            theme_text_color="Custom",
            text_color="#4A235A",
            font_style="Subtitle1"
        )
        root.add_widget(desc_label)

        root.add_widget(MDBoxLayout(size_hint_y=0.1))

        # Przycisk Start
        start_btn = MDRaisedButton(
            text="Zagraj",
            md_bg_color="#A05CC7",
            size_hint_x=1,
            height=60,
            font_size="18sp"
        )
        start_btn.bind(on_press=self.go_to_game)
        root.add_widget(start_btn)

        # Dolna przestrzeń
        root.add_widget(MDBoxLayout(size_hint_y=0.1))

        # Wersja
        version_label = MDLabel(
            text="v0.1 — made with 🧶 and Python",
            halign="center",
            theme_text_color="Custom",
            text_color="#AAAAAA",
            font_style="Caption"
        )
        root.add_widget(version_label)

        self.add_widget(root)

    def go_to_game(self, btn):
        self.manager.current = "game"