import turtle

# Setup screen
screen = turtle.Screen()
screen.bgcolor("pale turquoise")
screen.title("Pet Adoption Game")

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

# Global variable for hunger
hunger = 100
game_active = True

def display_message(message, y_offset=0):
    t.clear()
    # Draw a simple "pet" (a circle) so the screen isn't empty
    t.penup()
    t.goto(0, -50)
    t.pendown()
    t.fillcolor("orange")
    t.begin_fill()
    t.circle(40)
    t.end_fill()
    
    # Draw text
    t.penup()
    t.goto(0, y_offset + 50)
    t.write(message, align="center", font=("Arial", 18, "bold"))

def feed_pet(x, y):
    global hunger
    if game_active and hunger < 100:
        hunger += 1
        # We don't call update_display here to avoid timer stacking
        # Just let the next timer tick show the new value

def update_game():
    global hunger, game_active
    
    if hunger <= 0:
        display_message(f"Oh no! {name_pet} ran away to find food!")
        game_active = False
        return # Stops the loop

    hunger -= 1
    
    if hunger > 10:
        display_message(f"{name_pet}'s Hunger: {hunger}\n(Click to feed!)")
    else:
        display_message(f"{name_pet} is STARVING ({hunger})!\nCLICK TO FEED!")

    # Schedule the NEXT decrease in 1 second
    screen.ontimer(update_game, 1000) 

# 1. Welcome and Name Input
name = screen.textinput("Welcome", "Please enter your name:")

if name:
    name_pet = screen.textinput("Pet Name", "What is your pet's name?")
    
    if name_pet:
        pet_list = ["Dog", "Cat", "Hamster", "Rabbit"]
        options = ", ".join(pet_list)
        pet_choice = screen.textinput("Choose a Pet", f"Options: {options}\n\nPick one:")

        if pet_choice and pet_choice.capitalize() in pet_list:
            screen.onclick(feed_pet)
            update_game() # Start the loop
        else:
            display_message("Invalid choice. Restart to play.")

screen.mainloop()
