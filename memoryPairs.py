from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import random

class MemoryPuzzleGame(App):
    def __init__(self, **kwargs):
        super(MemoryPuzzleGame, self).__init__(**kwargs)
        self.symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] * 2
        random.shuffle(self.symbols)
        self.selected_cards = []
        self.matched_pairs = []

    def build(self):
        layout = GridLayout(cols=4, spacing=5)
        self.buttons = [Button(text='', font_size=30, on_press=self.flip_card) for _ in range(16)]
        for button in self.buttons:
            layout.add_widget(button)
        return layout

    def flip_card(self, instance):
        index = self.buttons.index(instance)
        if index in self.selected_cards or index in self.matched_pairs:
            return
        instance.text = self.symbols[index]
        self.selected_cards.append(index)
        if len(self.selected_cards) == 2:
            self.check_match()
    def check_match(self):
        index1, index2 = self.selected_cards
        if self.symbols[index1] == self.symbols[index2]:
            self.matched_pairs.extend(self.selected_cards)
            self.buttons[index1].disabled = True
            self.buttons[index2].disabled = True
        else:
            self.buttons[index1].text = ''
            self.buttons[index2].text = ''
        self.selected_cards = []
        if len(self.matched_pairs) == len(self.symbols):
            self.display_result()

    def display_result(self):
        result = "Congratulations! You found all pairs."
        popup = Popup(title="Game Over", content=Label(text=result), size_hint=(None, None), size=(400, 200))
        popup.open()
if __name__ == '__main__':
    MemoryPuzzleGame().run()