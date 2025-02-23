from tkinter import messagebox
from customtkinter import CTkLabel,CTkButton,CTk,filedialog
import customtkinter as ctk
import random
import pandas as pd
import sys
import pygame
import math
import threading
from players_card import PlayerCard

# Initialize Pygame
pygame.init()
LIGHT_BLUE = (173, 216, 230)

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 215, 0)
CH = (255,127,36)

# Game variables
player_score = 0


# Bat mechanics
bat_angle = -120  # Default bat angle (normal position)
bat_swinging = False
bat_swing_speed = 10  # Speed of bat movement
bat_max_angle = 0  # Maximum angle when swinging

# Positions
bowler_pos = (700, 400)
batsman_pos = (200, 450)
stump_pos = (100, 450)
ball_pos = [680, 450]
ball_in_play = False
ball_speed = [0, 0]

score = 0
scores_d = {
    4: 0,
    6: 1,
    8: 2,
    10: 3,
    14: 4,
    25: 6,
}

# Physics
GRAVITY = 0.5
BOUNCE_FACTOR = 0.8

def draw_stickman(surface, x, y, batting=False):
    """Draw the bowler and batsman."""
    pygame.draw.circle(surface, BLACK, (x, y - 40), 20)  # Head
    pygame.draw.line(surface, BLACK, (x, y - 20), (x, y + 20), 2)  # Body
    pygame.draw.line(surface, BLACK, (x, y - 10), (x - 30, y + 10), 2)  # Left Arm
    pygame.draw.line(surface, BLACK, (x, y - 10), (x + 30, y + 10), 2)  # Right Arm
    pygame.draw.line(surface, BLACK, (x, y + 20), (x - 20, y + 50), 2)  # Left Leg
    pygame.draw.line(surface, BLACK, (x, y + 20), (x + 20, y + 50), 2)  # Right Leg

    # Stumps
    pygame.draw.line(surface, YELLOW, (110, 450), (110, 500), 6)

    if batting:
        # Draw bat (Rotates at a fixed point)
        bat_length = 50
        bat_x = x + 25
        bat_y = y + 5
        bat_end_x = bat_x + bat_length * math.cos(math.radians(bat_angle))
        bat_end_y = bat_y - bat_length * math.sin(math.radians(bat_angle))
        pygame.draw.line(surface, CH, (bat_x, bat_y), (int(bat_end_x), int(bat_end_y)), 5)

def draw_pitch(screen):
    """Draw the cricket pitch and ground."""
    pygame.draw.rect(screen, GREEN, (0, 500, SCREEN_WIDTH, 100))  # Grass
    pygame.draw.line(screen, BROWN, (100, 500), (700, 500), 5)  # Pitch

def draw_ball(screen):
    """Draw the cricket ball."""
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), 8)

def bowl():
    """Start bowling the ball."""
    global ball_in_play, ball_speed
    ball_pos[:] = [680, 450]  # Reset ball position
    speed = 15
    angle = random.uniform(10, 20)  # Slight random variation in bowling angle
    ball_speed = [-speed * math.cos(math.radians(angle)), -speed * math.sin(math.radians(angle))]
    ball_in_play = True
def check_collision():
    """Check if the ball collides with the bat."""
    bat_length = 50
    bat_x = batsman_pos[0] + 30
    bat_y = batsman_pos[1] - 40
    bat_end_x = bat_x + bat_length * math.cos(math.radians(bat_angle))
    bat_end_y = bat_y - bat_length * math.sin(math.radians(bat_angle))

    ball_x, ball_y = ball_pos
    distance = math.hypot(bat_end_x - ball_x, bat_end_y - ball_y)

    if distance < 80:
        return True  # Ball is close enough to bat
    else:
        return False

def check_wicket():
    """Check if the ball hits the stumps."""
    global player_score

    stump_x = 110
    stump_top_y = 450
    stump_bottom_y = 500

    ball_x, ball_y = ball_pos

    if stump_x - 5 <= ball_x <= stump_x + 5 and stump_top_y <= ball_y <= stump_bottom_y:
        player_score = 0
        reset_ball()

def update_physics(screen):
    """Update the ball's physics and check for collisions."""
    global ball_speed, player_score, bat_swinging, bat_angle, score

    if ball_in_play:
        ball_speed[1] += GRAVITY  # Apply gravity
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        if ball_pos[1] > 500:  # Ball hits the ground
            ball_speed[1] *= -BOUNCE_FACTOR
            ball_pos[1] = 500

        if ball_pos[0] < 50 or ball_pos[0] > SCREEN_WIDTH - 50:
            score = 0
            player_score += 0
            reset_ball(False)

        if bat_swinging:
            if check_collision():  # Bat hits ball
                rnd = random.choice([6, 8, 10, 14,14, 25,25])
                ball_speed = [rnd, -rnd]  # Hit effect
                score = scores_d[abs(ball_speed[1])]
                player_score += score
                bat_swinging = False

        check_wicket()

        if ball_pos[0] < 80 and ball_pos[1] == 500:  # Ball stopped
            reset_ball(False)

def reset_ball(wic=True):
    """Reset the ball after a wicket or boundary."""
    global ball_in_play
    if not wic:
        pygame.time.wait(500)
        ball_pos[:] = [680, 450]  # Reset ball position
    ball_in_play = False

def draw_ui(screen,player,h_score):
    """Draw the game UI (score, hits)."""
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {player_score}", True, BLACK)
    screen.blit(text, (60, 20))
    runs = font.render(f"Hit! : {score}", True, BLACK)
    screen.blit(runs, (400, 20))

    runs = font.render(f"Player : {player.upper()}", True, BLACK)
    screen.blit(runs, (800, 20))
    runs = font.render(f"High Score : {h_score}", True, BLACK)
    screen.blit(runs, (800, 70))

def game_page(screen,player,file):
    """Main game loop."""
    global bat_angle, bat_swinging

    clock = pygame.time.Clock()
    running = True

    ex = pd.read_excel(file, sheet_name="Sheet1")
    x = int(ex.loc[ex['Player'] == player, "Score"].iloc[0])

    h_score = x  # Initialize high score

    while running:
        screen.fill(LIGHT_BLUE)
        draw_pitch(screen)
        draw_stickman(screen, 200, 450, batting=True)
        draw_stickman(screen, 650, 450)
        draw_ball(screen)
        draw_ui(screen,player,h_score)

        if h_score < player_score:
            h_score = player_score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not ball_in_play:
                    bowl()

                if event.key == pygame.K_RETURN:
                    bat_swinging = True
                    bat_angle = 0  # Swing forward

                if event.key == pygame.K_ESCAPE:
                    add_score(player,file,h_score)
                    running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    bat_swinging = False
                    bat_angle = -120  # Reset bat position

        update_physics(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
def add_score(player,file_path,h_score):

    df = pd.read_excel(file_path, sheet_name="Sheet1")
    df.loc[df['Player'] == player, "Score"] = int(h_score)
    df.to_excel(file_path,index=False)
        
class ScoreCard:
    def __init__(self, player, main_u, file_path):
        self.player = player
        self.main_u = main_u
        self.file_path = file_path
        self.speed = 0

        if player is None:
            messagebox.showerror('Not Selected', "Player is not Selected")
            return

        threading.Thread(target=self.start_pygame, daemon=True).start()

    def start_pygame(self):
        # Get the window ID of the ctkinter window
        
        screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
        pygame.display.set_caption("Doodle-Style Cricket")

        # Run the game
        game_page(screen,self.player,self.file_path)

class MenuPage:
    def __init__(self):
        main_u = CTk()
        main_u.title("Typo Tracker")
        # main_u.geometry("800x500+300+150")
        # main_u.configure(bg_color="blue")
        main_u.attributes("-fullscreen", True)

        self.selected_option = None
        CTkLabel(main_u, text="Created By Zaheer Abbas").pack(anchor="n")

        self.label_player = CTkLabel(main_u, text=f"PLAYER  :  {self.selected_option}  ".upper(), width=100, corner_radius=2)
        self.label_player.place(relx=0.3, rely=0.3, anchor="center")

        btn_add_file = CTkButton(master=main_u, text="Select Player", command=lambda: self.select_player(),fg_color="bisque4")
        btn_add_file.place(relx=0.5, rely=0.3, anchor="center")
        self.file_path = None

        def start_game():
            ScoreCard(self.selected_option, main_u, self.file_path)

        btn1 = CTkButton(master=main_u, text="Start", command=lambda: start_game(),fg_color="snow4",hover_color="gray18")
        btn1.place(relx=0.4, rely=0.7)

        btn3 = CTkButton(master=main_u, text="Exit", command=lambda: sys.exit(), fg_color="#FF5733", hover_color="#880808")
        btn3.place(relx=0.4, rely=0.9)

        btn3 = CTkButton(master=main_u, text="File Path", command=lambda: self.choose_path(), hover_color="gray18", fg_color="gray25")
        btn3.place(relx=0.7, rely=0.9)

        def results():
            PlayerCard(main_u, self.file_path)
            main_u.destroy()
            MenuPage()

        btn2 = CTkButton(master=main_u, text="Result", command=lambda: results(),fg_color="snow4",hover_color="gray18")
        btn2.place(relx=0.4, rely=0.8)

        main_u.mainloop()

    def choose_path(self):
        self.file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Excel File",
        )

    def select_player(self):
        opt = []
        if self.file_path is None:
            messagebox.showerror("No Path", "File not found")
            return
        else:
            df = pd.read_excel(self.file_path, usecols="A", skiprows=-1)
            for i in df["Player"]:
                opt.append(i)

        # Function to show the selected option
        def show_selection():
            self.selected_option = option_var.get()
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

# Run the application
MenuPage()