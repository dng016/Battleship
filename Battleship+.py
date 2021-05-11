# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import random
import string
import numpy as np

users = {}
selection = ""

#function to show the displaymenu
def displayMenu():
    global selection
    #prompt the users to make a selection 
    #Choose 1 for login 
    #Choose 2 for creating a new account
    #Reprompt the user if the user selects anything else
    
    print("\nWelcome to the game of Battleship!")
    print("1. Login")
    print("2. Create Account")
    selection = input("Enter your selection. Press q to quit:")
    if selection == '1':
        login()
    elif selection == '2':
        createAccount()
    elif selection == 'q':
        print("Program terminated!")
    else:
        displayMenu()

#function to check whether the input password from user during account creation satisfies all the criterias or not
def password_Checker(newPassword):
    #Check whether the password contains:
    # - At least 8 to 12 characters
    # - Alphabets must be between a-z
    # - At least one alphabet should be in Uppercase A-Z
    # - At least 1 number or digit between 0-9
    # - At least 1 character from [_ or @ or $ or ! or #]
    #Set password length to be minimum of 8 Characters
    
    LENGTH = 8
    upCase = False
    lowCase = False 
    digit = False
    specialSymbols = ['$','@', '_', '#', '!']
    symbols = False
    
    for char in newPassword:
        if char.isupper():
            upCase = True
        if char.islower():
            lowCase = True
        if char.isdigit():
            digit = True
        if char in specialSymbols:
            symbols = True
    
    length = len(newPassword)
    
    strong = upCase and lowCase and digit and length >= LENGTH and symbols
    if strong:
        print('Password is strong!')
        return True               
    else:
        print('Password is weak')
        print("Password should contain at least 8 to 12 characters.")
        print("Password should contain the alphabets must be between a-z.")
        print("Password should contain at least one alphabet should be in Uppercase A-Z.")
        print("Password should contain at least 1 number or digit between 0-9.")
        print("Password should contain at least 1 character from [_ or @ or $ or ! or #].")
        displayMenu()
        
                                                                
#function for user to create account        
def createAccount():
    # Prompt the users to create a username
    newUserName = input("Create Username: ")
    #Checks if new username has already been used. If username has been used, make use of the return function to stop the function
    if check_username(newUserName) == False:
        displayMenu()
        return
    #Prompt users to create a password
    #The password will be validate in the password_Checker function above
    #If the passwaord pass all the criteria, the system will then saved the username with the respective password
    newPassword = input("Create Password: ")
    if password_Checker(newPassword) == True:
        users[newUserName] = newPassword
        #stores username and password into a file
        storeACCinfo(newUserName, newPassword)
        print("User Created")
        displayMenu()
            

#function for user to login
def login():
    #Check if file that save account info exist or not. If does not exist, prompt user to go create account.
    try:
        with open("Accinfo.txt", "r") as savefile:
            read_file = savefile.read()
            savefile.close()
    except FileNotFoundError:
        print("No accounts found! Please go create account before attempting to login!")
        displayMenu()
        return
    
    #If file exist, prompt the users to enter the username and password
    login = input("Enter Username: ")
    password = input("Enter Password: ")
    
    #Check whether the username exist in the file
    #If username exist, check corresponding password. If not, prompt user that username does not exist
    myfile = open("ACCinfo.txt", "r")
    with myfile as savefile:
                for line in savefile:
                    eachline = line.split()                #separates each line of of text in the file
                    storedusername = eachline[0]           #stores the 1st element of each line (i.e username) into the storedusername variable
                    storedpw = eachline[1]                 #stores the 2nd element of each line (i.e password) into the storedpw variable
                    users[storedusername] = storedpw       #adds the corresponding username and password as keys and values into the dictionary called users that was created 1st line of code

    count = 0
    #Iterate through the save file to find corresponding username and password.
    for key,value in users.items():
        if login == key and password == value:
            print("Login Successful!")
            #Breaks out of for loop to proceed to game if username and password is both correct
            startgame()
            break
            
        count = count + 1
                
    if count == len(users):
        print("Invalid username or password!")
        displayMenu()


#checks if username during creation have been used already or not
def check_username(username):
    #check if a file to save username and password exist or not
    #creates a ACCinfo.txt file if there is no file
    try:
        with open("Accinfo.txt", "r") as savefile:
            read_file = savefile.read()
            savefile.close()
    except FileNotFoundError:
            savefile = open("Accinfo.txt", "w+")
            savefile.close()
            
    myfile = open("ACCinfo.txt", "r")
    with myfile as savefile:
                for line in savefile:
                    eachline = line.split()                #separates each line of of text in the file
                    storedusername = eachline[0]           #stores the 1st element of each line (i.e username) into the storedusername variable
                    storedpw = eachline[1]                 #stores the 2nd element of each line (i.e password) into the storedpw variable
                    users[storedusername] = storedpw       #adds the corresponding username and password as keys and values into the dictionary called users that was created 1st line of code
    for key in users:
        if username == key:
            print("Username has been used!", end = "\n")
            return False

#Saves created username and password into the ACCinfo file
def storeACCinfo(uname, pw):
    myfile = open("ACCinfo.txt", "a+")
    print(uname + " " + pw, file = myfile, end = "\n")
    myfile.close()


#make use of lists to create the boards required for the game
board_comp_surface=[]
for x in range(10):
    board_comp_surface.append([" |"] * 10)
board_comp_subsea=[]
for x in range(10):
    board_comp_subsea.append([" |"] * 10)
board_user_surface=[]
for x in range(10):
    board_user_surface.append([" |"] * 10)
board_user_subsea=[]
for x in range(10):
    board_user_subsea.append([" |"] * 10)
board_comp_surface_userp=[]
for x in range(10):
    board_comp_surface_userp.append([" |"] * 10)
board_comp_subsea_userp=[]
for x in range(10):
    board_comp_subsea_userp.append([" |"] * 10)
        
    
#print the layout of the board
def print_board(layer,board):
    #columns_names = ['A','B','C','D','E','F','G','H','I','J']

    print(layer)
    print (' ','  '.join(str(x) for x in range(1,11)))
    print('---------------------------------')
    for letter,row in zip('ABCDEFGHIJ',board):
        print(letter+'|', " ".join(row))
        print('---------------------------------')
        
#function to allow user to place their ships   
def user_place_ships():
    while True:
        #input coordinates of carrier
        print("Placing a/an carrier (Can only be placed on surface layer)")
        print("Please enter coordinates following this format (row,col). E.g.A,4")
        try:
            user_carrier_row,user_carrier_col=input("Please enter placement coordinates for carrier(row,col): ").split(",")
            user_carrier_row=user_carrier_row.upper()
            user_carrier_col=int(user_carrier_col)
            
        #to catch the error input of coordinates
        except ValueError:
            print('\nThe format is wrong!\n')
            continue
        if user_carrier_row not in string.ascii_uppercase[:10]:
            print('\nPlease enter the row from A to J(no case sensitive)!\n')
        elif user_carrier_col not in [1,2,3,4,5,6,7,8,9,10]:
            print('\nPlease enter the col number from 1 to 10 in integer\n')
        else:
            break
        #input direction of carrier
    while True:
        print("Note: direction in the format of 1 for up, 2 for down, 3 for left,4 for right")
        
        try:            
            user_carrier_dir=int(input("Please enter the direction of carrier's head: "))
        except ValueError:
            print("\nThe format is wrong, please enter an integer!\n")
            continue
         #catch the error input of direction and check the   
        if user_carrier_dir not in [1,2,3,4]:
            print("\nPlease select correct direction: 1,2,3,4\n")
        elif user_carrier_row in string.ascii_uppercase[:3] and user_carrier_dir==1:
            print("\nThere is no space for carrier to head up! Please select other direction\n")
        elif user_carrier_row in string.ascii_uppercase[7:10] and user_carrier_dir==2:
            print("\nThere is no space for carrier to head down! Please select other direction\n")
        elif user_carrier_col in [1,2,3] and user_carrier_dir==3:
            print("\nThere is no space for carrier to head left! Please select other direction\n")
        elif user_carrier_col in [8,9,10] and user_carrier_dir==4:
            print("\nThere is no space for carrier to head right! Please select other direction\n")
        else:
            break
    #print user carrier location on user board
    if user_carrier_dir==1:                 # UP
        for i in range(4):
            board_user_surface[ord(user_carrier_row)%32-1-i][user_carrier_col-1]="C|"
        print_board('User surface',board_user_surface)
    if user_carrier_dir==2:                 # Down
        for i in range(4):
            board_user_surface[ord(user_carrier_row)%32-1+i][user_carrier_col-1]="C|"
        print_board('User surface',board_user_surface)
    if user_carrier_dir==3:                 # Left
        for i in range(4):
            board_user_surface[ord(user_carrier_row)%32-1][user_carrier_col-1-i]="C|"
        print_board('User surface',board_user_surface)
    if user_carrier_dir==4:                 # Right
        for i in range(4):
            board_user_surface[ord(user_carrier_row)%32-1][user_carrier_col-1+i]="C|"
        print_board('User surface',board_user_surface)

    test = True     
    while test:
        #input coordinates for submarine
        print("Placing a/an submarine(Can be placed in depth:0,1)")
        print("Please enter coordinates following this format (row,col, depth). E.g.A,4,1")
        print("Note: depth = 0 represents the surface layer, and depth = 1 represents the subsea layer")
        #to catch the error input of coordinates
        try:
           
           user_submarine_row,user_submarine_col,user_submarine_layer=input("Please enter placement coordinates for submarine(row,col,depth): ").split(",")
           user_submarine_row=user_submarine_row.upper()
           user_submarine_col=int(user_submarine_col)
           user_submarine_layer=int(user_submarine_layer)
           
        except ValueError:
            print('\nThe format is wrong!\n')
            continue
        if user_submarine_row not in string.ascii_uppercase[:10]:
            print('\nPlease enter the row from A to J(no case sensitive)!\n')
        elif user_submarine_col not in [1,2,3,4,5,6,7,8,9,10]:
            print('\nPlease enter the col number from 1 to 10 in integer\n')
        elif user_submarine_layer not in [0,1]:
            print('\nPlease enter the 0 or 1 for layer\n')
            

        print("Note: direction in the format of 1 for up, 2 for down, 3 for left,4 for right")
        #input direction of submarine
        try:            
            user_submarine_dir=int(input("Please enter the direction of submarine's head: "))
        #catch errors for invalid input of submarine direction
        except ValueError:
            print("\nThe format is wrong, please enter an integer!\n")
            user_submarine_dir=int(input("Please enter the direction of submarine's head: "))
        
        #catch the error input of direction when submarine is placed at subsea layer
        if user_submarine_layer==1:
            if user_submarine_dir not in [1,2,3,4]:
                print("\nPlease select correct direction: 1,2,3,4\n")
            elif user_submarine_row in string.ascii_uppercase[:2] and user_submarine_dir==1:
                print("\nThere is no space for submarine to head up! Please select other direction\n")
            elif user_submarine_row in string.ascii_uppercase[8:10] and user_submarine_dir==2:
                print("\nThere is no space for submarine to head down! Please select other direction\n")
            elif user_submarine_col in [1,2] and user_submarine_dir==3:
                print("\nThere is no space for submarine to head left! Please select other direction\n")
            elif user_submarine_col in [9,10] and user_submarine_dir==4:
               print("\nThere is no space for submarine to head right! Please select other direction\n")
            else:
                break
        
        #catch error input when submairine is placed at surface layer
        elif user_submarine_layer==0:
            if user_submarine_dir not in [1,2,3,4]:
                print("\nPlease select correct direction: 1,2,3,4\n")
            elif user_submarine_row in string.ascii_uppercase[:2] and user_submarine_dir==1:
                print("\nThere is no space for submarine to head up! Please select other direction\n")
            elif user_submarine_row in string.ascii_uppercase[8:10] and user_submarine_dir==2:
                print("\nThere is no space for submarine to head down! Please select other direction\n")
            elif user_submarine_col in [1,2] and user_submarine_dir==3:
                print("\nThere is no space for submarine to head left! Please select other direction\n")
            elif user_submarine_col in [9,10] and user_submarine_dir==4:
               print("\nThere is no space for submarine to head right! Please select other direction\n")

            elif user_submarine_dir==1:
                for i in range(3):
                    if board_user_surface[ord(user_submarine_row)%32-1-i][user_submarine_col-1]=="C|":
                        print("\nInvalid input! Submarine will overlap with carrier!\n")
                        break
                    elif i==2:
                        test = False

            elif user_submarine_dir==2:
                for i in range(3):
                    if board_user_surface[ord(user_submarine_row)%32-1+i][user_submarine_col-1]=="C|":
                        print("\nInvalid input! Submarine will overlap with carrier!\n")
                        break
                    elif i==2:
                        test = False

            elif user_submarine_dir==3:
                for i in range(3):
                    if board_user_surface[ord(user_submarine_row)%32-1][user_submarine_col-1-i]=="C|":
                        print("\nInvalid input! Submarine will overlap with carrier!\n")
                        break
                    elif i==2:
                        test = False

            elif user_submarine_dir==4:
                for i in range(3):
                    if board_user_surface[ord(user_submarine_row)%32-1][user_submarine_col-1+i]=="C|":
                        print("\nInvalid input! Submarine will overlap with carrier!\n")
                        break
                    elif i==2:
                        test = False
            
    #print user submarine on user board
    if user_submarine_layer==0:

        if user_submarine_dir==1:
            for i in range(3):
                board_user_surface[ord(user_submarine_row)%32-1-i][user_submarine_col-1]="S|"
            print_board('User surface',board_user_surface)
        if user_submarine_dir==2:
            for i in range(3):
                board_user_surface[ord(user_submarine_row)%32-1+i][user_submarine_col-1]="S|"
            print_board('User surface',board_user_surface)
        if user_submarine_dir==3:
            for i in range(3):
                board_user_surface[ord(user_submarine_row)%32-1][user_submarine_col-1-i]="S|"
            print_board('User surface',board_user_surface)
        if user_submarine_dir==4:
            for i in range(3):
                board_user_surface[ord(user_submarine_row)%32-1][user_submarine_col-1+i]="S|"
            print_board('User surface',board_user_surface)
        
        
    else:    
        
        if user_submarine_dir==1:
            for i in range(3):
                board_user_subsea[ord(user_submarine_row)%32-1-i][user_submarine_col-1]="S|"
            print_board('User subsea',board_user_subsea)
        if user_submarine_dir==2:
            for i in range(3):
                board_user_subsea[ord(user_submarine_row)%32-1+i][user_submarine_col-1]="S|"
            print_board('User subsea',board_user_subsea)
        if user_submarine_dir==3:
            for i in range(3):
                board_user_subsea[ord(user_submarine_row)%32-1][user_submarine_col-1-i]="S|"
            print_board('User subsea',board_user_subsea)
        if user_submarine_dir==4:
            for i in range(3):
                board_user_subsea[ord(user_submarine_row)%32-1][user_submarine_col-1+i]="S|"
            print_board('User subsea',board_user_subsea)




#function to allow computer to place their ships
def computer_place_ships():
    #enemy's carrier placement
    while True:
        com_carrier_row=random.choice(string.ascii_uppercase[:10])
        com_carrier_col=random.randint(1,10)
        com_carrier_dir=random.randint(1,4)
        
        #consider the case of space issue to repeat loop if conditions not satisfied
        if com_carrier_row in string.ascii_uppercase[:3] and com_carrier_dir==1:
            continue
        elif com_carrier_row in string.ascii_uppercase[7:10] and com_carrier_dir==2:
            continue
        elif com_carrier_col in [1,2,3] and com_carrier_dir==3:
            continue
        elif com_carrier_col in [8,9,10] and com_carrier_dir==4:
            continue
        else:
            break 
    
    #assign computer selected carrier location on computer's board
    if com_carrier_dir==1:                 # UP
        for i in range(4):
            board_comp_surface[ord(com_carrier_row)%32-1-i][com_carrier_col-1]="C|"
    if com_carrier_dir==2:                 # Down
        for i in range(4):
            board_comp_surface[ord(com_carrier_row)%32-1+i][com_carrier_col-1]="C|"
    if com_carrier_dir==3:                 # Left
        for i in range(4):
            board_comp_surface[ord(com_carrier_row)%32-1][com_carrier_col-1-i]="C|"
    if com_carrier_dir==4:                 # Right
        for i in range(4):
            board_comp_surface[ord(com_carrier_row)%32-1][com_carrier_col-1+i]="C|"
    
        
    #enemy's submarine placement
    comtest = True
    while comtest:
        com_submarine_layer=random.randint(0,1)
        com_submarine_row=random.choice(string.ascii_uppercase[:10])
        com_submarine_col=random.randint(1,10)
        com_submarine_dir=random.randint(1,4)
        #consider space or overlap issue and let computer regenerate values until there is no space or overlap issues
        if com_submarine_layer==1:
            if com_submarine_row in string.ascii_uppercase[:2] and com_submarine_dir==1:
                continue
            elif com_submarine_row in string.ascii_uppercase[8:10] and com_submarine_dir==2:
                continue
            elif com_submarine_col in [1,2] and com_submarine_dir==3:
                continue
            elif com_submarine_col in [9,10] and com_submarine_dir==4:
               continue
            else:
                break
        elif com_submarine_layer==0:
            if com_submarine_row in string.ascii_uppercase[:2] and com_submarine_dir==1:
                continue
            elif com_submarine_row in string.ascii_uppercase[8:10] and com_submarine_dir==2:
                continue
            elif com_submarine_col in [1,2] and com_submarine_dir==3:
                continue
            elif com_submarine_col in [9,10] and com_submarine_dir==4:
               continue

            elif com_submarine_dir==1:
                for i in range(3):
                    if board_comp_surface[ord(com_submarine_row)%32-1-i][com_submarine_col-1]=="C|":
                        break
                    elif i==2:
                        comtest = False

            elif com_submarine_dir==2:
                for i in range(3):
                    if board_comp_surface[ord(com_submarine_row)%32-1+i][com_submarine_col-1]=="C|":
                        break
                    elif i==2:
                        comtest = False

            elif com_submarine_dir==3:
                for i in range(3):
                    if board_comp_surface[ord(com_submarine_row)%32-1][com_submarine_col-1-i]=="C|":
                        break
                    elif i==2:
                        comtest = False

            elif com_submarine_dir==4:
                for i in range(3):
                    if board_comp_surface[ord(com_submarine_row)%32-1][com_submarine_col-1+i]=="C|":
                        break
                    elif i==2:
                        comtest = False
        
    #assign computer selected submarine location on computer's board
    if com_submarine_layer==0:

        if com_submarine_dir==1:
            for i in range(3):
                board_comp_surface[ord(com_submarine_row)%32-1-i][com_submarine_col-1]="S|"
        if com_submarine_dir==2:
            for i in range(3):
                board_comp_surface[ord(com_submarine_row)%32-1+i][com_submarine_col-1]="S|"
        if com_submarine_dir==3:
            for i in range(3):
                board_comp_surface[ord(com_submarine_row)%32-1][com_submarine_col-1-i]="S|"
        if com_submarine_dir==4:
            for i in range(3):
                board_comp_surface[ord(com_submarine_row)%32-1][com_submarine_col-1+i]="S|"
        
        
    else:    
        
        if com_submarine_dir==1:
            for i in range(3):
                board_comp_subsea[ord(com_submarine_row)%32-1-i][com_submarine_col-1]="S|"
        if com_submarine_dir==2:
            for i in range(3):
                board_comp_subsea[ord(com_submarine_row)%32-1+i][com_submarine_col-1]="S|"
        if com_submarine_dir==3:
            for i in range(3):
                board_comp_subsea[ord(com_submarine_row)%32-1][com_submarine_col-1-i]="S|"
        if com_submarine_dir==4:
            for i in range(3):
                board_comp_subsea[ord(com_submarine_row)%32-1][com_submarine_col-1+i]="S|"

#function that keeps track of the user target locations during attack
def user_target():
    while True:
        #input coordinates of carrier
        print("Placing your target to attack enemy's ships")
        print("Please enter coordinates following this format (row,col). E.g.A,4,1")
        try:
            user_target_row,user_target_col,user_target_layer=input("Please enter placement coordinates to attack(row,col,layer): ").split(",")
            user_target_row=user_target_row.upper()
            user_target_col=int(user_target_col)
            user_target_layer=int(user_target_layer)
            
        #to catch the error input of coordinates
        except ValueError:
            print('The format is wrong!')
        
        if user_target_row not in string.ascii_uppercase[:10]:
            print('Please enter the row from A to J(no case sensitive)!')
        elif user_target_col not in [1,2,3,4,5,6,7,8,9,10]:
            print('Please enter the col number from 1 to 10 in integer')
        elif user_target_layer not in [0,1]:
            print('Please enter the 0 or 1 for layer')
        else:
            break   
        
    if user_target_layer==0:
        if ord(user_target_row)%32<2:
            if user_target_col<2:
                board_comp_surface[0][0]="X|"
                board_comp_surface_userp[0][0]="X|"
            elif user_target_col>9:
                board_comp_surface[0][9]="X|"
                board_comp_surface_userp[0][9]="X|"
            else:
                for j in range(3):
                    board_comp_surface[0][user_target_col-2+j]="X|"
                    board_comp_surface_userp[0][user_target_col-2+j]="X|"
                    
        elif ord(user_target_row)%32>9:
            if user_target_col<2:
                board_comp_surface[9][0]="X|"
                board_comp_surface_userp[9][0]="X|"
            elif user_target_col>9:
                board_comp_surface[9][9]="X|"
                board_comp_surface_userp[9][9]="X|"
            else:
                for j in range(3):
                    board_comp_surface[9][user_target_col-2+j]="X|"
                    board_comp_surface_userp[9][user_target_col-2+j]="X|"
        elif user_target_col<2:
            for i in range(3):
                board_comp_surface[ord(user_target_row)%32-2+i][0]="X|"
                board_comp_surface_userp[ord(user_target_row)%32-2+i][0]="X|"
        elif user_target_col>9:
            for i in range(3):
                board_comp_surface[ord(user_target_row)%32-2+i][0]="X|"
                board_comp_surface_userp[ord(user_target_row)%32-2+i][0]="X|"
        else:
            for i in range(3):
                for j in range(3):            
                    board_comp_surface[ord(user_target_row)%32-2+i][user_target_col-2+j]="X|"
                    board_comp_surface_userp[ord(user_target_row)%32-2+i][user_target_col-2+j]="X|"
    else:
        if ord(user_target_row)%32<2:
            if user_target_col<2:
                board_comp_subsea[0][0]="X|"
                board_comp_subsea_userp[0][0]="X|"
            elif user_target_col>9:
                board_comp_subsea[0][9]="X|"
                board_comp_subsea_userp[0][9]="X|"
            else:
                for j in range(3):
                    board_comp_subsea[0][user_target_col-2+j]="X|"
                    board_comp_subsea_userp[0][user_target_col-2+j]="X|"
                    
        elif ord(user_target_row)%32>9:
            if user_target_col<2:
                board_comp_subsea[9][0]="X|"
                board_comp_subsea_userp[9][0]="X|"
            elif user_target_col>9:
                board_comp_subsea[9][9]="X|"
                board_comp_subsea_userp[9][9]="X|"
            else:
                for j in range(3):
                    board_comp_subsea[9][user_target_col-2+j]="X|"
                    board_comp_subsea_userp[9][user_target_col-2+j]="X|"
        elif user_target_col<2:
            for i in range(3):
                board_comp_subsea[ord(user_target_row)%32-2+i][0]="X|"
                board_comp_subsea_userp[ord(user_target_row)%32-2+i][0]="X|"
        elif user_target_col>9:
            for i in range(3):
                board_comp_subsea[ord(user_target_row)%32-2+i][0]="X|"
                board_comp_subsea_userp[ord(user_target_row)%32-2+i][0]="X|"
        else:
            for i in range(3):
                for j in range(3):            
                    board_comp_subsea[ord(user_target_row)%32-2+i][user_target_col-2+j]="X|"
                    board_comp_subsea_userp[ord(user_target_row)%32-2+i][user_target_col-2+j]="X|"
                    
    
    #print target location for user perspective on the computers' surface and subsea boards without showing computer's placement of ships
    print_board('Computer Surface',board_comp_surface_userp)
    print_board('Computer Subsea',board_comp_subsea_userp)

#function that keeps track of the computer target locations during attack    
def comp_target():
    com_target_layer=random.randint(0,1)
    com_target_row=random.randint(0,len(board_comp_surface)-1)
    com_target_col=random.randint(0,len(board_comp_surface)-1)
    
    if com_target_layer==0:
        if com_target_row<1:
            if com_target_col<1:
                board_user_surface[0][0]="X|"
            elif com_target_col>8:
                board_user_surface[0][9]="X|"
            else:
                for j in range(3):
                    board_user_surface[0][com_target_col-1+j]="X|"
                    
        elif com_target_row>8:
            if com_target_col<1:
                board_user_surface[9][0]="X|"
            elif com_target_col>8:
                board_user_surface[9][9]="X|"
            else:
                for j in range(3):
                    board_user_surface[9][com_target_col-1+j]="X|"
        elif com_target_col<1:
            for i in range(3):
                board_user_surface[com_target_row-1+i][0]="X|"
        elif com_target_col>8:
            for i in range(3):
                board_user_surface[com_target_row-1+i][0]="X|"
        else:
            for i in range(3):
                for j in range(3):            
                    board_user_surface[com_target_row-1+i][com_target_col-1+j]="X|"
    else:
        if com_target_row<1:
            if com_target_col<1:
                board_user_subsea[0][0]="X|"
            elif com_target_col>8:
                board_user_subsea[0][9]="X|"
            else:
                for j in range(3):
                    board_user_subsea[0][com_target_col-1+j]="X|"
                    
        elif com_target_row>8:
            if com_target_col<1:
                board_user_subsea[9][0]="X|"
            elif com_target_col>8:
                board_user_subsea[9][9]="X|"
            else:
                for j in range(3):
                    board_user_subsea[9][com_target_col-1+j]="X|"
        elif com_target_col<2:
            for i in range(3):
                board_user_subsea[com_target_row-1+i][0]="X|"
        elif com_target_col>9:
            for i in range(3):
                board_user_subsea[com_target_row-1+i][0]="X|"
        else:
            for i in range(3):
                for j in range(3):            
                    board_user_subsea[com_target_row-1+i][com_target_col-2+j]="X|"
                    
    
    print_board('User Surface',board_user_surface)
    print_board('User Subsea',board_user_subsea)
    
#function that checks whether the winning condition of the game has been fulfilled or not    
def winning_condition(player):
    if player=='user':
        player_c=sum(sum(np.array(board_user_surface)=='C|'))
        player_s=sum(sum(np.array(board_user_surface)=='S|'))+sum(sum(np.array(board_user_subsea)=='S|'))
    elif player=='Enemy':
        player_c=sum(sum(np.array(board_comp_surface)=='C|'))
        player_s=sum(sum(np.array(board_comp_surface)=='S|'))+sum(sum(np.array(board_comp_subsea)=='S|'))
    else:
        print("Please put the correct player!")
    
    print("Current ",player,"'s ship status: ")
    print(player,"'s Carrier: left",player_c, " units")
    print(player,"'s Submarine: left",player_s, " units")
        
    if player_c == 0 and player_s == 0:
        status = 'WIN'
        return (status, player)
    elif player_c == player_c and player_s == player_s:
        status = 'Missed'
        return (status, player)
    else:
        status = 'Hit'
        return (status, player)
    

#function to start the game
def startgame():
    print_board('User surface' , board_user_surface)
    print_board('User subsea', board_user_subsea)
    
    user_place_ships()
    player_c=sum(sum(np.array(board_user_surface)=='C|'))
    player_s=sum(sum(np.array(board_user_surface)=='S|'))+sum(sum(np.array(board_user_subsea)=='S|'))
    print("Current User's ship status: ")
    print("User's Carrier: left",player_c, " units")
    print("User's Submarine: left",player_s, " units")
    
    computer_place_ships()
    player_c=sum(sum(np.array(board_comp_surface)=='C|'))
    player_s=sum(sum(np.array(board_comp_surface)=='S|'))+sum(sum(np.array(board_comp_subsea)=='S|'))
    print("Current Computer's ship status: ")
    print("Computer's Carrier: left:",player_c, " units")
    print("Computer's Submarine: left:",player_s, " units")

    while True:
        user_target()
        new_player_c=sum(sum(np.array(board_comp_surface)=='C|'))
        new_player_s=sum(sum(np.array(board_comp_surface)=='S|'))+sum(sum(np.array(board_comp_subsea)=='S|'))
        print("Current Computer's ship status: ")
        print("Computer's Carrier: left",new_player_c, " units")
        print("Computer's Submarine: left",new_player_s, " units")
        
        if new_player_c == 0 and new_player_s == 0:
            computer_status = 'WIN'
            print ('User', computer_status)  
        elif new_player_c == player_c and new_player_s == player_s:
            computer_status = 'Missed'
            print ('User', computer_status, end='\n\n')
        else:
            computer_status = 'HIT'
            print ('User', computer_status, end='\n\n')
        
        comp_target()
        new_player_c=sum(sum(np.array(board_user_surface)=='C|'))
        new_player_s=sum(sum(np.array(board_user_surface)=='S|'))+sum(sum(np.array(board_user_subsea)=='S|'))
        print("Current User's ship status: ")
        print("User's Carrier: left:",new_player_c, " units")
        print("User's Submarine: left:",new_player_s, " units")
        
        if new_player_c == 0 and new_player_s == 0:
            user_status = 'WIN'
            print ('Computer', user_status, end='\n\n')  
        elif new_player_c == player_c and new_player_s == player_s:
            user_status = 'Missed'
            print ('Computer', user_status, end='\n\n')
        else:
            user_status = 'HIT'
            print ('Computer', user_status, end='\n\n')
        
        if user_status == 'WIN':
            try_again = input('Do you want to play the game again? (y/n)')
            if try_again == 'y':
                boardcreation()
                startgame()
            else: 
                print('Thank you for playing Battleship')
                break
                
        if computer_status == 'WIN':
            try_again = input('Do you want to play the game again? (y/n)')
            if try_again == 'y':
                boardcreation()
                startgame()
            else: 
                print('Thank you for playing Battleship')
                break
    
#function to reset the boards during a new game        
def boardcreation():
    global board_comp_surface
    board_comp_surface=[]
    for x in range(10):
        board_comp_surface.append([" |"] * 10)
    global board_comp_subsea
    board_comp_subsea=[]
    for x in range(10):
        board_comp_subsea.append([" |"] * 10)
    global board_user_surface
    board_user_surface=[]
    for x in range(10):
        board_user_surface.append([" |"] * 10)
    global board_user_subsea
    board_user_subsea=[]
    for x in range(10):
        board_user_subsea.append([" |"] * 10)
    global board_comp_surface_userperspective
    board_comp_surface_userperspective=[]
    for x in range(10):
        board_comp_surface_userperspective.append([" |"] * 10)
    global board_comp_subsea_userperspective
    board_comp_subsea_userperspective=[]
    for x in range(10):
        board_comp_subsea_userperspective.append([" |"] * 10)


displayMenu()

