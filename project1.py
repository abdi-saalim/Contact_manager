#Adventure Game

name = input("Hey type your name: ")
print("Hello " + name + "," + " Welcome to my Adventure Game!")

#Asks the user if they want to play the game
should_we_play = input("Do you want to play? ").lower()

#Check if the user types in Yes or No
if should_we_play == "yes" or should_we_play == "y":
    print("We are going to play!")

    direction = input("Do you want to go left or right? (enter only left/right) ").lower()
    if direction == "left":
        print("Okay we went left, and fell off a cliff, game over, try again.")
    elif direction == "right": 
        choice = input("Okay now you see a bride, do you want to swim under it or cross it (enter only swim/cross)").lower()
        if choice == "swim":
            print("You got eaten by a shark, you die, the end!")
        else: 
            print("You crossed the bridge and found the gold, you won!")
    else:
        print("Sorry that is not a valid response, you die!")
else: 
    print("We are not going to play!")