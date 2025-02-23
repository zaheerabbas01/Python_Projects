import tkinter as tk
from tkinter import messagebox
import math

class Game:
    def __init__(self,rows,main):
        root = tk.Toplevel(main)
        root.title("Draw Arrow Line Between Circles")
        root.attributes("-fullscreen", True)

        tk.Button(root,text=" Exit ",width=20,bg="orange", command=lambda: ext()).place(x=500, y=660)

        tk.Label(root,text=" TURN ",bg="gray").place(x=50,y=50)
        self.turn_lab = tk.Label(root,text=" X ",bg="red")
        self.turn_lab.place(x=100,y=50)
        self.turn = "x"

        tk.Label(root,text=" SCORE ",bg="gray").place(x=150,y=15)
        self.x = 0
        self.x_lab = tk.Label(root,text=f" X : {self.x}",bg="red")
        self.x_lab.place(x=250,y=15)

        self.y = 0
        self.y_lab = tk.Label(root,text=f" Y : {self.y}",bg="blue")
        self.y_lab.place(x=350,y=15)
        self.box = 0
        self.total_box = (rows - 1) * 3 
        # Create a canvas widget
        canvas = tk.Canvas(root, width=1000, height=600, bg="white")
        canvas.pack(pady=40)

        # List to store circle IDs
        self.circles = []
        self.connected_circles = {}
        self.lines = []
        n = rows * 4
        def draw_circles(n):
            i = 100
            j = 100
            r = 14
            for rows in range(int(n/4)):
                for col in range(4):
                    circle = canvas.create_oval(i - r, j - r, i + r, j + r, fill="white", outline="black")
                    self.circles.append(circle)
                    i += 250
                j += 100
                i = 100

        draw_circles(n)

        self.first_circle_clicked = None
        self.second_circle_clicked = None

        def get_intersection_point(circle1, circle2):
            x1, y1, _, _ = canvas.coords(circle1)
            x2, y2, _, _ = canvas.coords(circle2)

            # Center of the circles
            center1 = (x1 + 14, y1 + 14)
            center2 = (x2 + 14, y2 + 14)

            # Vector from center1 to center2
            dx = center2[0] - center1[0]
            dy = center2[1] - center1[1]

            # Distance between centers
            distance = math.hypot(dx, dy)

            # Normalize the vector
            dx /= distance
            dy /= distance

            # Calculate intersection points on the circumference
            start_x = center1[0] + dx * 14  # 20 is the radius
            start_y = center1[1] + dy * 14
            end_x = center2[0] - dx * 14
            end_y = center2[1] - dy * 14

            return (start_x, start_y, end_x, end_y)

        def on_circle_click(event):

            clicked_circle = canvas.find_withtag("current")[0]
            if self.turn == "x":
                canvas.itemconfig(clicked_circle, fill="red")
            else:
                canvas.itemconfig(clicked_circle, fill="blue")


            if self.first_circle_clicked is None:
                self.first_circle_clicked = clicked_circle
            else:
                self.second_circle_clicked = clicked_circle
                if self.second_circle_clicked not in [self.first_circle_clicked + 1, self.first_circle_clicked + 4,
                                                abs(4 - self.first_circle_clicked), abs(1 - self.first_circle_clicked)]:
                    canvas.itemconfig(clicked_circle, fill="white")
                    return

                self.connected_circles[self.first_circle_clicked] = {"connect": self.second_circle_clicked}
                if check_connection(self.first_circle_clicked, self.second_circle_clicked):
                    canvas.itemconfig(clicked_circle, fill="green")
                    return

                x1, y1, x2, y2 = get_intersection_point(self.first_circle_clicked,self.second_circle_clicked)

                line = canvas.create_line(x1, y1, x2, y2, fill="navy blue", width=5)
                self.lines.append((self.first_circle_clicked, self.second_circle_clicked))

                canvas.itemconfig(self.first_circle_clicked, fill="#DC143C")
                canvas.itemconfig(self.second_circle_clicked, fill="#DC143C")
                
                check_square()
                if self.turn == "x":
                    self.turn_lab.config(text=" Y ",bg="blue")
                    self.turn = "y"
                else:
                    self.turn_lab.config(text=" X ",bg="red")
                    self.turn = "x"
                self.first_circle_clicked = None
                self.second_circle_clicked = None

        def check_connection(f, l):
            for keys in self.connected_circles:
                if self.connected_circles[keys]["connect"] == f and keys == l:
                    return True
            return False
        def patterns(n):
            for i in range(1,n):
                a = i
                b = i + 1
                self.square_patterns.append((a,b,a+4,b+4))    
        self.square_patterns = []
        patterns(n)
        
        def check_square():
            for a, b, c, d in self.square_patterns:
                if ((a, b) in self.lines or (b, a) in self.lines) and \
                ((b, d) in self.lines or (d, b) in self.lines) and \
                ((d, c) in self.lines or (c, d) in self.lines) and \
                ((c, a) in self.lines or (a, c) in self.lines):
                    draw_x_y(a,b,c,d,self.turn)
                    self.box += 1
                    self.square_patterns = [tup for tup in self.square_patterns if tup != (a, b, c, d)]
            if self.box == self.total_box:
                ext()

        def draw_x_y(a, b, c, d,trn):
            x1, y1, _, _ = canvas.coords(a)
            x2, y2, _, _ = canvas.coords(d)
            center_x = (x1 + x2) / 2 + 20
            center_y = (y1 + y2) / 2 + 20

            if trn == "x":
                canvas.create_text(center_x, center_y, text="X", font=("Arial", 20,"bold"), fill="red")
                self.x += 1
                self.x_lab.config(text=f" X : {self.x}")
            else:
                canvas.create_text(center_x, center_y, text="Y", font=("Arial", 20,"bold"), fill="Blue")
                self.y += 1
                self.y_lab.config(text=f" Y : {self.y}")

        for circle in self.circles:
            canvas.tag_bind(circle, "<Button-1>", on_circle_click)

        def ext():
            end = tk.Toplevel(root)
            end.geometry("400x300+500+200")
            end.title("game over")
            tk.Label(end,text="  GAME OVER  ",font=("Arial",20,"bold")).pack(padx=30,pady=30)

            if self.x > self.y:
                tk.Label(end,text=f"  Winner X ",font=("Arial",20),bg="red").pack(padx=30,pady=30)
            elif self.x < self.y:
                tk.Label(end,text=f"  Winner Y ",font=("Arial",20),bg="blue").pack(padx=30,pady=30)
            else:
                tk.Label(end,text=f"  Game Tied  ",font=("Arial",16),bg="black",fg="white").pack(padx=30,pady=30)
            
            tk.Button(end,text=" Play Again ",command=lambda:play_again(),width=20,bg="gray").pack(padx=30,pady=10)
            tk.Button(end,text=" Exit ",command=lambda:root.destroy(),width=20,bg="gray").pack(padx=30,pady=10)
        def play_again():
            root.destroy()
            Game(rows,main)
        root.mainloop()
# Game(5)
