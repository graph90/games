from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import random

class GuessNumberGame(App):
    def build(self):
        self.secret_number = random.randint(1, 100)
        layout = BoxLayout(orientation='vertical', spacing=10)

        with layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.8, 1, 0.8, 1)
            self.rect = Rectangle(size=(layout.width, layout.height), pos=layout.pos)

        instructions_label = Label(text="Guess a number between 1 and 100:", font_size=20, color=(0, 0.5, 0, 1))
        layout.add_widget(instructions_label)

        self.guess_input = TextInput(multiline=False, input_type='number', input_filter='int',background_color=(1, 1, 1, 1), foreground_color=(0, 0.5, 0, 1))
        layout.add_widget(self.guess_input)

        submit_button = Button(text="Submit Guess", on_press=self.check_guess,background_color=(1, 1, 0.5, 1), color=(0, 0, 0, 1))
        layout.add_widget(submit_button)

        self.result_label = Label(text="", font_size=18, color=(0, 0, 0.5, 1))
        layout.add_widget(self.result_label)

        return layout

    def check_guess(self, instance):
        try:
            user_guess = int(self.guess_input.text)
            if user_guess == self.secret_number:
                self.result_label.text = "Congratulations! You guessed the correct number."
            elif user_guess < self.secret_number:
                self.result_label.text = "Try a higher number."
            else:
                self.result_label.text = "Try a lower number."
        except ValueError:
            self.result_label.text = "Please enter a valid number."
        finally:
            self.guess_input.text = ""

if __name__ == '__main__':
    GuessNumberGame().run()
