# Overview

This is a choose your own adventure game built in Python. In this game, the player will be able to pick which path they choose as they move through the 10x10 dungeon. Each room has a different encounter based on the random number generator, which decides which event or monster will be placed into each room as the player reaches it.
The program is built around linked lists and classes, which made it easy to setup each event and monster and will make it very easy in the future to add upon the foundation of the game.

I have actually made a choose your own adventure game in Python before, but it was both not as complex as this one and also more difficult to test and maintain. This is because I used a lot of if statements and while loops to make the game work, which made it very difficult to add upon the game as it progressed. This time, I used classes and linked lists to make the game more modular and easier to add upon.

[Software Demo Video](https://www.loom.com/share/d74f4058df9e4553b08390d556123d5a)

# Development Environment

For building this program, I used Visual Studio Code and Python. I used the Python extension in VS Code to run the program.

The only libraries I used were the random library and the time library. The random library was used to determine the encounter
in each room as well as the damage output of the player and the enemy. The time library was used to make the game more interactive
by having the text appear on screen more slowly, which makes the game feel more like a text adventure.

# Useful Websites

{Make a list of websites that you found helpful in this project}

- [Tutorials Point](https://www.tutorialspoint.com/python_data_structure/python_linked_lists.htm)
- [W3Schools](https://www.w3schools.com/python/)
- [Medium](https://angellom.medium.com/writing-a-python-dungeon-game-part-i-47e35668f16b)

# Future Work

- Add GUI to make the game more interactive
- Add more monsters and events to make the game more interesting
- Add more paths and more path restrictions to make the game more complex instead of just an open 10x10 grid