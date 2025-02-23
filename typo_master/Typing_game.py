from tkinter import messagebox
from customtkinter import *
import customtkinter as ctk
import random
import pandas as pd
import textwrap
import sys
# import files
from type_page import TypingPage
from players_card import PlayerCard

def easy():
    txt3 = "First of all, many people try to forgive people during Diwali. It is certainly an occasion where people forget disputes."
    txt2 = "The simple computer basically consists of CPU, monitor, mouse, and keyboard. Also, there are hundreds of other computer parts that can be attached to it."
    txt1 = "It is very difficult to find the exact origin of computers. But according to some experts computer exists at the time of world war-II."
    return random.choice([txt1,txt2,txt3])
def medium():
    txt1 = "A RAISE in the salaries of members of parliament and the provincial legislatures in Pakistan always evokes a strong negative reaction, at least from vocal segments of society"
    txt2 = "Animals and marine creatures unknowingly consume plastic particles along with their food. Research shows that waste plastic bags have been a major reason for untimely animal deaths"
    txt3 = "Regularly evolving technology has become an important part of our lives. Also, newer technologies are taking the market by storm and the people are getting used to them in no time"
    return random.choice([txt1,txt2,txt3])

def hard():
    txt3 = "The government of Pakistan has been facing a lot of criticism for its decision to increase the salaries of the members of parliament and the provincial legislatures. The opposition parties have been vocal in their criticism"
    txt2 = "Although technology is a good thing, everything has two sides. Technology also has two sides one is good and the other is bad. Here are some negative aspects of technology that we are going to discuss"
    txt1 = "Experts are debating on this topic for years. Also, the technology covered a long way to make human life easier but the negative aspect of it can’t be ignored. Over the years technological advancement has caused a severe rise in pollution."
    return random.choice([txt1,txt2,txt3])

class ScoreCard:
    def __init__(self,player,main_u,level,punct,file_path,mode):

        self.player = player
        self.main_u = main_u
        self.level = level
        self.punct = punct
        self.mode = mode

        self.timer = 40
        self.score_path = ""
        self.cell = 0
        if player == None:
            messagebox.showerror('not selected',"Player is not Selected")
            return            
        self.txt = ""
        if level == "EASY":
            self.txt = textwrap.fill(easy(),width=70)
            self.score_path = "Easy"
        elif level == "MEDIUM":
            self.txt = textwrap.fill(medium(),width=70)
            self.score_path = "Medium"
        elif level == "HARD":
            self.txt = textwrap.fill(hard(),width=70)
            self.score_path = "Hard"
        elif level == "CUSTOM":
            self.content = ""
            def select_file():
                file_path = filedialog.askopenfilename(
                    defaultextension=".txt", 
                        filetypes=[("Text files", "*.txt")],
                        title="Save Excel File",
                        # initialdir="D:\score_counter\data",
                    )
                
                with open(file_path, 'r') as file:
                    self.content = file.read() # Read the entire content of the file
            def done():
                if self.content == "":
                    messagebox.showerror('not selected',"File is not Selected")
                    return
                else:
                    self.content = " ".join(self.content.split()) # Remove extra spaces
                    self.txt = textwrap.fill(self.content,width=70)

                    if punct == "off":
                        self.txt = self.txt.replace(".","")
                        self.txt = self.txt.replace(",","")

                    self.score_path = "Custom"
                    if time_option_var.get() == "0:30":
                        self.timer = 30
                    elif time_option_var.get() == "0:60":
                        self.timer = 60
                    else:
                        t = time_option_var.get()
                        t = t.replace(":",".")
                        t = float(t)
                        self.timer = t*60

                    cust_win.destroy()
                    TypingPage(False,main_u,self.txt.lower(),self.timer,level,punct,player,self.score_path)  # Get the initial score
                    return
                
            # cust_win = CTk()
            cust_win = CTkToplevel(main_u)
            cust_win.title("Custom Difficulty")
            cust_win.geometry("300x200+500+200")
            time_options = ["0:30","0:60","1:30","2:00","3:00","5:00"]
            cust_win._apply_appearance_mode(self.mode)
            cust_win.lift()
            cust_win.grab_set()
            # cust_win
            time_option_var = ctk.StringVar()
            time_option_var.set(time_options[0])  # Set the default value (first option)
            CTkLabel(cust_win,text="Select time").place(relx=0.3,rely=1)
            # Create the CTkOptionMenu widget
            time_option_menu = ctk.CTkOptionMenu(master=cust_win, variable=time_option_var, values=time_options,dropdown_fg_color="blue")
            time_option_menu.place(relx = 0.3, rely = 0.2, anchor = "center")
            btn_add_file = CTkButton(master=cust_win,text="Add File Txt",command=lambda: select_file())
            btn_add_file.place(relx=0.3,rely=0.4)
            btn_done = CTkButton(master=cust_win,text="Done",command=lambda:done())
            btn_done.place(relx=0.3,rely=0.6)
            cust_win.mainloop()
        
        if level != "CUSTOM":
            if punct == "off":
                self.txt = self.txt.replace(".","")
                self.txt = self.txt.replace(",","")
            
            TypingPage(False,main_u,self.txt.lower(),self.timer,level,punct,player,self.score_path,file_path,self.mode)  # Get the initial score
            return
       
class MenuPage:
    def __init__(self):
        main_u = CTk()
        main_u.title("Typo Tracker")
        main_u.geometry(f"800x500+300+150")
        self.selected_option = None
        main_u.attributes("-fullscreen",True)

        CTkLabel(main_u,text="Created By Zaheer Abbas").pack(anchor="n")

        level_options = ["EASY","MEDIUM","HARD","CUSTOM"]

        level_option_var = ctk.StringVar()
        level_option_var.set(level_options[0])  # Set the default value (first option)

        # Create the CTkOptionMenu widget
        level_option_menu = ctk.CTkOptionMenu(main_u, variable=level_option_var, values=level_options,dropdown_fg_color="red")
        level_option_menu.place(relx = 0.5, rely = 0.2, anchor = "center")

        def get_level():
            self.level = level_option_var.get()
            return self.level
        
        self.mode = "Dark"
        def switch_event():
            if switch_var.get() == "on":
                main_u._set_appearance_mode("Dark")
            else:
                main_u._set_appearance_mode("Light")
                self.mode = "Light"


        switch_var = StringVar(value="on")
        switch = CTkSwitch(main_u, text="Dark Mode", command=switch_event,variable=switch_var, onvalue="on", offvalue="off")
        switch.place(relx = 0.8, rely = 0.1, anchor = "center")

        self.label_player = CTkLabel(main_u,text=f"PLAYER  :  {self.selected_option}  ".upper(),fg_color="green",width=100,corner_radius=2)
        self.label_player.place(relx = 0.3, rely = 0.1, anchor = "center")

        self.label_level = CTkLabel(main_u,text=f"Level ",fg_color="green",width=100,corner_radius=2)
        self.label_level.place(relx = 0.3, rely = 0.2, anchor = "center")
        
        # punctuation check box
        self.label_level = CTkLabel(main_u,text=f"PUNCTUATION ",fg_color="green",width=100,corner_radius=2)
        self.label_level.place(relx = 0.3, rely = 0.3, anchor = "center")
        self.current_value = "on"
        def checkbox_event():
            self.current_value = check_var.get()

        check_var = StringVar(value="on")
        checkbox = CTkCheckBox(main_u, text="",command=checkbox_event,variable=check_var, onvalue="on", offvalue="off")
        checkbox.place(relx = 0.5, rely = 0.3, anchor = "center")

        btn_add_file = CTkButton(master=main_u,text="Select Player",command=lambda:self.select_player())
        btn_add_file.place(relx = 0.5, rely = 0.1, anchor = "center")
        self.file_path = None
        def strt():
            ScoreCard(self.selected_option,main_u,get_level(),self.current_value,self.file_path,self.mode)

        btn1 = CTkButton(master=main_u,text="Start",command=lambda:strt())
        btn1.place(relx=0.4,rely=0.7)
        # def ext()
        btn3 = CTkButton(master=main_u,text="Exit",command=lambda:sys.exit(),fg_color="#FF5733",hover_color="#880808")
        btn3.place(relx=0.4,rely=0.9)
        btn3 = CTkButton(master=main_u,text="File Path",command=lambda:self.choose_path(),hover_color="gray18",fg_color="gray25")
        btn3.place(relx=0.7,rely=0.9)
            

        def results():
            PlayerCard(main_u,self.file_path)
            main_u.destroy()
            MenuPage

        btn2 = CTkButton(master=main_u,text="Result",command=lambda:results())
        btn2.place(relx=0.4,rely=0.8)
        
        main_u.mainloop()

    def choose_path(self):
        self.file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx", 
        filetypes=[("Excel files", "*.xlsx")],
        title="Save Excel File",
        )
    def select_player(self):
        opt = []
        if self.file_path == None:
            messagebox.showerror("No Path","File not found")
            return    
        else:
            df = pd.read_excel(self.file_path, usecols="A", skiprows=-1)
            for i in df["Player"]:
                opt.append(i)

    # Function to show the selected option
        def show_selection():
            self.selected_option = option_var.get()
            # messagebox.showinfo("selection",f"{self.selected_option} selected successfully!")
            root.destroy()
            self.label_player.configure(text=f"PLAYER  :  {self.selected_option.upper()} ")

        root = ctk.CTk()
        root.title("CTkOptionMenu Example")
        root.geometry("300x200+500+200")  # Optional: Set the window size

        # Define the options for the OptionMenu
        options = opt

        # Create a CTk variable to store the selected option
        option_var = ctk.StringVar()
        option_var.set(options[0])  # Set the default value (first option)

        # Create the CTkOptionMenu widget
        option_menu = ctk.CTkOptionMenu(root, variable=option_var, values=options)
        option_menu.pack(pady=20)

        # Create a CTk button to show the selected option
        button = ctk.CTkButton(root, text="Select", command=show_selection)
        button.pack(pady=10)

        root.mainloop() 
MenuPage()
