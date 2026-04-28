import turtle
import time

# --- Setup ---
screen = turtle.Screen()
screen.bgcolor("pale turquoise")
screen.title("Pet Adoption Game")
screen.setup(width=600, height=600)
screen.tracer(0) # Turns off animation for smoother drawing

# Turtles for drawing
pet_drawer = turtle.Turtle()
pet_drawer.hideturtle()
ui_drawer = turtle.Turtle()
ui_drawer.hideturtle()

# Game Stats
stats = {"hunger": 100, "happiness": 100, "age": 0}
game_active = True
pet_type = ""
pet_name = ""

def draw_pet(mood):
    """Draws a simple face based on the pet's mood."""
    pet_drawer.clear()
    
    # Body
    pet_drawer.penup()
    pet_drawer.goto(0, -100)
    pet_drawer.pendown()
    colors = {"happy": "gold", "sad": "light coral", "hungry": "orange"}
    pet_drawer.fillcolor(colors.get(mood, "gold"))
    pet_drawer.begin_fill()
    pet_drawer.circle(100)
    pet_drawer.end_fill()

    # Eyes
    for x in [-35, 35]:
        pet_drawer.penup()
        pet_drawer.goto(x, 20)
        pet_drawer.pendown()
        pet_drawer.dot(20, "black")

    # Mouth
    pet_drawer.penup()
    pet_drawer.goto(-40, -30)
    pet_drawer.pendown()
    pet_drawer.pensize(5)
    if mood == "happy":
        pet_drawer.setheading(-60)
        pet_drawer.circle(45, 120)
    else:
        pet_drawer.setheading(60)
        pet_drawer.circle(-45, -120)
    pet_drawer.setheading(0) # Reset heading

def update_ui():
    """Updates the text on screen."""
    ui_drawer.clear()
    ui_drawer.penup()
    ui_drawer.goto(0, 220)
    ui_drawer.write(f"{pet_name} the {pet_type}", align="center", font=("Arial", 24, "bold"))
    
    ui_drawer.goto(-200, 180)
    ui_drawer.write(f"Hunger: {stats['hunger']}%", align="left", font=("Arial", 14, "normal"))
    
    ui_drawer.goto(80, 180)
    ui_drawer.write(f"Happiness: {stats['happiness']}%", align="left", font=("Arial", 14, "normal"))
    
    ui_drawer.goto(0, -250)
    ui_drawer.write("Press 'F' to Feed | Press 'P' to Play", align="center", font=("Arial(12, 'italic')"))
    screen.update()

def feed():
    if game_active and stats["hunger"] < 100:
        stats["hunger"] = min(100, stats["hunger"] + 15)
        update_ui()

def play():
    if game_active and stats["happiness"] < 100:
        stats["happiness"] = min(100, stats["happiness"] + 15)
        stats["hunger"] -= 5 # Playing makes them hungry!
        update_ui()

def game_loop():
    global game_active
    if not game_active:
        return

    # Decrease stats over time
    stats["hunger"] -= 2
    stats["happiness"] -= 1
    
    # Determine Mood
    current_mood = "happy"
    if stats["hunger"] < 30 or stats["happiness"] < 30:
        current_mood = "sad"
    
    # Check Game Over
    if stats["hunger"] <= 0:
        draw_pet("sad")
        ui_drawer.goto(0, 0)
        ui_drawer.write("GAME OVER: Your pet ran away!", align="center", font=("Arial", 20, "bold"))
        game_active = False
        return

    draw_pet(current_mood)
    update_ui()
    screen.ontimer(game_loop, 1000)

# --- Start Game ---
name = screen.textinput("Welcome", "Your Name:")
if name:
    pet_name = screen.textinput("Pet Name", "Name your pet:")
    pet_type = screen.textinput("Choose Pet", "Dog, Cat, or Hamster?").capitalize()

    # Controls
    screen.listen()
    screen.onkey(feed, "f")
    screen.onkey(play, "p")
    
    game_loop()

screen.mainloop()
