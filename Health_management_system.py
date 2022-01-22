"""This program is written to ease a trainer or someone who prefers some serious exercise and diet routines, One can record logs of upto three persons using this program, this program creates two txt files and stores the records, you can add the records and also see the time when you wrote that."""
# Coded by :- Prasoon Tripathi
"""You can change the name at just the starting and that will change the names throughout the program, you just have to change at first."""
import time # To make breaks between statements so that one can read nicely.
import datetime # To record date and time when someone makes changes to the logs.
name1 = "Manas" # You can change the first name.
name2 = "Achyut" # You can change the second name.
name3 = "Hritikh" # You can change the third name.
def cho(): # This function makes the choices of either to exit or write again.
    print("Press Y/y to write again or N/n to exit!!")
    choi = input() # Takes the user input.
    choi = choi.lower()
    if choi == "y":
        optionss()
    elif choi == "n":
        print("GOOD BYE!!")
        time.sleep(1)
def getdate():
    return datetime.datetime.now() # Returns the date and timne.
def optionss():
    print("Press 1 for", name1, ", Press 2 for", name2, ", Press 3 for", name3)
    opt = int(input())
    # Choice 1 , to select the first user i.e., the name stored in name1 variable.
    if opt == 1:
        print(name1, "Folder")
        print("Press 1 for accessing diet, Press 2 for accessing exercise")
        aces = int(input())
        # To read or write in the diet folder.
        if aces == 1:
            print("You have opened Diet Folder!")
            print("Press 1 to write, Press 2 to see the log")
            ope = int(input())
            # To write in the diet folder.
            if ope == 1:
                print("Now you can start to write!")
                with open (name1, " diet folder.txt", "a") as f: # Opens the folder for reading and writing.
                    a = input()
                    b = str(getdate())
                    e = f.write(a + " " + b + "\n ")
                    time.sleep(1)
                    cho()
            # To read in the diet folder.
            elif ope == 2:
                print("You are reading logs!")
                with open (name1, " diet folder.txt", "r") as f: # Opens the folder for reading and writing.
                    a = f.readlines()
                    print(a)
                    time.sleep(1)
                    cho()
        # To read or write in the exercise folder.
        elif aces == 2:
            print("You have opened Exercise Folder!!")
            print("Press 1 to write, Press 2 to see the log")
            ope = int(input())
            # To write in the diet folder.
            if ope == 1:
                print("Now you can start to write!")
                with open (name1, " Exercise folder.txt", "a") as f: # Opens the folder for reading and writing.
                    a = input()
                    b = str(getdate())
                    e = f.write(a + " " + b + "\n ")
                    time.sleep(1)
                    cho()
            # To read in the diet folder.
            elif ope == 2:
                print("You are reading logs!")
                with open (name1, " Exercise folder.txt", "r") as f: # Opens the folder for reading and writing.
                    a = f.readlines()
                    print(a)
                    time.sleep(1)
                    cho()
    # Choice 2 , to select the Second user i.e., the name stored in name2 variable.
    elif opt == 2:
        print(name2, "Folder")
        print("Press 1 for accessing diet, Press 2 for accessing exercise")
        aces = int(input())
        # To read or write in the diet folder.
        if aces == 1:
            print("You have opened Diet Folder!!")
            print("Press 1 to write, Press 2 to see the log")
            ope = int(input())
            # To write in the diet folder.
            if ope == 1:
                print("Now you can start to write!")
                with open (name2, "diet folder.txt", "a") as f: # Opens the folder for reading and writing.
                    a = input()
                    b = str(getdate())
                    e = f.write(a + " " + b + "\n ")
                    time.sleep(1)
                    cho()
            # To read in the diet folder.
            elif ope == 2:
                print("You are reading logs!")
                with open (name2, " bdiet folder.txt", "r") as f: # Opens the folder for reading and writing.
                    a = f.readlines()
                    print(a)
                    time.sleep(1)
                    cho()
        # To read or write in the exercise folder.
        elif aces == 2:
            print("You have opened Exercise Folder!!")
            print("Press 1 to write, Press 2 to see the log")
            ope = int(input())
            # To write in the diet folder.
            if ope == 1:
                print("Now you can start to write!")
                with open (name2, " Exercise folder.txt", "a") as f: # Opens the folder for reading and writing.
                    a = input()
                    b = str(getdate())
                    e = f.write(a + " " + b + "\n ")
                    time.sleep(1)
                    cho()
            # To read in the diet folder.
            elif ope == 2:
                print("You are reading logs!")
                with open (name2," Exercise folder.txt", "r") as f: # Opens the folder for reading and writing.
                    a = f.readlines()
                    print(a)
                    time.sleep(1)
                    cho()
    # Choice 3 , to select the Third user i.e., the name stored in name3 variable.
    elif opt == 3:
        print(name3, "folder")
        print("Press 1 for accessing diet, Press 2 for accessing exercise")
        aces = int(input())
        # To read or write in the diet folder.
        if aces == 1:
            print("You have opened Diet Folder!!")
            print("Press 1 to write, Press 2 to see the log")
            ope = int(input())
            # To write in the diet folder.
            if ope == 1:
                print("Now you can start to write!")
                with open (name3, " diet folder.txt", "a") as f: # Opens the folder for reading and writing.
                    a = input()
                    b = str(getdate())
                    e = f.write(a + " " + b + "\n ")
                    time.sleep(1)
                    cho()
             # To read in the diet folder.
            elif ope == 2:
                print("You are reading logs!")
                with open (name3, " diet folder.txt", "r") as f: # Opens the folder for reading and writing.
                    a = f.readlines()
                    print(a)
                    time.sleep(1)
                    cho()
        # To read or write in the exercise folder.
        elif aces == 2:
            print("You have opened Exercise Folder!!")
            print("Press 1 to write, Press 2 to see the log")
            ope = int(input())
             # To write in the diet folder.
            if ope == 1:
                with open (name3, " Exercise folder.txt", "a") as f: # Opens the folder for reading and writing.
                    a = input()
                    b = str(getdate())
                    e = f.write(a + " " + b + "\n ")
                    time.sleep(1)
                    cho()
             # To read in the diet folder.
            elif ope == 2:
                print("You are reading logs!")
                with open (name3, " Exercise folder.txt", "r") as f: # Opens the folder for reading and writing.
                    a = f.readlines()
                    print(a)
                    time.sleep(1)
                    cho()
    else:
        print("Wrong try again!!")
        optionss()
getdate()
optionss()