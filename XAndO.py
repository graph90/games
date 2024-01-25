from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import random

class TicTacToeGame(App):
    def build(self):
        layout = GridLayout(cols=3, spacing=5)
        self.current_player = 'X'
        self.board = [[''] * 3 for _ in range(3)]
        for row in range(3):
            for col in range(3):
                button = Button(text='', font_size=30, on_press=self.make_move)
                layout.add_widget(button)
        return layout

    def make_move(self, instance):
        row, col = self.get_button_position(instance)
        if self.board[row][col] == '':
            instance.text = self.current_player
            self.board[row][col] = self.current_player
            if self.check_winner() or self.check_draw():
                self.display_result()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.computer_move()

    def computer_move(self):
        empty_spots = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
        if empty_spots:
            row, col = random.choice(empty_spots)
            index = row * 3 + col
            if 0 <= index < len(self.root.children[0].children):
                button = self.root.children[0].children[index]
                if button.text == '':
                    self.make_move(button)

    def get_button_position(self, button):
        index = button.parent.children.index(button)
        row = index // 3
        col = index % 3
        return row, col

    def check_winner(self):
        for i in range(3):
            if (self.board[i][0] == self.board[i][1] == self.board[i][2] == self.current_player or
                self.board[0][i] == self.board[1][i] == self.board[2][i] == self.current_player):
                return True
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] == self.current_player or
            self.board[0][2] == self.board[1][1] == self.board[2][0] == self.current_player):
            return True
        return False

    def check_draw(self):
        return all(self.board[i][j] != '' for i in range(3) for j in range(3))
    def display_result(self):
        if self.check_winner():
            result = f"Player {self.current_player} wins!"
        else:
            result = "It's a draw!"
        popup = Popup(title="Game Over", content=Label(text=result), size_hint=(None, None), size=(400, 200))
        popup.open()
        
if __name__ == '__main__':
    TicTacToeGame().run()
