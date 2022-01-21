# Snake drinks Water, Water submerge Gun, Gun kills the Snake
# Created by :- Prasoon Tripathi
"""This Game plays Snake Water Gun with you if you dont know whats Snake Water Gun, well then google it or simply think it like Rock Paper Scissors. Well if you dont even know Rock Paper Scissors then Google it I cant help you Enough.""" 
""""P.S. By just changing the name Snake Water Gun in two places (Marked with **) and you can write whatever game you want to play for e.g. you can Write Rock paper scissors and you can play that game"""
import time # Imports time Module, we need this module for time intervals.
import random # Imports random Module, we need this module to select random choices.
a = ["snake", "water", "gun"] # index a[0] > a[1], a[1] > a[2], a[2] > a[0] **here you can write any other names to change snake water gun
win_count = 0 # Counts the number of wins.
lose_count = 0  # Counts the number of losses.
draw_count = 0 # Counts the number of draws.
while True:
    b = random.randint(0,2) # Chooses randomely between 0 to 2
    print("Type Your choice or press Z to Reset or press X to quit")
    time.sleep(0.5)
    print("Snake Water Gun!")
    c = input() # **here you can change whatever name of the game you want
    c = c.lower() # Coverts all the alphabets to lower alphabets
    # LOSING TO COMP :(
    if a[b] == a[0] and c == a[1]:
        print("HaHa you lose!...because I had ==>", a[b])
        lose_count = lose_count + 1
    elif a[b] == a[1] and c == a[2]:
        print("HaHa you lose!...because I had ==>", a[b])
        lose_count = lose_count + 1
    elif a[b] == a[2] and c == a[0]:
        print("HaHa you lose!...because I had ==>", a[b])
        lose_count = lose_count + 1
    # WINNING FROM COMP :)
    elif a[b] == a[0] and c == a[2]:
        print("Aww! I lost :( ...I had ==>", a[b])
        win_count = win_count + 1
    elif a[b] == a[1] and c == a[0]:
        print("Aww! I lost :( ...I had ==>", a[b])
        win_count = win_count + 1
    elif a[b] == a[2] and c == a[1]:
        print("Aww! I lost :( ...I had ==>", a[b])
        win_count = win_count + 1
    # DRAW :|
    elif a[b] == a[0] and c == a[0]:
        print("Hey! you cheat! i also had ==>", a[b])
        draw_count = draw_count + 1
    elif a[b] == a[1] and c == a[1]:
        print("Hey! you cheat! i also had ==>", a[b])
        draw_count = draw_count + 1
    elif a[b] == a[2] and c == a[2]:
        print("Hey! you cheat! i also had ==>", a[b])
        draw_count = draw_count + 1
    # Choices to reset or quit
    elif c == "z": # To Reset :()
        print("Yayyy! lets play again!!!!")
        time.sleep(1)
        win_count = 0 
        lose_count = 0
        draw_count = 0
    elif c == "x": # To Quit :((
        print("Aww :( we were having so much fun!!......Bye")
        time.sleep(1)
        break
    time.sleep(1)
    print("Here is the summary, Wins ==>", win_count, "Losses ==>", lose_count, "Draws ==>", draw_count)
# print(c)
# print(a[b])