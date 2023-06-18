import random
from time import sleep

# ToDone: Figure out why encounters stop after reaching level 2
# ToDone: Add instructions and goal of the game
# ToDone: Add more options to choose from in each room based on the event/monster (e.g. fight or run away, open chest or leave it, etc.)
# ToDone: Make map bigger (10x10)
# ToDone: Slow down combat
# ToDo: Add more monsters
# ToDo: Add more events
# ToDo: Add mimic monster type
# ToDo: Add more ASCII art for monsters and events
# ToDontDoThisItWillTakeWayTooLong: Add collectibles and show how many you've collected at the end

class Room:
    def __init__(self, description, event=None, monster=None):
        self.description = description
        self.event = event
        self.monster = monster
        self.visited = False

    def enter(self, player):
        # If the room was visited and monster was defeated, respawn it as a skeleton
        if self.visited and self.monster and self.monster.health <= 0:
            self.monster = Monster("a skeleton", 1, 30, 50)
            print(f"As you look around, the corpse of the {self.monster.name} begins to stir. It rises, a skeleton now!")
            self.monster.health = 30  # The skeleton comes to life!
            return f"You encounter {self.monster.name}!"
        elif self.visited:
            return "You've already explored this room."
        else:
            self.visited = True
            if self.event:
                if self.event.health_restore:
                    player.health = 500 + (50 * (player.level - 1))
                    print("Your health has been fully restored!")
                return self.event.description
            elif self.monster and self.monster.min_player_level <= player.level:
                return f"You encounter {self.monster.name}!"
            else:
                return self.description


class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.experience = 0
        self.health = 500
        self.rooms_visited = 0

    def damage(self):
        return (random.randint(0, 10) * self.level) + random.randint(0, 1)

    def gain_experience(self, amount):
        self.experience += amount

        if self.experience >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.health += 50  # Increase health by 50 each level up
        print(f"\n{self.name} leveled up! You are now level {self.level}!\n")


class Event:
    def __init__(self, description, exp_gain, health_restore=False):
        self.description = description
        self.exp_gain = exp_gain
        self.health_restore = health_restore

    def activate(self, player):
        if self.health_restore:
            player.health = 500 + (50 * (player.level - 1))
            print("Your health has been fully restored!")

        else:
            player.gain_experience(self.exp_gain)


class Monster:
    def __init__(self, name, level, health, exp_gain, min_player_level=0, guaranteed_level_up=False):
        self.name = name
        self.level = level
        self.health = health
        self.exp_gain = exp_gain
        self.min_player_level = min_player_level
        self.guaranteed_level_up = guaranteed_level_up

    def damage(self):
        return (random.randint(0, 10) * self.level) + random.randint(0, 1)


    def spawn(self):
        return Monster(
            self.name, 
            self.level, 
            self.health, 
            self.exp_gain,
            self.min_player_level,
            self.guaranteed_level_up
            )

def game():
    # Setting up the player
    player = Player(input("Enter your name: "))
    print("\n")
    print(f"Welcome {player.name}! \nYou are a level {player.level} adventurer. \nYour goal is to survive until you find the treasure!")
    sleep(2)
    print("You will encounter monsters and events along the way. \nYou will gain experience for defeating monsters and completing events. \nEach level up will increase your health and damage output.")
    sleep(4)
    print("Good luck!")
    sleep(2)
    print("\n")
    # Print the Title Screen
    print(
        """\

 _____                                           _______               __                        
|     \.--.--.-----.-----.-----.-----.-----.    |    ___|.--.--.-----.|  |.-----.----.-----.----.
|  --  |  |  |     |  _  |  -__|  _  |     |    |    ___||_   _|  _  ||  ||  _  |   _|  -__|   _|
|_____/|_____|__|__|___  |_____|_____|__|__|    |_______||__.__|   __||__||_____|__| |_____|__|  
                   |_____|                                     |__|                              
"""
    )
    print("                                                                                    \x1b[3m\x1b[1;31mBy: \x1b[0m\x1b[3m\x1b[1;34mAndrew\x1b[0m")
    print("\n")
    sleep(1)
    input("Press Enter to begin.")

    # Room events and monsters
    events = [
        Event("You found a hidden stash of gold!", 200),
        Event("You disarmed a deadly trap!", 150),
        Event("You found a fairy fountain! Health restored to full.", 0, health_restore=True,),
        Event("You helped a lost ghost find peace!", 250),
        Event("You solved an ancient riddle!", 300),
    ]

    monsters = [
        Monster("a goblin", 1, 50, 50),
        Monster("an orc", 2, 100, 100),
        Monster("a ghost", 3, 150, 100, min_player_level=3),
        Monster("a dragon", 4, 200, 500, min_player_level=4, guaranteed_level_up=True),
    ]


    # Setting up the map (10x10 grid)
    map = []
    for i in range(10):
        row = []
        for j in range(10):

            if i == 0 and j == 0:  # Ensure the starting room is always empty
                room_desc = "You wake up in a damp, dark room. You can't remember how you got here. \nYou see a door to the South and to the East."
                room_event = None
                room_monster = None
            else:
                room_desc = f"You are in room at coordinates ({i}, {j})."
                room_chances = random.random()

                room_event = None
                room_monster = None
                if room_chances <= 0.4:  # 40% chance of event
                    room_event = random.choice(events)
                elif room_chances >= 0.6:  # 40% chance of monster
                    possible_monsters = [monster for monster in monsters if monster.min_player_level <= player.level]
                    if possible_monsters:
                        room_monster = random.choice(possible_monsters).spawn()
                elif room_chances > 0.4 and room_chances < 0.6:
                    # in this case, show output saying that the room is empty
                    room_desc = f"You are in room at coordinates ({i}, {j}). \nThis room is empty."

            row.append(Room(room_desc, event=room_event, monster=room_monster))
        map.append(row)
    # The final room always contains the treasure
    map[9][9] = Room(
        "You have reached the treasure room!",
        event=Event("You found the treasure!", 500),
    )

    def print_compass():
        print("You can go: ", end="")
        if y > 0:
            print("NORTH ", end="")
        if y < 9:
            print("SOUTH ", end="")
        if x > 0:
            print("WEST ", end="")
        if x < 9:
            print("EAST ", end="")
        print()

    # Function to print the map
    def print_map():
        for i in range(10):
            for j in range(10):
                if (i == 0 and j == 0) and (i == y and j == x):
                    print("[O]", end=" ")
                elif (i == 0 and j == 0) and not (i == y and j == x):
                    print("[s]", end=" ")
                elif i == y and j == x:
                    print("[o]", end=" ")
                elif map[i][j].visited:
                    print("[x]", end=" ")
                else:
                    print("[ ]", end=" ")
            print()

    # Previous room
    prevX, prevY = 0, 0

    # Starting position
    x, y = 0, 0

    # Main game loop
    while True:
        room = map[y][x]  # Access room using y for row and x for column

        if not room.visited:
            player.rooms_visited += 1
        print_compass()  # Print the compass
        print_map()  # Print the map
        print(room.enter(player))  # Use the enter method to print the description

        if room.event and not room.visited:
            print(room.event.description)

            if room.event.health_restore:
                player.health = 500 + 50 * (player.level - 1)
                print("Your health has been fully restored!")
            else:
                room.event.activate(player)

        if room.monster and room.monster.health >= 0:
            sleep(2)
            print(f"Would you like to fight {room.monster.name} or go back the way you came? (Fight/Run)")
            fight_or_run = input("> ")

            if fight_or_run.lower() == "run" or fight_or_run.lower() == "r":
                print(f"You run away from {room.monster.name}!")
                # put player back in previous room
                x, y = prevX, prevY
                continue

            else :
                while player.health > 0 and room.monster.health > 0:
                    monsterDamage = room.monster.damage()
                    playerDamage = player.damage()
                    player.health -= monsterDamage

                    print(f"The {room.monster.name} attacks for {monsterDamage}! You have {player.health} health remaining.")

                    if player.health <= 0:
                        print("You have been defeated.")
                        return
                    room.monster.health -= playerDamage  # Player deals damage equal to 8 times their level

                    if room.monster.health > 0:
                        print(
                            f"You attack for {playerDamage}! The {room.monster.name} has {room.monster.health} health remaining."
                        )
                        sleep(.5)
                
                print(f"You defeated {room.monster.name}! \nYou gain {room.monster.exp_gain} experience.")
                sleep(1)

                room.monster.health = 0
                player.gain_experience(room.monster.exp_gain)

                if room.monster.guaranteed_level_up:
                    while player.experience < player.level * 100:
                        player.gain_experience(100)

        if x == 9 and y == 9:
            break  # end game when player reaches the treasure room

        # Player movement
        while True:
            direction = input("Which way do you want to go? (North, South, East, West) \n>")
            if (direction.lower() == "north" or direction.lower() == "n") and y > 0:
                prevX, prevY = x, y
                y -= 1
                break
            elif (direction.lower() == "south" or direction.lower() == "s") and y < 9:
                prevX, prevY = x, y
                y += 1
                break
            elif (direction.lower() == "west" or direction.lower() == "w") and x > 0:
                prevX, prevY = x, y
                x -= 1
                break
            elif (direction.lower() == "east" or direction.lower() == "e") and x < 9:
                prevX, prevY = x, y
                x += 1
                break
            else:
                print("You can't go that way!")
    sleep(1)
    print("""\
    
             |                   |                  |                     |
    _________|________________.=""_;=.______________|_____________________|_______
    |                   |  ,-"_,=""     `"=.|                  |
    |___________________|__"=._o`"-._        `"=.______________|___________________
             |                `"=._o`"=._      _`"=._                     |
    _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
    |                   |    __.--" , ; `"=._o." ,-"`"-._ ".   |
    |___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
             |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
    _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
    |                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
    |___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
    ____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
    /______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
    ____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
    /______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
    ____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
    /______/______/______/______/______/______/______/______/______/______/_____ /_

    """)
    sleep(1)
    print(f"\nCongratulations {player.name}! \nYou completed the adventure at level {player.level}!")


game()
