from customtkinter import *
import pandas as pd

x = []
txt_words = []
user_entr_txt = []

class ScorePage:
    def __init__(self,parent,score,player,player_path,content,timer,mode,punct,file_path,theme_mode):
        self.parent = parent
        self.score = score
        self.score_path = player_path
        self.player = player
        self.content = content
        self.timer = timer
        self.mode = mode
        self.punct = punct
        self.file_path = file_path
        self.theme_mode = theme_mode

        ex = pd.read_excel(self.file_path, sheet_name="Sheet1")
        x = int(ex.loc[ex['Player'] == player, self.score_path].iloc[0])

        self.h_score = x  # Initialize high score

        self.card = CTkToplevel(parent)
        self.card.title("Score Card")
        self.card.geometry("300x400+500+200")
        self.card.configure(bg="#f0f0f0")
        self.card._apply_appearance_mode(self.theme_mode)
        self.card.attributes("-fullscreen",True)

        # Game Over Label
        game_over_label = CTkLabel(
            self.card,
            text="SCORE CARD",
            text_color="white",
            width=300,
            height=40,
            font=("Verdana", 24, "bold"),
            bg_color="green"
        )

        game_over_label.pack(pady=20,anchor="center")
        score_frame = CTkFrame(self.card, width=300, height=170)
        score_label = CTkLabel(
            score_frame,
            text="SCORE",
            text_color="white",
            width=100
        )
        score_label.place(x=10,y=30)

        score_num_label = CTkLabel(
            score_frame,
            text=f"{self.score:02}",
            text_color="white",
            fg_color="blue",
            width=100
        )
        score_num_label.place(x=105,y=30)
        # Update High Score
        if self.score > self.h_score:
            self.h_score = self.score

        df = pd.read_excel(self.file_path, sheet_name="Sheet1")
        df.loc[df['Player'] == self.player, self.score_path] = int(self.h_score)
        df.to_excel(self.file_path,index=False)
        
        h_score_label = CTkLabel(
        score_frame,
        text="HIGH SCORE",
        text_color="white",
        width=100
        )
        h_score_label.place(x=10, y=80)
        h_score_num_label = CTkLabel(
            score_frame,
            text=f"{self.h_score:02}",
            text_color="white",
            fg_color="blue",
            width=100
        )
        h_score_num_label.place(x=105, y=80)

        score_frame.pack(pady=20,anchor="center")
        # Play Again Button
        btn_again = CTkButton(
            master=self.card,
            text="Play Again",
            command=self.play_again
        )
        btn_again.pack(pady=20,anchor="center")

        # Exit Button
        btn_ext = CTkButton(
            master=self.card,
            text="Exit",
            command=lambda:self.ext(),
            fg_color="#FF5733",hover_color="#880808"
        )
        btn_ext.pack(pady=10,anchor="center")

        self.card.lift()
        self.card.grab_set()
        self.card.mainloop()

    def play_again(self):
        self.card.destroy()
        main.destroy()

        TypingPage(False,self.parent,self.content,self.timer,self.mode,self.punct,self.player,self.score_path,self.file_path,self.theme_mode)

    def ext(self):
        self.card.destroy()  # Close the current score card window
        self.x = False  # Stop the loop
        main.destroy()
        return


def TypingPage(again = False,roats = None,content = "hello I am zaheer",timer = 40,mode = "easy",punct = "off",player = "zaheer",player_path = None,file_path=None,theme_mode = None):
    score = 0
    class CountdownTimer:
        def __init__(self, root, time_in_seconds,running):
            self.root = root
            self.time_left = time_in_seconds
            user_entr_txt.append("")
            
            self.chr = ""
            self.i = 0
            self.j = 0

            self.timer_label = CTkLabel(root,text="Timer : 00:00",fg_color="green",corner_radius=50,width=200,font=("Arial",20,"bold"))
            self.timer_label.place(relx=0.8,rely=0.2)
            
            CTkLabel(root,text=f"",bg_color="gray",width=140,height=130,corner_radius=15,pady=30).place(x=30,y=25)
            CTkLabel(root,text=f"  Player :  {player}\t").place(x=40,y=30)
            CTkLabel(root,text=f"  Mode   :  {mode.upper().strip()}\t").place(x=40,y=60)
            CTkLabel(root,text=f" Punctuation : {punct.upper()}\t").place(x=40,y=90)
            CTkLabel(root,text=f"  Words :  {len(txt_words)}\t").place(x=40,y=120)

            self.textbox = CTkTextbox(master=main,width=800,font=("Arabic Transparent",17))
            self.textbox.pack(pady=40,padx=20)
            self.textbox.insert("0.0", "")

            main.bind('<Key>', self.key_pressed)
            self.running = running  # Flag to track if the timer is running

            # self.play_again()
            if self.running:
                self.update_timer()

        def update_timer(self):
            if self.running:
                # Convert time left to minutes and seconds
                minutes, seconds = divmod(self.time_left, 60)
                time_str = f"Timer: {minutes:02}:{seconds:02}"

                # Update the label with the remaining time
                self.timer_label.configure(text=time_str)

                if self.time_left > 0:
                    # Decrease the time by 1 second and call the function again after 1000 ms (1 second)
                    self.time_left -= 1
                    self.root.after(1000, self.update_timer)
                else:
                    # Timer reaches 0, display a message (you can customize this action)
                    self.timer_label.configure(text="Time's up!")
                    self.running = False
                    self.update_timer()
                    self.textbox.delete('0.0',"end")
                    des()
                    return

        def key_pressed(self,event):
            # Get the key that was pressed
            pressed_key = event.keysym  # This returns a symbolic name for the key
            if pressed_key == "space":
                try:
                    self.i += 1
                    user_entr_txt[self.i-1] = self.chr.strip()
                    self.chr = ""
                    txt.configure(text=txt_words[self.i])
                except IndexError:
                    self.running = False
                    self.update_timer()
                    self.textbox.delete('0.0',"end")
                    des()
                    return

            elif pressed_key == "BackSpace":
                self.j += 1
                self.chr = self.chr[:-1]
                if self.i == 0:
                    self.j = 0
                    return
                elif self.lastest_key_pressed == "space":
                    self.i -= 1
                    txt.configure(text=txt_words[self.i])
                    self.chr = user_entr_txt[self.i]
                    self.j = 0
                elif self.j > len(txt_words[self.i]):
                    self.i -= 1
                    self.chr = user_entr_txt[self.i]
                    txt.configure(text=txt_words[self.i])
                    self.j = 0
            else:
                self.chr += pressed_key 

            self.lastest_key_pressed = pressed_key

    global main

    if again == True:
        main.destroy()

    main = CTkToplevel(roats)
    main.attributes("-fullscreen",True)
    main.title("My GUI App")
    main_txt = content.replace("\n"," ")
    x.append(main_txt.split(" "))
    main._apply_appearance_mode(theme_mode)
    for word in x:
        for m in word:
            txt_words.append(m)
            user_entr_txt.append("")

    txt1 = CTkLabel(master=main,text=content,font=("Arial",20))
    txt1.pack(pady=20,padx=30)

    txt = CTkLabel(master=main,text=txt_words[0],bg_color="purple",width=200,font=("Arial",20,"bold"))
    txt.pack(pady=10,padx=20)
    def des():
        score = 0
        for i in range(len(txt_words)):
            if txt_words[i].lower() == user_entr_txt[i].lower():
                score += 1

        txt_words.clear()
        x.clear()
        user_entr_txt.clear()

        ScorePage(roats,score,player,player_path,content,timer,mode,punct,file_path,theme_mode)
 
    CTkButton(master=main,text="EXT",command=lambda:des(),fg_color="#FF5733",hover_color="#880808",width=10).place(relx=0.8,rely=0.8)

    countdown = CountdownTimer(main, int(timer), True) # 5 minutes = 300 seconds
    
    main.lift()
    main.grab_set()
    main.mainloop()