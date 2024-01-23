# Section 3 Final by Ben Klein, Anh Le, and Yutong Zhang 
#NOTE: the program needs two folders: 'bugs' and 'bug attributes' to display images
# the folder 'bugs' needs images labeled as such: Name.jpeg (Ant.jpeg)
# the folder 'bug attributes' needs images labeled as such: Attribute.jpeg (antennas.jpeg)

#
from tkinter import *
from tkinter.messagebox import showerror
from PIL import ImageTk, Image 
import re
from os.path import exists


# GUESSING GAME SET UP

# open file
with  open('insects.txt') as f:test = f.read()     

f.close()

test = re.split("[:\n]", test)

# make string from file
text = []

for a in test:

    if a != '':

        text.append(a)

# make dictionary from file string
insects = {}

i = 0

while i < len(text):

    if i % 2 == 0:
        a = text[i+1].split(',')
        insects[text[i]] = a

    i += 1

# function to sort the count characteristics
def Count_Chara_Num(DIC):

    c = []
    c_num = {}

    for x in DIC.values():
        for a in x:
            c.append(a)

    c_set = set(c)
    c1 = list(c_set)
    i = 0

    while i < len(c_set):
        c_num[c1[i]] = c.count(c1[i])
        i += 1

    c_num = sorted(c_num.items(), key=lambda x: x[1], reverse=True)

    return c_num

# list of attributes with corresponding amounts
sorted_atts = Count_Chara_Num(insects)

# accuracy lists 
insect_values = []
key_list = list(insects.keys())
for ins in key_list:
    insect_values.append([ins,10])

def find_mostlikely():
    largest_value = 0
    value_index = 0
    for i in range(0,len(insect_values)):
        if insect_values[i][1] > largest_value:
            largest_value = insect_values[i][1]
            value_index = i
    return (value_index)

def find_2ndmostlikely():
    insect_values2 = insect_values.copy()
    del insect_values2[find_mostlikely()]
    largest_value = 0
    value_index = 0
    for i in range(0,len(insect_values2)):
        if insect_values2[i][1] > largest_value:
            largest_value = insect_values2[i][1]
            value_index = i
    
    value_index_final = insect_values.index(insect_values2[value_index])
    return (value_index_final)

# loop stuff
atts_index = 0
guessing = False

# TKINTER GUI SETUP

# root window
root = Tk()
root.title('Insectinator')

w = 683
h = 384
ws = root.winfo_screenwidth() 
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.resizable(False, False)
window_width = 683
window_height = 384

# question label
att = sorted_atts[atts_index][0]
text_label = Label(root, text="Does your bug have the following attribute: " + str(att))
text_label.place(x = 250, y = 0)


# QUESTION UPDATE AFTER BUTTON PRESSED function
def question_update(val):

    # check for guesses and win
    global guessing

    if guessing == True: # win
        if val == 1 or val == 3:
            text_label.config(text="I win! :D")
            destroy_buttons()
            return False
        else: # guess again
            make_guess()
            return False

    # attribute to ask about
    global atts_index
    att = sorted_atts[atts_index][0]
    
    # save answer by changing insect values accordingly
    for i in range(0,len(insect_values)):
        temp_key = insect_values[i][0]
        if att in insects[temp_key]:
            insect_values[i][1] += val
        #else: # penalize (each question holds more weight)
           #insect_values[i][1] += -val
    
    # update question
    atts_index += 1
    att = str(sorted_atts[atts_index][0])
    att = att.strip()
    text_label.config(text="Does your bug have the following attribute: " + att)

    # update image (if needed)
    global img_temp, image1, image_label
    image_label.configure(image="")
    path = 'bug attributes/'+att+'.jpeg'
    if exists(path):
        img_temp = Image.open(path)
        img_temp = img_temp.resize((300,200))

        image1 = ImageTk.PhotoImage(img_temp)
        image_label.configure(image=image1)
        
    # finish game and guess
    if ((insect_values[find_mostlikely()][1] >= 15) and ((insect_values[find_mostlikely()][1] - insect_values[find_2ndmostlikely()][1]) >= 3)) or \
    (atts_index == len(sorted_atts)-1):
        guessing = True
        make_guess()


# GUESS THE INSECT function
def make_guess():
    global img_temp, image1, image_label

    # lose if completely out of guesses
    if len(insect_values) == 0:
        destroy_buttons()
        image_label.destroy()
        text_label.config(text="I lose D:")
        return False

    # change text and adjust list 
    index = find_mostlikely()
    bug = str(insect_values[index][0])
    text_label.config(text="Are you thinking of " + bug + "?")
    del insect_values[index]

    # image update
    bug = bug.capitalize()

    img_temp = Image.open('bugs/'+bug+'.jpeg')
    img_temp = img_temp.resize((300,200))

    image1 = ImageTk.PhotoImage(img_temp)
    image_label.configure(image=image1)


# Button setup
def button1():
    question_update(1)
def button2():
    question_update(-1)
def button3():
    question_update(0.5)
def button4():
    question_update(-0.5)
def button5():
    question_update(0)
def button6():
    global guessing
    guessing = True
    make_guess()

yes_button = Button(root, text=' Yes ')
yes_button.place(x = 300, y = 40, anchor = NW)
yes_button.configure(command=button1)
no_button = Button(root, text=' No ')
no_button.place(x = 350, y = 40, anchor = NW)
no_button.configure(command=button2)
prob_button = Button(root, text='Probably')
prob_button.place(x = 270, y = 80, anchor = NW)
prob_button.configure(command=button3)
probno_button = Button(root, text='Probably Not')
probno_button.place(x = 350, y = 80, anchor = NW)
probno_button.configure(command=button4)
dknow_button = Button(root, text="Don't Know")
dknow_button.place(x = 300, y = 120, anchor = NW)
dknow_button.configure(command=button5)
mguess_button = Button(root, text="Make Guess")
mguess_button.place(x = 550, y = 320, anchor = NW)
mguess_button.configure(command=button6)

def destroy_buttons():
    yes_button.destroy()
    no_button.destroy()
    prob_button.destroy()
    probno_button.destroy()
    dknow_button.destroy()

# Image setup
img_temp = Image.open('bug attributes/antennas.jpeg')
img_temp = img_temp.resize((300,200))

image1 = ImageTk.PhotoImage(img_temp)
image_label = Label(image=image1)
image_label.place(x = 200, y = 150)


# START APP AND LOOP
root.mainloop()

