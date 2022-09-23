import sys
from tkinter import *
import random
import ctypes
import sys
from PIL import Image, ImageTk

size = 20
bombs_count = 75
sys.setrecursionlimit(10000)


class Cells():
    all = []
    cell_count = size**2-bombs_count
    bomb_count = bombs_count
    cell_count_label = None
    bomb_count_label = None

    def __init__(self, x, y, is_bomb=False):
        self.is_bomb = is_bomb
        self.is_opened = False
        self.is_flagged = False
        self.cell_button_object = None
        self.x = x
        self.y = y
        self.bombs_around = 0
        Cells.all.append(self)

    def left_click(self, event):
        if self.is_bomb:
            self.cell_button_object.configure(bg="red") #not working
            ctypes.windll.user32.MessageBoxW(0, "You clicked on a mine", "Game Over", 0)
            sys.exit()
        else:
            self.show_cell()
            if self.show_cell() == "":
                for cell_obj in self.surrounded_cells():
                    cell_obj.show_cell()
                    cell_obj.cell_button_object.unbind("<Button-3>")
        self.cell_button_object.unbind("<Button-3>")

    def right_click(self, event):

        if self.is_flagged:
            self.is_flagged = False
            self.cell_button_object.configure(bg="SystemButtonFace", image="")
            self.cell_button_object.bind("<Button-1>", self.left_click)
            Cells.bomb_count += 1
            if Cells.bomb_count_label:
                Cells.bomb_count_label.configure(text=f"Bombs left:{Cells.bomb_count}")

        elif not self.is_flagged:
            self.is_flagged = True
            self.cell_button_object.configure(bg='orange')
            self.cell_button_object.unbind("<Button-1>")
            Cells.bomb_count -= 1
            if Cells.bomb_count_label:
                Cells.bomb_count_label.configure(text=f"Bombs left:{Cells.bomb_count}")

    def create_button_object(self, location):
        button = Button(location, text="", width=int(100/size), height=int(50/size))
        button.bind("<Button-1>", self.left_click)
        button.bind("<Button-3>", self.right_click)
        self.cell_button_object = button

    def create_cell_count(self):
        label = Label(self, text=f"Cells left:{Cells.cell_count}", width=16,
                      height=8, bg="black", fg="white", font=("consolas", 18))
        Cells.cell_count_label = label

    def create_bomb_count(self):
        label = Label(self, text=f"Bombs left:{Cells.bomb_count}", width=16,
                      height=8, bg="black", fg="white", font=("consolas", 18))
        Cells.bomb_count_label = label

    def randomize_bombs():
        bomb_cells = random.sample(Cells.all, bombs_count)
        for bomb_cell in bomb_cells:
            bomb_cell.is_bomb = True

    def get_cell(self, x, y):
        for cell in Cells.all:
            if cell.x == x and cell.y == y:
                return cell

    def surrounded_cells(self):
        cells_around = [self.get_cell(self.x - 1, self.y - 1),
                        self.get_cell(self.x - 1, self.y),
                        self.get_cell(self.x - 1, self.y + 1),
                        self.get_cell(self.x, self.y - 1),
                        self.get_cell(self.x, self.y + 1),
                        self.get_cell(self.x + 1, self.y - 1),
                        self.get_cell(self.x + 1, self.y),
                        self.get_cell(self.x + 1, self.y + 1)]
        cells = [cell for cell in cells_around if cell is not None]
        return cells

    def bomb_counter(self):
        for cell in self.surrounded_cells():
            if cell.is_bomb:
                self.bombs_around += 1
        return self.bombs_around

    def show_cell(self):
        self.bombs_around = 0

        if not self.is_opened:
            Cells.cell_count -= 1
        self.bomb_counter()
        self.is_opened = True

        if self.bombs_around == 0:
            self.bombs_around = ""
            for empty_cell in self.surrounded_cells():
                if empty_cell.bombs_around == 0:
                    empty_cell.show_cell()
                    empty_cell.cell_button_object.unbind("<Button-3>")

        if Cells.cell_count_label:
            Cells.cell_count_label.configure(text=f"Cells left:{Cells.cell_count}")

        if Cells.cell_count == 0:
            Cells.cell_count_label.configure(text=f"Cells left:{Cells.cell_count}\n"
                                                  f"YOU WIN!!!")
            ctypes.windll.user32.MessageBoxW(0, "Congratulations :)", "You win!", 0)

        self.cell_button_object.configure(text=str(self.bombs_around), bg="white")
        return self.bombs_around

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"


WIDTH = 1200
HEIGHT = 1000
window = Tk()
window.geometry(f"{WIDTH}x{HEIGHT}")
window.title("Saper")
window.config(bg="#FFE0BC")

top_frame = Frame(window, bg="#460000", width=WIDTH, height=100)
top_frame.place(x=200, y=0)

game_title = Label(top_frame, bg="#460000", fg="white", text=" Minesweeper Game", font=("consolas", 40))
game_title.grid(row=0, column=3)
game_board = Frame(window)


score_frame = Frame(window, bg="#FF7A2F", width=200, height=(HEIGHT-100))
score_frame.place(x=0, y=120)

for row in range(size):
    for column in range(size):
        button = Cells(row, column)
        button.create_button_object(game_board)
        button.cell_button_object.grid(row=row, column=column)

game_board.place(x=200, y=120)

Cells.create_cell_count(score_frame)
Cells.create_bomb_count(score_frame)
Cells.cell_count_label.place(x=0, y=0)
Cells.bomb_count_label.place(x=0, y=200)

Cells.randomize_bombs()

window.mainloop()