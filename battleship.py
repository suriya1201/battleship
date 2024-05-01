import os

alphabets = ["A","B","C","D","E","F","G","H","I","J","K","L","M"]

def setrowandcolumn():
    global rows
    while True:
        try:
            rows = int(input("Enter number of rows and columns: "))
            if rows < 11 and rows > 4:
                break
            else:
                print("Rows must be between 5 and 10.")
        except ValueError:
            print("Invalid number of rows")

def setships():
    global cruisers, destroyers, battleships
    while True:
        try:
            cruisers = int(input("Enter number of cruisers (1 to 5): "))
            if cruisers < 6 and cruisers > 0:
                break
            else:
                print("Number of cruisers must be between 1 and 5.")
        except ValueError:
            print("Invalid number of cruisers.")
    while True:
        try:
            destroyers = int(input("Enter number of destroyers (0 to 3): "))
            if destroyers < 4 and destroyers >= 0:
                break
            else:
                print("Number of destroyers must be between 0 and 3.")
        except ValueError:
            print("Invalid number of destroyers.")
    while True:
        try:
            battleships = int(input("Enter number of battleships (0 to 2): "))
            if battleships < 3 and battleships >= 0:
                break
            else:
                print("Number of battleships must be between 0 and 2.")
        except ValueError:
            print("Invalid number of battleships.")


def createvalidoptions():
    validoptions=[]
    for i in alphabets[:rows]:
        j = 0
        while j < rows:
            validoptions.append(i+str(j+1))
            j += 1
    return validoptions


def createboard():
    shipboard = []
    i = 0
    while i < rows:
        j = 0
        row = []
        while j < rows:
            row.append("-")
            j += 1
        shipboard.append(row)
        i+=1
    return shipboard

def createcruisers(Player,shipboard):
    i = 1
    validoptions=createvalidoptions()
    while i < (cruisers+1):
        print(Player)
        print("Choose the location of {} Cruiser(s): ".format(cruisers))
        PrintGrid(shipboard)
        spot = input("Cruiser {}: ".format(str(i)))
        if spot in validoptions and spot not in location:
            shipboard[alphabets.index(spot[0])][int(spot[-1])-1]="X"

            location.append(spot)
            i += 1
            os.system("cls")
        else:
            os.system("cls")
            print("Invalid Option")

def createdestroyers(Player,shipboard):
    i = 1
    validoptions=createvalidoptions()
    while i < (destroyers+1):
        print(Player)
        print("Choose the location of {} Destoyer(s): ".format(cruisers))
        PrintGrid(shipboard)
        spot = input("Destroyer {}: ".format(str(i)))
        while True:
            orientation = input("Orientation of Destroyer {} (H: Horizontal, V: Vertical): ".format(str(1)))
            if orientation == "H":
                spot2 = spot[0]+str(int(spot[1:])+1)
                break
            elif orientation == "V":
                spot2 = alphabets[alphabets.index(spot[0])+1]+spot[1:]
                break
            else:
                print("Invalid Orientation")
        if spot in validoptions and spot not in location \
                and spot2 in validoptions and spot2 not in location:
            shipboard[alphabets.index(spot[0])][int(spot[1:])-1]="X"
            shipboard[alphabets.index(spot2[0])][int(spot2[1:])-1]="X"
            location.append(spot)
            location.append(spot2)
            i += 1
            os.system("cls")
        else:
            os.system("cls")
            print("Invalid Option")

def createbattleships(Player,shipboard):
    i = 1
    validoptions=createvalidoptions()
    while i < (battleships+1):
        print(Player)
        print("Choose the location of {} Battleship(s): ".format(cruisers))
        PrintGrid(shipboard)
        spot = input("Battleship {}: ".format(str(i)))
        orientation = input("Orientation of Battleship {} (H: Horizontal, V: Vertical): ".format(str(1)))
        while True:
            if orientation == "H":
                spot2 = spot[0]+str(int(spot[1:])+1)
                spot3 = spot[0]+str(int(spot[1:])+2)
                break
            elif orientation == "V":
                spot2 = alphabets[alphabets.index(spot[0])+1]+spot[1:]
                spot3 = alphabets[alphabets.index(spot[0])+2]+spot[1:]
                break
            else:
                print("Invalid Orientation")
        if spot in validoptions and spot not in location \
                and spot2 in validoptions and spot2 not in location \
                and spot3 in validoptions and spot3 not in location:
            shipboard[alphabets.index(spot[0])][int(spot[1:])-1]="X"
            shipboard[alphabets.index(spot2[0])][int(spot2[1:])-1]="X"
            shipboard[alphabets.index(spot3[0])][int(spot3[1:])-1]="X"
            location.append(spot)
            location.append(spot2)
            location.append(spot3)
            i += 1
            os.system("cls")
        else:
            os.system("cls")
            print("Invalid Option")

def createshipboard(Player):
    global location
    location = []
    os.system("cls")
    shipboard=createboard()
    createcruisers(Player,shipboard)
    createdestroyers(Player,shipboard)
    createbattleships(Player,shipboard)
    return shipboard

def PrintGrid(playerboard):
    TopLabel = ""
    i=1
    while i <= len(playerboard):
        TopLabel += "    "+str(i)
        i += 1
    i = 0
    print(TopLabel)

    while i < len(playerboard):
        string = "  "
        for j in playerboard[i]:
            string += j + "    "
        print(alphabets[i],string)
        i += 1

def PlayerAttack(player, playershipboard, playerattackboard, opponentshipboard):
    Attacking = True
    validoptions=createvalidoptions()
    while Attacking == True:
        os.system("cls")
        print(player)
        print("Ships")
        PrintGrid(playershipboard)
        print("Attack")
        PrintGrid(playerattackboard)

        Target = input("Enter a location to attack: ")

        if Target not in validoptions:
            print("Invalid Target")
            input("Press Enter to continue...")
        else:
            TargetStatus = opponentshipboard[alphabets.index(Target[0])][int(Target[-1])-1]
            PlayerAttackStatus = playerattackboard[alphabets.index(Target[0])][int(Target[-1])-1]
            if TargetStatus=="0" or PlayerAttackStatus=="M":
                print("Invalid Target")
                input("Press Enter to continue...")
            elif opponentshipboard[alphabets.index(Target[0])][int(Target[-1])-1]=="X":
                print("You have hit your target.")
                input("Press Enter to continue...")
                opponentshipboard[alphabets.index(Target[0])][int(Target[-1])-1]="0"
                playerattackboard[alphabets.index(Target[0])][int(Target[-1])-1]="H"
                if OpponentAlive(opponentshipboard, player) != "ongoing":
                    break
                os.system("cls")
            else:
                os.system("cls")
                print("You missed...")
                input("Press Enter to continue...")
                playerattackboard[alphabets.index(Target[0])][int(Target[-1])-1]="M"
                Attacking = False
    return OpponentAlive(opponentshipboard,player)

def OpponentAlive(opponentshipboard, player):
    alive = False
    for i in opponentshipboard:
        if "X" in i:
            alive = True
        else:
            continue
    if alive == True:
        return "ongoing"
    else:
        return player

def gamestart(player1shipboard, player1attackboard, player2shipboard, player2attackboard):
    status = "ongoing"
    while status == "ongoing":
        status = PlayerAttack("Player 1",player1shipboard,player1attackboard,player2shipboard)
        if status == "ongoing":
            status = PlayerAttack("Player 2",player2shipboard,player2attackboard,player1shipboard)
    print("{} won.".format(status))

def main():
    setrowandcolumn()
    setships()
    player1shipboard=createshipboard("Player 1")
    player1attackboard = createboard()
    player2shipboard=createshipboard("Player 2")
    player2attackboard = createboard()
    gamestart(player1shipboard,player1attackboard,player2shipboard,player2attackboard)

if __name__=="__main__":
    main()
