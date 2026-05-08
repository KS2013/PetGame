import tkinter as tk
from tkinter import ttk, messagebox

class PetGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Premium Pet Adoption")
        self.root.geometry("500x700")
        self.root.configure(bg="#f0f4f7")

        # Game State
        self.stats = {"hunger": 100, "happiness": 100, "energy": 100}
        self.pet_name = ""
        self.pet_type = ""
        self.game_active = False

        self.setup_start_screen()

    def setup_start_screen(self):
        self.start_frame = tk.Frame(self.root, bg="#f0f4f7")
        self.start_frame.pack(expand=True)

        tk.Label(self.start_frame, text="🐾 Pet Adoption Center", font=("Helvetica", 24, "bold"), bg="#f0f4f7").pack(pady=20)
        
        tk.Label(self.start_frame, text="Pet Name:", bg="#f0f4f7").pack()
        self.name_entry = tk.Entry(self.start_frame, font=("Helvetica", 14))
        self.name_entry.pack(pady=5)

        tk.Label(self.start_frame, text="Select Species:", bg="#f0f4f7").pack()
        self.type_var = tk.StringVar(value="Dog")
        species = ["Dog", "Cat", "Hamster", "Rabbit", "Dragon"]
        self.type_menu = ttk.Combobox(self.start_frame, textvariable=self.type_var, values=species, state="readonly")
        self.type_menu.pack(pady=5)

        tk.Button(self.start_frame, text="Adopt Pet!", command=self.start_game, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), padx=20).pack(pady=20)

    def start_game(self):
        self.pet_name = self.name_entry.get()
        self.pet_type = self.type_var.get()
        
        if not self.pet_name:
            messagebox.showwarning("Wait!", "Your pet needs a name!")
            return

        self.start_frame.destroy()
        self.game_active = True
        self.setup_main_ui()
        self.update_loop()

    def setup_main_ui(self):
        # Header
        tk.Label(self.root, text=f"{self.pet_name} the {self.pet_type}", font=("Helvetica", 20, "bold"), bg="#f0f4f7").pack(pady=10)

        # Canvas for Drawing Pet
        self.canvas = tk.Canvas(self.root, width=400, height=350, bg="white", highlightthickness=2, highlightbackground="#d1d9e0")
        self.canvas.pack(pady=10)

        # Stats Container
        stats_frame = tk.Frame(self.root, bg="#f0f4f7")
        stats_frame.pack(fill="x", padx=50)

        # Hunger Bar
        tk.Label(stats_frame, text="Hunger", bg="#f0f4f7").pack(anchor="w")
        self.hunger_bar = ttk.Progressbar(stats_frame, length=300, mode='determinate')
        self.hunger_bar.pack(pady=2, fill="x")

        # Happiness Bar
        tk.Label(stats_frame, text="Happiness", bg="#f0f4f7").pack(anchor="w")
        self.happiness_bar = ttk.Progressbar(stats_frame, length=300, mode='determinate')
        self.happiness_bar.pack(pady=2, fill="x")

        # Interaction Buttons
        btn_frame = tk.Frame(self.root, bg="#f0f4f7")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="🍎 Feed", width=10, command=self.feed, bg="#ff9f43", fg="white", font=("bold")).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="🎾 Play", width=10, command=self.play, bg="#54a0ff", fg="white", font=("bold")).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="💤 Rest", width=10, command=self.rest, bg="#5f27cd", fg="white", font=("bold")).grid(row=0, column=2, padx=10)

    def draw_pet(self):
        self.canvas.delete("all")
        cx, cy = 200, 200 # Center
        
        colors = {"Dog": "#f39c12", "Cat": "#bdc3c7", "Hamster": "#edbf91", "Rabbit": "#ffffff", "Dragon": "#2ecc71"}
        color = colors.get(self.pet_type, "gold")
        
        # Draw Ears based on type
        if self.pet_type == "Cat":
            self.canvas.create_polygon(cx-70, cy-50, cx-40, cy-120, cx-10, cy-70, fill=color, outline="black")
            self.canvas.create_polygon(cx+70, cy-50, cx+40, cy-120, cx+10, cy-70, fill=color, outline="black")
        elif self.pet_type == "Rabbit":
            self.canvas.create_oval(cx-60, cy-180, cx-20, cy-50, fill=color, outline="black")
            self.canvas.create_oval(cx+20, cy-180, cx+60, cy-50, fill=color, outline="black")
        elif self.pet_type == "Dragon":
            self.canvas.create_polygon(cx-80, cy-40, cx-110, cy-110, cx-40, cy-80, fill="#c0392b")
            self.canvas.create_polygon(cx+80, cy-40, cx+110, cy-110, cx+40, cy-80, fill="#c0392b")

        # Main Body/Head
        self.canvas.create_oval(cx-90, cy-80, cx+90, cy+100, fill=color, outline="#333", width=2)

        # Eyes
        eye_color = "black" if self.stats["hunger"] > 20 else "#576574"
        self.canvas.create_oval(cx-40, cy-10, cx-20, cy+10, fill=eye_color)
        self.canvas.create_oval(cx+20, cy-10, cx+40, cy+10, fill=eye_color)

        # Mouth (Dynamic Mood)
        if self.stats["happiness"] > 50:
            self.canvas.create_arc(cx-40, cy+20, cx+40, cy+60, start=0, extent=-180, style="arc", width=3)
        else:
            self.canvas.create_arc(cx-30, cy+50, cx+30, cy+80, start=0, extent=180, style="arc", width=2)

    def update_loop(self):
        if not self.game_active: return

        # Decay stats
        self.stats["hunger"] -= 1.5
        self.stats["happiness"] -= 1.0
        
        # Clamp values
        for key in self.stats:
            self.stats[key] = max(0, min(100, self.stats[key]))

        # Update Bars
        self.hunger_bar['value'] = self.stats["hunger"]
        self.happiness_bar['value'] = self.stats["happiness"]

        self.draw_pet()

        if self.stats["hunger"] <= 0:
            self.game_active = False
            messagebox.showinfo("Game Over", f"Oh no! {self.pet_name} got too hungry and went to find snacks elsewhere!")
            self.root.destroy()
        else:
            self.root.after(1000, self.update_loop)

    def feed(self):
        self.stats["hunger"] += 15
        self.draw_pet()

    def play(self):
        if self.stats["hunger"] > 10:
            self.stats["happiness"] += 20
            self.stats["hunger"] -= 10
            self.draw_pet()
        else:
            messagebox.showwarning("Too Hungry", f"{self.pet_name} is too hungry to play!")

    def rest(self):
        self.stats["happiness"] += 5
        self.stats["hunger"] -= 5
        self.draw_pet()

if __name__ == "__main__":
    root = tk.Tk()
    game = PetGame(root)
    root.mainloop()
