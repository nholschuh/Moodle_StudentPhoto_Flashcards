from tkinter import *
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
    
    df = pandas.DataFrame(word_dictionary)


#randint or random.choice
def next_card():
    global current_card
    current_card = random.choice(word_dictionary)
    current_card_ind = current_card['Unnamed: 0']
       
    canvas.itemconfig(face, image=mask_im[current_card_ind], activeimage=non_mask_im[current_card_ind])
    canvas.itemconfig(p_name, text=current_card['fn']+' '+current_card['ln'], fill="#311a4d")
    canvas.itemconfig(p_pronoun, text=current_card['pronouns'], fill="#311a4d")
    timer = window.after(5000, func=next_card)


#---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.geometry("770x490")
window.title("Name ID -- "+course_name)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=405, bg=BACKGROUND_COLOR, highlightthickness=0 )

#Add image to the Canvas Items
non_mask_im = []
mask_im = []
for i in range(len(df)):
    non_mask_im.append(PhotoImage(file=df.iloc[i]['photo']))
    mask_im.append(PhotoImage(file=df.iloc[i]['photo_mask']))

#if create it inside function, by the end of the function call, reference will be gone
box = canvas.create_polygon([2,2,660,2,660,400,2,400], outline="#311a4d",fill="#FFFFFF",width=5)
header = canvas.create_text(330, 50, text=course_name, fill="#311a4d", font=('Arial 25 bold'))
m_im = PhotoImage(file='Mammoth.png')
mammoth = canvas.create_image(60, 40, image=m_im)

face = canvas.create_image(330, 190, image=mask_im[0], activeimage=non_mask_im[0])
p_name = canvas.create_text(330, 330, text="title", fill="#311a4d", font=("Arial", 25, "italic"))
p_pronoun = canvas.create_text(330, 370, text="a", fill="#311a4d", font=("Arial", 15, "bold"))
canvas.grid(column=0,row=0, columnspan=2)


#first screen setup with actual values
next_card()

window.mainloop()