from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
import json
import random

class FlashCardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cards = self.load_cards()
        self.index = 0
        self.showing_answer = False

        self.layout = MDBoxLayout(orientation='vertical', spacing=20, padding=40)
        self.label = MDLabel(text="Flashcard", halign="center", theme_text_color="Custom", text_color=(1,1,1,1), font_style="H5")
        self.button = MDRaisedButton(text="Afficher la réponse", pos_hint={"center_x": 0.5}, on_release=self.toggle_card)
        self.next_button = MDRaisedButton(text="Carte suivante", pos_hint={"center_x": 0.5}, on_release=self.next_card)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.next_button)
        self.add_widget(self.layout)

        self.show_card()

    def load_cards(self):
        with open("flashcards.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def show_card(self):
        self.showing_answer = False
        self.label.text = self.cards[self.index]["question"]
        self.button.text = "Afficher la réponse"

    def toggle_card(self, instance):
        if self.showing_answer:
            self.label.text = self.cards[self.index]["question"]
            self.button.text = "Afficher la réponse"
        else:
            self.label.text = self.cards[self.index]["answer"]
            self.button.text = "Afficher la question"
        self.showing_answer = not self.showing_answer

    def next_card(self, instance):
        self.index = (self.index + 1) % len(self.cards)
        self.show_card()

class FlashCardApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return FlashCardScreen()

if __name__ == "__main__":
    FlashCardApp().run()
