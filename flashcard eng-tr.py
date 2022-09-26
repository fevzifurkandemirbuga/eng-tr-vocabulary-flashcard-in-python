import pandas as pd
import tkinter as tk
import random


def next_card():
    global timer
    window.after_cancel(timer)
    index = random.randint(0, len(data)-1)
    canvas.itemconfig(canvasText1, text=column1)
    canvas.itemconfig(canvasText2, text=data["English"][index])
    timer = window.after(3000, flip_card)


def flip_card():
    word = canvas.itemcget(canvasText2, "text")
    index = data[column1][data[column1] == word].index[0]
    canvas.itemconfig(canvasText1, text=column2)
    canvas.itemconfig(canvasText2, text=data["Türkçe"][index])


def to_learn():
    trword = canvas.itemcget(canvasText2, "text")
    if trword in trWordList:
        return next_card()
    word = canvas.itemcget(canvasText2, "text")
    index = data[column2][data[column2] == word].index[0]
    trWordList.append(canvas.itemcget(canvasText2, "text"))
    engWordList.append(data[column1][index])
    newData = {"english": engWordList, "türkçe": trWordList}
    df = pd.DataFrame(newData, index=None)
    df.to_excel("to_learn.xlsx", index=False)
    next_card()


data = pd.read_excel("words.xlsx")
column1 = data.columns[0]
column2 = data.columns[1]
engWordList = []
trWordList = []

window = tk.Tk()
window.config(padx=100, pady=50)
timer = window.after(3000, flip_card)

canvas = tk.Canvas(width=300, height=300, highlightthickness=3, highlightbackground="black")
canvasText1 = canvas.create_text(160, 115, text="", font=("ariel", 10, "italic"))
canvasText2 = canvas.create_text(160, 150, text="", font=("ariel", 30, "bold"))
canvas.grid(column=1, row=1)

rightButton = tk.Button(text="✓", fg="green", font=("ariel", 20, "bold"), command=next_card)
wrongButton = tk.Button(text="X", fg="red", font=("ariel", 20, "bold"), command=to_learn)
rightButton.grid(row=2, column=2)
wrongButton.grid(row=2, column=0)

next_card()

window.mainloop()
