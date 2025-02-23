import pandas as pd
from tkinter import messagebox
import customtkinter as ctk
from customtkinter import CTkInputDialog, CTkButton, CTkLabel
# from openpyxl import load_workbook
import os

# Initialize players dictionary
players = {}

# def plr_score():
class PlayerCard:
    def __init__(self,parent,file_path):
        # Improved Excel append function
        self.file_path = file_path
        def append_to_excel(file_name, new_data):
            try:
                if os.path.exists(file_name):
                    # Load existing data
                    existing_df = pd.read_excel(file_name)
                    # Combine old and new data
                    combined_df = pd.concat([existing_df, new_data], ignore_index=True)
                else:
                    combined_df = new_data
                
                # Save combined data
                combined_df.to_excel(file_name, index=False)
            except Exception as e:
                messagebox.showerror("Excel Error", f"Failed to update Excel: {str(e)}")

        def add_player():
            name_dialog = CTkInputDialog(text="Enter player name")
            name_dialog.geometry("400x200+200+50")
            name = name_dialog.get_input()
            
            if not name:
                return
            
            if name in players:
                messagebox.showerror("Error", "Player already exists!")
                return
            
            # Add to players dictionary
            players[name] = {
                'Easy': int(0),
                'Medium': int(0),
                'Hard': int(0),
                'Custom': int(0)
            }
            
            # Create DataFrame for new player
            new_df = pd.DataFrame([{
                'Player': name,
                'Easy': int(0),
                'Medium': int(0),
                'Hard': int(0),
                'Custom':int(0)
            }])
            
            # Update Excel
            append_to_excel(self.file_path, new_df)
            update(scrollable_frame)

        def selected(player):
            self.selected_player = player

        def update(scrollable_frame):
            # Clear existing widgets
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            
            # Add updated players
            for idx, (player, scores) in enumerate(players.items()):
                btn_text = f"\t\t{player}\t\t{scores['Easy']}\t\t{scores['Medium']}\t\t{scores['Hard']}\t\t{scores['Custom']}\t\t"
                btn = ctk.CTkButton(
                    scrollable_frame,
                    text=btn_text,
                    command=lambda p=player: selected(p),
                    width=400
                )
                btn.grid(row=idx, column=0, pady=5, padx=20, sticky="ew")

        def delete_selected():
            if not hasattr(self, 'selected_player') or not self.selected_player:
                messagebox.showwarning("Warning", "No player selected!")
                return
            
            confirm = messagebox.askyesno(
                "Confirm", 
                f"Delete {self.selected_player}?"
            )
            
            if confirm:
                try:
                    # Remove from dictionary
                    del players[self.selected_player]
                    
                    # Update Excel file
                    df = pd.DataFrame.from_dict(players, orient='index').reset_index()
                    df.columns = ['Player', 'Easy', 'Medium', 'Hard','Custom']
                    df.to_excel(file_path, index=False)
                    
                    # Update GUI
                    update(scrollable_frame)
                    # messagebox.showinfo("Success", "Player deleted!")
                    self.selected_player = None
                except Exception as e:
                    messagebox.showerror("Error", f"Deletion failed: {str(e)}")
            app.lift()
            app.grab_set()
        # Load initial data
        try:
            df = pd.read_excel(self.file_path)
            for _, row in df.iterrows():
                players[row['Player']] = {
                    'Easy': row['Easy'],
                    'Medium': row['Medium'],
                    'Hard': row['Hard'],
                    'Custom':row['Custom']
                }
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No existing player data found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

        # GUI setup
        app = ctk.CTkToplevel(parent)
        app.title("Player Manager")
        app.attributes("-fullscreen",True)
        # Configure grid layout
        app.grid_columnconfigure(0, weight=1)
        app.grid_rowconfigure(0, weight=1)


        # Scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(app, width=750, height=400)
        scrollable_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Control buttons
        button_frame = ctk.CTkFrame(app)
        button_frame.grid(row=1, column=0, pady=10, sticky="ew")

        CTkLabel(app, text="Player", font=("Arial", 10,"bold"),height=10,width=100).place(x=140, y=8)
        CTkLabel(app, text="Easy", font=("Arial", 10,"bold"),height=10,width=100).place(x=240, y=8)
        CTkLabel(app, text="Medium", font=("Arial", 10,"bold"),height=10,width=100).place(x=360, y=8)
        CTkLabel(app, text="Hard", font=("Arial", 10,"bold"),height=10,width=100).place(x=480, y=8)
        CTkLabel(app, text="Custom", font=("Arial", 10,"bold"),height=10,width=100).place(x=600, y=8)
        CTkButton(
            button_frame, 
            text="Add Player",
            command=add_player
        ).pack(side="left", padx=10)

        CTkButton(
            button_frame,
            text="Delete Player",
            command=delete_selected,
            fg_color="#d9534f"
        ).pack(side="left", padx=10)

        CTkButton(
            button_frame,
            text="Exit",
            command=lambda:app.destroy(),
            fg_color="#5bc0de"
        ).pack(side="right", padx=10)

        # Initial update
        update(scrollable_frame)
        app.lift()
        app.grab_set()
        app.mainloop()

# PlayerCard()
