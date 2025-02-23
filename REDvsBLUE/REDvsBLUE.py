import tkinter as tk
from tkinter import messagebox
from game_page import Game
levels = {
    "Easy": 3,
    "Medium": 4,
    "Hard": 5
}
def rows():

    selected_choice = option_var.get()  # Get the selected value
    return levels[selected_choice]

def start(rows,parent):
    Game(rows,parent)

# Create a variable to store the selected option
main = tk.Tk()
main.title("red and blue")
main.attributes("-fullscreen",True)
main.configure(bg="light blue")

option_var = tk.StringVar()
option_var.set("Easy")  # Set the default value
choices = ["Easy","Medium","Hard"]
option_menu = tk.OptionMenu(main, option_var, *choices)
option_menu.config(bg="black",fg="white",width=30)

tk.Label(main,text=" Red ",fg="red",font=("Arial",20,"bold")).pack(padx = 30, pady=50)
tk.Label(main,text=" VS ",font=("Arial",20,"bold")).pack(padx = 50, pady=50)
tk.Label(main,text=" Blue ",fg="blue",font=("Arial",20,"bold")).pack(padx = 70, pady=50)
option_menu.pack(pady=10)

tk.Button(main,text=" Start ",width=30,bg="orange",command=lambda:start(rows(),main)).pack(pady=20)
tk.Button(main,text=" Exit ",width=30,bg="orange red",command=lambda:main.destroy()).pack(pady=10)

main.mainloop()
