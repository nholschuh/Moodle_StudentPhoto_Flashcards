#!/usr/bin/python

from tkinter import *
import sys
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
BACKGROUND_COLOR = "#FFFFFF"
timer = None

if len(sys.argv) == 1:
    course_name = 'Amherst Course Photos'
else:
    course_name = sys.argv[1]
    
# ---------------------------- CONTENT SETUP ------------------------------- #
#fetch the words in a dict format to make key:value pair
df = pandas.read_csv("Moodle_DataFrame.csv")
word_dictionary = df.to_dict(orient='records')

current_card = {}

def checked():
    global current_card
    next_card()
    #df.remove(current_card)
    #print(word_dictionary)

#randint or random.choice
def next_card():
    global current_card
    current_card = random.choice(word_dictionary)
    current_card_ind = current_card['Unnamed: 0']
    
    for i in range(6):
        name_val = random.randint(0,len(df)-1)
        buttons[i].config(text=df.iloc[name_val]['fn']+' '+df.iloc[name_val]['ln'][0]+'.',command=incorrect_name)
        
    correct_ind = random.randint(0,5)
    buttons[i].config(text=current_card['fn']+' '+current_card['ln'][0]+'.',command=correct_name)
    
    canvas.itemconfig(face, image=mask_im[current_card_ind], activeimage=non_mask_im[current_card_ind])
    canvas.itemconfig(p_name, text='?', fill="#311a4d")
    canvas.itemconfig(p_pronoun, text=current_card['pronouns'], fill="#311a4d")
    #timer = window.after(3000, func=flip_card)


def correct_name():
    canvas.itemconfig(p_name, text='Correct!', fill="green")
    canvas.itemconfig(p_pronoun, text='', fill="#311a4d")
    timer = window.after(1500, func=next_card)
    
def incorrect_name():
    canvas.itemconfig(p_name, text='Incorrect: '+current_card['fn']+' '+current_card['ln'], fill="red")
    canvas.itemconfig(p_pronoun, text=current_card['pronouns'], fill="#311a4d")
    timer = window.after(1500, func=next_card)


#---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.geometry("770x620")
window.title("Name ID -- "+course_name)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0 )

#Add image to the Canvas Items
non_mask_im = []
mask_im = []
for i in range(len(df)):
    non_mask_im.append(PhotoImage(file=df.iloc[i]['photo']))
    mask_im.append(PhotoImage(file=df.iloc[i]['photo_mask']))

#if create it inside function, by the end of the function call, reference will be gone
box = canvas.create_polygon([2,2,660,2,660,520,2,520], outline="#311a4d",fill="#FFFFFF",width=5)
header = canvas.create_text(330, 50, text=course_name, fill="#311a4d", font=('Arial 25 bold'))
m_im = PhotoImage(file='Mammoth.png')
mammoth = canvas.create_image(60, 40, image=m_im)

face = canvas.create_image(330, 190, image=mask_im[0], activeimage=non_mask_im[0])
p_name = canvas.create_text(330, 330, text="title", fill="#311a4d", font=("Arial", 25, "italic"))
p_pronoun = canvas.create_text(330, 370, text="a", fill="#311a4d", font=("Arial", 15, "bold"))
canvas.grid(column=0,row=0, columnspan=2)

#buttons
buttons = []
bposition_x = [50,250,450,50,250,450]
bposition_y = [400,400,400,450,450,450]
for i in range(6):
    buttons.append(Button(highlightthickness=1, command=next_card, text='Button '+str(i), width = 20, height=3, font=("Arial", 12, "bold"), bg="#d2cfcd", fg="#311a4d", activebackground="#b7a5d3"))
    buttons[i].place(x=bposition_x[i],y=bposition_y[i])

#first screen setup with actual values
next_card()

window.mainloop()