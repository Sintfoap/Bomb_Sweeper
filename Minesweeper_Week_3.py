from tkinter import *
from PIL import Image , ImageTk
# from tkinter.ttk import *
from functools import partial
import random
import os

class location:
    def __init__(self):
        self.bomb = False
        self.flag = False
        self.row = 0
        self.col = 0
        self.bomb_count = 0
        self.clicked = False
        self.button = None
        self.icon = ''
        # self.revealed = False

        # self.button = Button(window, text='X', width=3) .grid(row=0, column=0)

## MINE MAP
class map:
    def __init__(self):
        self.width = 30
        self.height = 16

        self.the_map = []
    
    def build_map(self):
        for row in range(self.height):
            my_row = []
            for col in range(self.width):
                loc = location()
                loc.row = row
                loc.col = col

                if random_number(8) == 3:
                    loc.bomb = True
                my_row.append(loc)
            self.the_map.append(my_row)
        self.build_bomb_count()

    def build_bomb_count(self):
        for row in range(self.height):
          for col in range(self.width):
            #check for boundaries
            num_bombs = 0
            for loc in [(1,0), (1,1), (0,1), (-1,0), (-1,-1), (-1, 1), (1,-1), (0,-1)]:
                row_change = loc[0]
                col_change = loc[1]
                working_row = row + row_change
                working_col = col + col_change
                if working_row >= 0 and working_row < self.height and working_col >= 0 and working_col < self.width:
                    if self.the_map[working_row][working_col].bomb:
                        num_bombs += 1
            self.the_map[row][col].bomb_count = num_bombs

            # if row > 0:
            #   go_ = True
            # if row < self.height:
    
    def print_map(self):
        for row in self.the_map:
            for loc in row:
                icon = ' '
                # if loc.bomb == True:
                #     icon = 'X'
                loc.button = create_button(loc, icon)

def create_button(loc, my_text):
    button = Button(window, 
        text=my_text, 
        width=2,
        height=1,
        font=("Courier Bold", 18))
    button.grid(row=loc.row, column=loc.col)
    # button.bind("<Button-1>", partial(left_click, loc, button))
    button.bind("<Button-3>", partial(right_click, loc))
    button.configure(command = partial(left_click, loc, button))
    return button

number_colors = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'red',
    4: 'purple',
    5: 'maroon',
    6: 'teal',
    7: 'black',
    8: 'grey'
}

## key down function
def left_click(loc, button):
    # if loc flagged, ignore
    if loc.flag or loc.clicked:
        return
    # if is a mine, blow up
    if loc.bomb:
        close_window()
    # else change icon to num_bombs
    # button = event.widget
    loc.icon = loc.bomb_count
    button.config(text=loc.icon, fg=number_colors[loc.bomb_count])
    loc.clicked = True

    if loc.bomb_count == 0:
        button.config(text='', relief=SUNKEN, bg="#cec8c7")
        for neighbor in [(1,0), (1,1), (0,1), (-1,0), (-1,-1), (-1, 1), (1,-1), (0,-1)]:
                row_change = neighbor[0]
                col_change = neighbor[1]
                working_row = loc.row + row_change
                working_col = loc.col + col_change
                if working_row >= 0 and working_row < map1.height and working_col >= 0 and working_col < map1.width:
                    map1.the_map[working_row][working_col].button.invoke()
                    # print("Clicked " + str(working_row) + ", " + str(working_col))


def right_click(loc, event):
    button = event.widget

    # swap to/from flagged
    if loc.clicked == False:
    # else:
        loc.flag = not loc.flag


    # rerenders
    if loc.flag:
        # loc.icon = '?'
        image1 = Image.open("bomb_sm.png")
        photoimage = ImageTk.PhotoImage(image1)
        button.config(image = photoimage)
        button.pack
    else:
        if loc.clicked:
            if loc.bomb_count > 0:
                loc.icon = str(loc.bomb_count)
            else:
                loc.icon = ' '
        else:
            loc.icon = ''
    
    button.config(text=loc.icon)


    # loc.icon = '?' if loc.flag else str(loc.bomb_count)
 
 
    # if loc.flag:
    #     photo=PhotoImage(file="minesweeper.png")
    #     photoimage = photo
    #     button.image = photoimage
    #     button.config(image=photoimage)
    # else:
    #     button.config(image='')

    # photoimage = photo.subsample(1, 7)
    

def close_window():
    window.destroy()
    exit()

def random_number(limit):
    return random.randint(0, limit)

window = Tk()
window.title("My Minesweeper")
# window.configure(background='black')

map1 = map()
map1.build_map()
map1.print_map()

## exit button
Button(window, text='Exit', width=6, command=close_window) .grid(row=17, column=0, columnspan=2, sticky=W)


window.mainloop()