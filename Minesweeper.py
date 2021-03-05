from tkinter import *
from tkinter import messagebox, simpledialog
from functools import partial
import random
import os
import datetime

class location:
    def __init__(self):
        self.bomb = False
        self.flag = False
        self.row = 0
        self.col = 0
        self.bomb_count = 0
        self.clicked = False
        self.button = None

## MINE MAP
class map:
    def __init__(self):
        # self.width = 30
        # self.height = 16
        self.width = 0
        self.height = 0
        self.completed = True

        self.the_map = []
        self.num_bombs = 0
        self.num_squares_flagged = 0
        self.num_squares_clicked = 0
    
    def build_map(self):
        for row in range(self.height):
            my_row = []
            for col in range(self.width):
                loc = location()
                loc.row = row
                loc.col = col

                if random_number(8) == 3:
                    loc.bomb = True
                    self.num_bombs += 1
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

    def print_map(self):
        print("the_map rows in print map: " + str(len(self.the_map)))
        for row in self.the_map:
            for loc in row:
                icon = ' '
                loc.button = create_button(loc, icon)
        mines_label.config(text=str(map1.num_bombs - map1.num_squares_flagged))

    def complete(self):
        print("CURRENT CLICKED:", self.num_squares_clicked)
        print("MINES:", self.num_bombs)
        return (self.height * self.width) - self.num_bombs == self.num_squares_clicked

    def clear(self):
        self.width = 0
        self.height = 0
        self.the_map.clear()
        # print(self.the_map)
        self.num_bombs = 0
        self.num_squares_flagged = 0
        self.num_squares_clicked = 0

    def num_squares(self):
        return self.height * self.width



def create_button(loc, my_text):
    button = Button(game_frame, 
        text=my_text, 
        width=2,
        height=1,
        font=("Courier Bold", 18))
    button.grid(row=loc.row, column=loc.col)
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

# Example highscore file:
# 13,austin
# 23,scott
# 10000000000,ryan

def ordinal(n):
    return "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])


def end_game():
    max_highscores = 5
    if map1.completed:
        return
    print("HURRAY!")
    timer1.timing = False
    map1.completed = True
    total_time = timer1.timer_text
    user_name = simpledialog.askstring("Input", "What is your name?")
    if not os.path.isdir('./highscores'):
        os.mkdir('./highscores')
    filename = "{}x{}_highscores.txt".format(map1.width, map1.height)
    current_highscore_list = []
    if os.path.isfile('./highscores/{}'.format(filename)):
        file = open('./highscores/{}'.format(filename),mode='r')
        current_highscores_file = file.read()
        file.close()
        current_highscores_file = current_highscores_file.split('\n')
        for entry in current_highscores_file:
            if entry != '':
                entry = entry.split(',')
                entry[0] = int(entry[0])
                current_highscore_list.append(entry)
    user_place = -1
    for i in range(len(current_highscore_list)):
        item = current_highscore_list[i]
        if total_time < item[0]:
            user_place = i
            break
    else:
        if len(current_highscore_list) < max_highscores:
            user_place = len(current_highscore_list)
    if user_place >= 0:
        messagebox.showinfo(title="YOU WIN!", message="{} you have completed this {} x {} BombSweeper game in a time of {} and placed {} on the highscore list!".format(user_name, map1.width, map1.height, datetime.timedelta(seconds=timer1.timer_text), ordinal(user_place + 1)))
        current_highscore_list.insert(user_place, [total_time,user_name])
        current_highscore_list = current_highscore_list[:max_highscores]
        file = open('./highscores/{}'.format(filename),mode='w')
        lines = []
        for item in current_highscore_list:
            item[0] = str(item[0])
            lines.append(",".join(item))
        file.write('\n'.join(lines))
        file.close()
    else:
        messagebox.showinfo(title="YOU WIN!", message="{} you have completed this {} x {} BombSweeper game in a time of {}!".format(user_name, map1.width, map1.height, datetime.timedelta(seconds=timer1.timer_text)))



## key down function
def left_click(loc, button):
    # if loc flagged, ignore
    if loc.flag or loc.clicked:
        print(str(loc.row) + '- ' + str(loc.col) + ' Already Clicked!')
        return
    # if is a mine, blow up
    if loc.bomb:
        close_window()
    # else change icon to num_bombs
    loc.icon = loc.bomb_count
    button.config(text=loc.icon, fg=number_colors[loc.bomb_count])
    loc.clicked = True
    map1.num_squares_clicked += 1

    if loc.bomb_count == 0:
        button.config(text='', relief=SUNKEN, bg="#cec8c7")
        for neighbor in [(1,0), (1,1), (0,1), (-1,0), (-1,-1), (-1, 1), (1,-1), (0,-1)]:
                row_change = neighbor[0]
                col_change = neighbor[1]
                working_row = loc.row + row_change
                working_col = loc.col + col_change
                if working_row >= 0 and working_row < map1.height and working_col >= 0 and working_col < map1.width:
                    map1.the_map[working_row][working_col].button.invoke()
    if map1.complete():
        end_game()

def right_click(loc, event):
    button = event.widget
    print ('loc.clicked: ' + str(loc.clicked))
    # swap to/from flagged
    if loc.clicked == False:
        if loc.flag:
            loc.flag = False
            map1.num_squares_flagged -= 1
        else:
            loc.flag = True
            map1.num_squares_flagged += 1
        

    # rerenders
    button = event.widget
    if loc.flag:
        loc.icon = '?'
    else:
        if loc.clicked:
            if loc.bomb_count > 0:
                loc.icon = str(loc.bomb_count)
            else:
                loc.icon = ' '
        else:
            loc.icon = ''
    if loc.icon == '?':
        button.config(image=flag)
        button.config(width=32)
        button.config(height=41)
    else:
        button.config(image='')
        button.config(width=2)
        button.config(height=1)
    mines_label.config(text=str(map1.num_bombs - map1.num_squares_flagged))

   
def close_window():
    window.destroy()
    exit()

def random_number(limit):
    return random.randint(0, limit)

def integer_check(entry_number, input_type):
    integer = 0
    try:
        integer = int(entry_number)
    except ValueError:
        messagebox.showerror(title="YOU STINK!", message="Sorry - you must enter an integer for the {0}!".format(input_type))
        return None
    else:
        if integer >= 5:
            return integer
        else:
            messagebox.showerror(title="YOU STINK!", message="Sorry - the {} must be 5 or greater".format(input_type))
            return None

class timer:
    def __init__(self):
        self.timer_text = 0
        self.timing = True

    def update_timer(self):
        if self.timing == False:
            return
        else:
            self.timer_text += 1
            timer_label['text']=self.timer_text
            top_frame.after(1000, self.update_timer)

def submit():
    global timer1
    width = integer_check(entry_W.get(), 'Width')
    if width is None:
        return
    height = integer_check(entry_H.get(), 'Height')
    if height is None:
        return
    map1.clear()
    # Murder loop
    for widget in game_frame.winfo_children():
        widget.destroy()
    map1.width = width
    map1.height = height

    map1.build_map()
    map1.print_map()
    map1.completed = False

    #top_frame.after_cancel(timer1.after_function)
    timer1.timing = False
    timer1 = timer()
    timer1.update_timer()

window = Tk()
Titlebar_Icon =PhotoImage(file ="Minesweeper_Icon.png")
window.iconphoto(False, Titlebar_Icon)
window.resizable(width=False, height=False)

timer1 = timer()

# create all of the main containers
top_frame = Frame(window, bg='orange', width=450, height=50, pady=3)
game_frame = Frame(window, bg='gray2', width=450, height=450, padx=3, pady=3)

top_frame.grid(row=0, sticky='ew')
game_frame.grid(row=1, sticky='nsew')

# create the widgets for the top frame
# map_label = Label(top_frame, text='Minesweeper Map Dimensions')
width_label = Label(top_frame, text='Width: ')
length_label = Label(top_frame, text='Height: ')
entry_W = Entry(top_frame, width=15)
entry_H = Entry(top_frame, width=15)
submit = Button(top_frame, text='Submit', command=submit)
timer_label = Label(top_frame, text=timer1.timer_text)

# layout the widgets in the top frame
# map_label.grid(row=0, columnspan=3)
width_label.grid(row=0, column=0, padx=3, pady=3)
length_label.grid(row=0, column=2, padx=3, pady=3)
entry_W.grid(row=0, column=1, padx=3, pady=3)
entry_H.grid(row=0, column=3, padx=3, pady=3)
submit.grid(row=0, column=4, padx=15, pady=3)
timer_label.grid(row=0, column=5, padx=3, pady=3)

flag = PhotoImage(file = "flag.png")
flag = flag.subsample(25,28)
window.title("My Minesweeper")

map1 = map()

## exit button
Button(window, text='Exit', width=6, command=close_window) .grid(row=17, column=0, columnspan=2, sticky=W)
## Current Mines Label
mines_label = Label(window, text=map1.num_bombs, width=3, borderwidth=3, relief="groove")
mines_label.grid(row=17, column=2, columnspan=2, sticky=W)


window.mainloop()
