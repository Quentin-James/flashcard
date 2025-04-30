from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import MDSnackbar
from kivy.core.window import Window
from kivy.metrics import dp
import json
import random
import os

# Set window size and background color
Window.size = (400, 700)
Window.clearcolor = (0.1, 0.1, 0.1, 1)

class FlashCardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cards = self.load_cards()
        self.index = 0
        self.showing_answer = False
        self.form_visible = False
        self.current_category = "Toutes"
        self.categories = self.get_categories()

        # Layout principal avec padding augmenté
        self.layout = MDBoxLayout(orientation='vertical', spacing=30, padding=(20, 40))

        # Titre de l'application
        self.title = MDLabel(
            text="Flashcards",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.2, 0.7, 0.7, 1),
            font_style="H3",
            font_size='34sp',
            size_hint_y=None,
            height=dp(50)
        )

        # Widgets principaux
        self.label = MDLabel(
            text="Chargement...",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            font_size='24sp'
        )

        self.counter_label = MDLabel(
            text="Carte 0 / 0",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.7, 0.7, 0.7, 1),
            font_style="Body1",
            size_hint_y=None,
            height=dp(30)
        )

        # Style commun pour les boutons
        button_style = {
            'size_hint': (None, None),
            'size': (300, 50),
            'background_normal': '',
            'pos_hint': {"center_x": 0.5},
            'font_size': '18sp'
        }

        # Create buttons with enhanced style
        self.button = Button(
            text="Afficher la réponse",
            background_color=(0.2, 0.7, 0.7, 1),
            **button_style
        )
        self.button.bind(on_release=self.toggle_card)

        self.next_button = Button(
            text="Carte suivante",
            background_color=(0.2, 0.6, 0.6, 1),
            **button_style
        )
        self.next_button.bind(on_release=self.next_card)

        self.prev_button = Button(
            text="Carte précédente",
            background_color=(0.2, 0.6, 0.6, 1),
            **button_style
        )
        self.prev_button.bind(on_release=self.prev_card)

        self.shuffle_button = Button(
            text="Mélanger les cartes",
            background_color=(0.2, 0.5, 0.5, 1),
            **button_style
        )
        self.shuffle_button.bind(on_release=self.shuffle_cards)

        self.add_button = Button(
            text="Ajouter une carte",
            background_color=(0.3, 0.6, 0.3, 1),
            **button_style
        )
        self.add_button.bind(on_release=self.toggle_form)

        # Formulaire amélioré
        self.question_input = MDTextField(
            hint_text="Question",
            mode="rectangle",
            multiline=True,
            size_hint_y=None,
            height=dp(100)
        )
        self.answer_input = MDTextField(
            hint_text="Réponse",
            mode="rectangle",
            multiline=True,
            size_hint_y=None,
            height=dp(100)
        )
        self.category_input = MDTextField(
            hint_text="Catégorie (optionnel)",
            mode="rectangle",
            size_hint_y=None,
            height=dp(50)
        )
        self.save_button = Button(
            text="Enregistrer la carte",
            background_color=(0.3, 0.6, 0.3, 1),
            **button_style
        )
        self.save_button.bind(on_release=self.save_card)

        self.form_widgets = [
            self.question_input,
            self.answer_input,
            self.category_input,
            self.save_button
        ]

        # Ajout des widgets
        self.layout.add_widget(self.title)
        self.layout.add_widget(self.counter_label)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.prev_button)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.shuffle_button)
        self.layout.add_widget(self.add_button)

        self.add_widget(self.layout)

        if self.cards:
            self.show_card()
        else:
            self.label.text = "Aucune carte disponible."

    def get_categories(self):
        categories = set()
        for card in self.cards:
            if "category" in card:
                categories.add(card["category"])
        return list(categories)

    def load_cards(self):
        path = "flashcards.json"
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []

    def save_cards_to_file(self):
        with open("flashcards.json", "w", encoding="utf-8") as f:
            json.dump(self.cards, f, indent=4, ensure_ascii=False)

    def show_card(self):
        if not self.cards:
            self.label.text = "Aucune carte disponible."
            self.counter_label.text = "Carte 0 / 0"
            return

        self.showing_answer = False
        card = self.cards[self.index]
        self.label.text = card["question"]
        self.button.text = "Afficher la réponse"
        
        # Afficher la catégorie si elle existe
        category_text = f" - {card.get('category', 'Sans catégorie')}"
        self.counter_label.text = f"Carte {self.index + 1} / {len(self.cards)}{category_text}"

    def toggle_card(self, instance):
        if not self.cards:
            return
        card = self.cards[self.index]
        if self.showing_answer:
            self.label.text = card["question"]
            self.button.text = "Afficher la réponse"
        else:
            self.label.text = card["answer"]
            self.button.text = "Afficher la question"
        self.showing_answer = not self.showing_answer

    def next_card(self, instance):
        if not self.cards:
            return
        self.index = (self.index + 1) % len(self.cards)
        self.show_card()

    def prev_card(self, instance):
        if not self.cards:
            return
        self.index = (self.index - 1) % len(self.cards)
        self.show_card()

    def shuffle_cards(self, instance):
        if not self.cards:
            return
        random.shuffle(self.cards)
        self.index = 0
        snackbar = MDSnackbar()
        snackbar.snackbar_x = 10
        snackbar.snackbar_y = 10
        snackbar.size_hint_x = 0.9
        snackbar.buttons = [
            MDLabel(
                text="Cartes mélangées !",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        ]
        snackbar.open()
        self.show_card()

    def toggle_form(self, instance):
        if not self.form_visible:
            for widget in self.form_widgets:
                self.layout.add_widget(widget)
            self.form_visible = True
            self.add_button.text = "Fermer le formulaire"
        else:
            for widget in self.form_widgets:
                self.layout.remove_widget(widget)
            self.form_visible = False
            self.add_button.text = "Ajouter une carte"

    def save_card(self, instance):
        question = self.question_input.text.strip()
        answer = self.answer_input.text.strip()
        category = self.category_input.text.strip()

        if question and answer:
            new_card = {
                "question": question,
                "answer": answer
            }
            if category:
                new_card["category"] = category
                if category not in self.categories:
                    self.categories.append(category)

            self.cards.append(new_card)
            self.save_cards_to_file()
            
            self.question_input.text = ""
            self.answer_input.text = ""
            self.category_input.text = ""
            
            snackbar = MDSnackbar()
            snackbar.snackbar_x = 10
            snackbar.snackbar_y = 10
            snackbar.size_hint_x = 0.9
            snackbar.buttons = [
                MDLabel(
                    text="Carte ajoutée !",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1)
                )
            ]
            snackbar.open()
            
            self.index = len(self.cards) - 1
            self.show_card()
        else:
            snackbar = MDSnackbar()
            snackbar.snackbar_x = 10
            snackbar.snackbar_y = 10
            snackbar.size_hint_x = 0.9
            snackbar.buttons = [
                MDLabel(
                    text="Remplis au moins la question et la réponse.",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1)
                )
            ]
            snackbar.open()

class FlashCardApp(MDApp):
    def build(self):
        self.title = "Flashcards App"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        return FlashCardScreen()

if __name__ == "__main__":
    FlashCardApp().run()
