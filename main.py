import turtle

# --- Setup Screen ---
screen = turtle.Screen()
screen.bgcolor("pale turquoise")
screen.title("Pet Adoption Game")
screen.setup(width=600, height=600)
screen.tracer(0) 

# --- Global Variables ---
stats = {"hunger": 100, "happiness": 100}
game_active = True
pet_name = ""
pet_type = ""

# Setup Turtles
pet_drawer = turtle.Turtle()
pet_drawer.hideturtle()
ui_drawer = turtle.Turtle()
ui_drawer.hideturtle()

def draw_pet(mood):
    pet_drawer.clear()
    
    colors = {
        "Dog": "orange",
        "Cat": "light gray",
        "Hamster": "tan",
        "Rabbit": "white",
        "Dragon": "forest green"
    }
    
    body_color = colors.get(pet_type, "gold")
    if mood == "sad":
        body_color = "light coral"

    # Draw Body
    pet_drawer.penup()
    pet_drawer.goto(0, -100)
    pet_drawer.pendown()
    pet_drawer.fillcolor(body_color)
    pet_drawer.begin_fill()
    pet_drawer.circle(100)
    pet_drawer.end_fill()

    # ADDED: Ear logic for Cats
    if pet_type == "Cat":
        for x in [-70, 30]: # Position ears
            pet_drawer.penup()
            pet_drawer.goto(x, 70)
            pet_drawer.setheading(0)
            pet_drawer.pendown()
            pet_drawer.begin_fill()
            for _ in range(3): # Triangle shape
                pet_drawer.forward(40)
                pet_drawer.left(120)
            pet_drawer.end_fill()

    # Draw Eyes
    for x in [-35, 35]:
        pet_drawer.penup()
        pet_drawer.goto(x, 20)
        pet_drawer.pendown()
        pet_drawer.dot(20, "black")

    # Draw Mouth
    pet_drawer.penup()
    pet_drawer.pensize(5)
    if mood == "happy":
        pet_drawer.goto(-40, -30)
        pet_drawer.setheading(-60)
        pet_drawer.circle(45, 120)
    else:
        pet_drawer.goto(-40, -60)
        pet_drawer.setheading(60)
        pet_drawer.circle(-45, -120)
    pet_drawer.setheading(0)

def update_ui():
    ui_drawer.clear()
    ui_drawer.penup()
    ui_drawer.goto(0, 220)
    ui_drawer.write(f"{pet_name} the {pet_type}", align="center", font=("Arial", 24, "bold"))
    ui_drawer.goto(-220, 180)
    ui_drawer.write(f"Hunger: {stats['hunger']}%", align="left", font=("Arial", 14, "bold"))
    ui_drawer.goto(80, 180)
    ui_drawer.write(f"Happiness: {stats['happiness']}%", align="left", font=("Arial", 14, "bold"))
    ui_drawer.goto(0, -250)
    ui_drawer.write("Press [F] to Feed | Press [P] to Play", align="center", font=("Arial", 12, "italic"))
    screen.update()

def feed():
    if game_active:
        stats["hunger"] = min(100, stats["hunger"] + 20)
        update_ui()

def play():
    if game_active:
        stats["happiness"] = min(100, stats["happiness"] + 20)
        stats["hunger"] -= 5
        update_ui()

def game_loop():
    global game_active
    if not game_active: return

    stats["hunger"] -= 2
    stats["happiness"] -= 1
    
    if stats["hunger"] <= 0:
        draw_pet("sad")
        ui_drawer.goto(0, 0)
        ui_drawer.color("red")
        ui_drawer.write(f"GAME OVER: {pet_name} ran away!", align="center", font=("Arial", 22, "bold"))
        game_active = False
        screen.update()
        return

    mood = "happy" if stats["hunger"] > 30 and stats["happiness"] > 30 else "sad"
    draw_pet(mood)
    update_ui()
    screen.ontimer(game_loop, 1000)

# --- Start Game ---
name_user = screen.textinput("Welcome", "What is your name?")
if name_user:
    pet_name = screen.textinput("Pet Name", "Name your pet:")
    options = ["Dog", "Cat", "Hamster", "Rabbit", "Dragon"]
    pet_choice = screen.textinput("Choose Pet", f"Options: {', '.join(options)}")
    
    if pet_choice and pet_choice.capitalize() in options:
        pet_type = pet_choice.capitalize()
        screen.listen()
        screen.onkey(feed, "f")
        screen.onkey(play, "p")
        game_loop()
    else:
        ui_drawer.write("Invalid choice. Please restart.", align="center", font=("Arial", 18))

screen.mainloop()
