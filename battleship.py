
import curses
import random


alphabets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]


def main(stdscr):
    # Turn on the visibility of typed characters
    curses.echo()
    # curses.curs_set(0)  # Hide the cursor
    stdscr.clear()  # Clear the terminal screen
    stdscr.refresh()

    # Setting the environment
    setrowandcolumn(stdscr)
    setships(stdscr)

    # Choosing the game mode either single or multiplayer
    mode = game_mode_selection(stdscr)

    # Creating boards for both players
    player1shipboard = createshipboard("Player 1", stdscr, False)
    player1attackboard = createboard()
    if mode == "multiplayer":
        player2shipboard = createshipboard("Player 2", stdscr, False)
    else:
        player2shipboard = createshipboard("Computer", stdscr, True)
    player2attackboard = createboard()

    # Start the game
    gamestart(
        player1shipboard,
        player1attackboard,
        player2shipboard,
        player2attackboard,
        stdscr,
        mode,
    )


def game_mode_selection(stdscr):
    stdscr.clear()  # Clear the screen at the beginning of each input prompt
    stdscr.addstr("Enter '1' for Single Player or '2' for Multiplayer: ")
    stdscr.refresh()
    mode = int(stdscr.getstr().decode().strip())
    if mode == 1:
        return "single"
    elif mode == 2:
        return "multiplayer"
    else:
        stdscr.addstr(25, 0, "Invalid selection. Defaulting to Single Player.")
        return "single"


def setrowandcolumn(stdscr):
    global rows
    while True:
        stdscr.addstr(0, 0, "Enter number of rows (5 to 10): ")
        stdscr.refresh()
        try:
            rows = int(stdscr.getstr().decode().strip())
            if 5 <= rows <= 10:
                break
            else:
                stdscr.addstr(1, 0, "Rows must be between 5 and 10.\n")
                stdscr.refresh()
        except ValueError:
            stdscr.addstr(1, 0, "Invalid number of rows\n")
            stdscr.refresh()


def setships(stdscr):
    global cruisers, battleships, destroyers
    while True:
        stdscr.clear()  # Clear the screen at the beginning of each input prompt
        stdscr.addstr(0, 0, "Enter number of cruisers (1 to 5): ")
        stdscr.refresh()
        try:
            cruisers = int(stdscr.getstr().decode("utf-8").strip())
            if 1 <= cruisers <= 5:
                break
            else:
                stdscr.addstr(1, 0, "Number of cruisers must be between 1 and 5.\n")
                stdscr.refresh()
        except ValueError:
            stdscr.addstr(1, 0, "Invalid number of cruisers.\n")
            stdscr.refresh()

    while True:
        stdscr.clear()  # Clear the screen at the beginning of each input prompt
        stdscr.addstr(0, 0, "Enter number of destroyers (0 to 3): ")
        stdscr.refresh()
        try:
            destroyers = int(stdscr.getstr().decode("utf-8").strip())
            if 0 <= destroyers <= 3:
                break
            else:
                stdscr.addstr(1, 0, "Number of destroyers must be between 0 and 3.\n")
                stdscr.refresh()
        except ValueError:
            stdscr.addstr(1, 0, "Invalid number of destroyers.\n")
            stdscr.refresh()

    while True:
        stdscr.clear()  # Clear the screen at the beginning of each input prompt
        stdscr.addstr(0, 0, "Enter number of battleships (0 to 2): ")
        stdscr.refresh()
        try:
            battleships = int(stdscr.getstr().decode("utf-8").strip())
            if 0 <= battleships <= 2:
                break
            else:
                stdscr.addstr(1, 0, "Number of battleships must be between 0 and 2.\n")
                stdscr.refresh()
        except ValueError:
            stdscr.addstr(1, 0, "Invalid number of battleships.\n")
            stdscr.refresh()

    #  display a confirmation message or the inputs
    stdscr.clear()
    stdscr.addstr(
        0,
        0,
        f"Cruisers: {cruisers}, Destroyers: {destroyers}, Battleships: {battleships}",
    )
    stdscr.refresh()
    stdscr.getch()  # Wait for the user to press a key


def createvalidoptions():
    validoptions = []
    for i in alphabets[:rows]:
        j = 0
        while j < rows:
            validoptions.append(i + str(j + 1))
            j += 1
    return validoptions


def PrintGrid(playerboard, stdscr, offset_y=0):
    TopLabel = ""
    for i in range(1, len(playerboard) + 1):
        TopLabel += "{:4}".format(i)
    stdscr.addstr(offset_y, 0, TopLabel)

    for idx, row in enumerate(playerboard):
        line = "{} ".format(alphabets[idx])
        for cell in row:
            # Check if the cell is part of a destroyer
            if cell == "X":
                # If it's the first or last cell of a destroyer, draw it as a corner
                if (
                    idx == 0
                    or idx == len(playerboard) - 1
                    or row.index(cell) == 0
                    or row.index(cell) == len(row) - 1
                ):
                    line += "{:4}".format("X")
                else:
                    # Otherwise, draw it as a part of the destroyer
                    line += "{:4}".format("X")
            else:
                line += "{:4}".format(cell)
        stdscr.addstr(offset_y + idx + 1, 0, line)
    stdscr.refresh()


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
        i += 1
    return shipboard


def random_placement_decision(validoptions, ship_size):
    while True:
        spot = random.choice(validoptions)
        orientation = random.choice(["H", "V"])
        return spot, orientation


def createcruisers(Player, shipboard, stdscr, is_computer=False):
    global location
    location = []
    i = 1
    validoptions = createvalidoptions()

    # Initialize ship position
    ship_row = 0
    ship_col = 0

    while i <= cruisers:
        stdscr.clear()  # Clear the screen
        if is_computer:
            spot = random.choice(validoptions)
            ship_row = alphabets.index(spot[0])
            ship_col = int(spot[1:]) - 1
            if spot in validoptions and spot not in location:
                # Update the shipboard with an 'X' at the current position
                shipboard[ship_row][ship_col] = "X"
                location.append(spot)
                i += 1  # Only increment if the placement is successful
            else:
                stdscr.addstr(
                    3 + len(shipboard),
                    0,
                    "Invalid option or already taken. Please try again.",
                )
                stdscr.refresh()
                stdscr.getch()  # Wait for user to acknowledge the error
        else:
            stdscr.addstr(0, 0, f"{Player}: Place your cruisers{is_computer}")
            PrintGrid(
                shipboard, stdscr, offset_y=2
            )  # Adjusted to pass offset_y to position the grid
            # Highlight the current ship position
            stdscr.addstr(3 + ship_row, 1 + ship_col * 4, "X", curses.color_pair(1))

            # Get user input
            key = stdscr.getch()

            # Move the ship based on the arrow key pressed
            if key == curses.KEY_UP and ship_row > 0:
                ship_row -= 1
            elif key == curses.KEY_DOWN and ship_row < len(shipboard) - 1:
                ship_row += 1
            elif key == curses.KEY_LEFT and ship_col > 0:
                ship_col -= 1
            elif key == curses.KEY_RIGHT and ship_col < len(shipboard[0]) - 1:
                ship_col += 1
            elif key == ord("\n"):  # Enter key to place the ship
                spot = alphabets[ship_row] + str(ship_col + 1)
                if spot in validoptions and spot not in location:
                    # Update the shipboard with an 'X' at the current position
                    shipboard[ship_row][ship_col] = "X"
                    location.append(spot)
                    i += 1  # Only increment if the placement is successful
                else:
                    stdscr.addstr(
                        3 + len(shipboard),
                        0,
                        "Invalid option or already taken. Please try again.",
                    )
                    stdscr.refresh()
                    stdscr.getch()  # Wait for user to acknowledge the error

    return shipboard


def createdestroyers(Player, shipboard, stdscr, is_computer=False):
    i = 1

    ship_row = 0
    ship_col = 0
    orientation = "horizontal"  # Start with horizontal orientation

    while i <= destroyers:
        stdscr.clear()  # Clear the screen
        if is_computer:
            # Computer's turn
            ship_row = random.randint(0, len(shipboard) - 1)
            ship_col = random.randint(0, len(shipboard[0]) - 1)
            orientation = random.choice(["horizontal", "vertical"])

            # Check if the position is valid
            if orientation == "horizontal" and ship_col <= len(shipboard[0]) - 2:
                if all(shipboard[ship_row][ship_col + j] == "-" for j in range(3)):
                    shipboard[ship_row][ship_col] = "<"
                    shipboard[ship_row][ship_col + 1] = "X"
                    shipboard[ship_row][ship_col + 2] = ">"
                    i += 1
            elif orientation == "vertical" and ship_row <= len(shipboard) - 2:
                if all(shipboard[ship_row + j][ship_col] == "-" for j in range(3)):
                    shipboard[ship_row][ship_col] = "∧"
                    shipboard[ship_row + 1][ship_col] = "X"
                    shipboard[ship_row + 2][ship_col] = "V"
                    i += 1
        else:
            stdscr.addstr(
                0,
                0,
                f"{Player}: Place your destroyer(s).(Use R key to rotate the ship)",
            )
            PrintGrid(
                shipboard, stdscr, offset_y=2
            )  # Adjusted to pass offset_y to position the grid

            # Highlight the current ship position based on orientation
            if orientation == "horizontal":
                stdscr.addstr(3 + ship_row, 1 + ship_col * 4, "<", curses.color_pair(1))
                stdscr.addstr(
                    3 + ship_row, 1 + (ship_col + 1) * 4, "X", curses.color_pair(1)
                )
                stdscr.addstr(
                    3 + ship_row, 1 + (ship_col + 2) * 4, ">", curses.color_pair(1)
                )
            else:  # Vertical orientation
                stdscr.addstr(3 + ship_row, 1 + ship_col * 4, "∧", curses.color_pair(1))
                stdscr.addstr(
                    3 + (ship_row + 1), 1 + ship_col * 4, "X", curses.color_pair(1)
                )
                stdscr.addstr(
                    3 + (ship_row + 2), 1 + ship_col * 4, "v", curses.color_pair(1)
                )

            # Get user input
            key = stdscr.getch()

            # Rotate the destroyer
            if key == ord("r") or key == ord("R"):
                orientation = (
                    "vertical" if orientation == "horizontal" else "horizontal"
                )
                stdscr.refresh()
                continue

            # Move the ship based on the arrow key pressed
            if key == curses.KEY_UP and ship_row > 0:
                ship_row -= 1
            elif (
                key == curses.KEY_DOWN and ship_row < len(shipboard) - 1
            ):  # Adjust for ship length
                ship_row += 1
            elif key == curses.KEY_LEFT and ship_col > 0:
                ship_col -= 1
            elif (
                key == curses.KEY_RIGHT and ship_col < len(shipboard[0]) - 1
            ):  # Adjust for ship length
                ship_col += 1
            elif key == ord("\n"):  # Enter key to place the ship
                # Check if the destroyer can be placed in the current orientation
                if orientation == "horizontal" and ship_col <= len(shipboard[0]) - 2:
                    if all(shipboard[ship_row][ship_col + j] == "-" for j in range(3)):
                        shipboard[ship_row][ship_col] = "<"
                        shipboard[ship_row][ship_col + 1] = "X"
                        shipboard[ship_row][ship_col + 2] = ">"
                        location.append(alphabets[ship_row] + str(ship_col + 1))
                        location.append(alphabets[ship_row] + str(ship_col + 2))
                        location.append(alphabets[ship_row] + str(ship_col + 3))
                        i += 1
                    else:
                        stdscr.addstr(
                            3 + len(shipboard),
                            0,
                            "Invalid option or already taken. Please try again.",
                        )
                        stdscr.refresh()
                        stdscr.getch()  # Wait for user to acknowledge the error
                elif orientation == "vertical" and ship_row <= len(shipboard) - 2:
                    if all(shipboard[ship_row + j][ship_col] == "-" for j in range(3)):
                        shipboard[ship_row][ship_col] = "∧"
                        shipboard[ship_row + 1][ship_col] = "X"
                        shipboard[ship_row + 2][ship_col] = "V"
                        location.append(alphabets[ship_row + 1] + str(ship_col + 1))
                        location.append(alphabets[ship_row + 2] + str(ship_col + 1))
                        location.append(alphabets[ship_row + 3] + str(ship_col + 1))
                        i += 1
                    else:
                        stdscr.addstr(
                            3 + len(shipboard),
                            0,
                            "Invalid option or already taken. Please try again.",
                        )
                        stdscr.refresh()
                        stdscr.getch()  # Wait for user to acknowledge the error
                else:
                    stdscr.addstr(
                        3 + len(shipboard),
                        0,
                        "Invalid option or already taken. Please try again.",
                    )
                    stdscr.refresh()
                    stdscr.getch()  # Wait for user to acknowledge the error

    return shipboard


def createbattleships(Player, shipboard, stdscr, is_computer=False):
    i = 1
    ship_row = 0
    ship_col = 0
    orientation = "horizontal"  # Start with horizontal orientation

    while i <= battleships:
        stdscr.clear()  # Clear the screen
        if is_computer:
            # Computer's turn
            ship_row = random.randint(0, len(shipboard) - 1)
            ship_col = random.randint(0, len(shipboard[0]) - 1)
            orientation = random.choice(["horizontal", "vertical"])

            # Check if the position is valid
            if orientation == "horizontal" and ship_col <= len(shipboard[0]) - 4:
                if all(shipboard[ship_row][ship_col + j] == "-" for j in range(5)):
                    shipboard[ship_row][ship_col] = "<"
                    for j in range(1, 4):
                        shipboard[ship_row][ship_col + j] = "X"
                    shipboard[ship_row][ship_col + 4] = ">"
                    i += 1
            elif orientation == "vertical" and ship_row <= len(shipboard) - 4:
                if all(shipboard[ship_row + j][ship_col] == "-" for j in range(5)):
                    shipboard[ship_row][ship_col] = "∧"
                    for j in range(1, 4):
                        shipboard[ship_row + j][ship_col] = "X"
                    shipboard[ship_row + 4][ship_col] = "V"
                    i += 1
        else:
            stdscr.addstr(
                0,
                0,
                f"{Player}: Place your battleship(s).(Use R key to rotate the ship)",
            )
            PrintGrid(
                shipboard, stdscr, offset_y=2
            )  # Adjusted to pass offset_y to position the grid

            # Highlight the current ship position based on orientation
            if orientation == "horizontal":
                stdscr.addstr(3 + ship_row, 1 + ship_col * 4, "<", curses.color_pair(1))
                for j in range(1, 4):
                    stdscr.addstr(
                        3 + ship_row, 1 + (ship_col + j) * 4, "X", curses.color_pair(1)
                    )
                stdscr.addstr(
                    3 + ship_row, 1 + (ship_col + 4) * 4, ">", curses.color_pair(1)
                )
            else:  # Vertical orientation
                stdscr.addstr(3 + ship_row, 1 + ship_col * 4, "∧", curses.color_pair(1))
                for j in range(1, 4):
                    stdscr.addstr(
                        3 + (ship_row + j), 1 + ship_col * 4, "X", curses.color_pair(1)
                    )
                stdscr.addstr(
                    3 + (ship_row + 4), 1 + ship_col * 4, "V", curses.color_pair(1)
                )

            # Get user input
            key = stdscr.getch()

            # Rotate the battleship
            if key == ord("r") or key == ord("R"):
                orientation = (
                    "vertical" if orientation == "horizontal" else "horizontal"
                )
                stdscr.refresh()
                continue

            # Move the ship based on the arrow key pressed
            if key == curses.KEY_UP and ship_row > 0:
                ship_row -= 1
            elif (
                key == curses.KEY_DOWN and ship_row < len(shipboard) - 1
            ):  # Adjust for ship length
                ship_row += 1
            elif key == curses.KEY_LEFT and ship_col > 0:
                ship_col -= 1
            elif (
                key == curses.KEY_RIGHT and ship_col < len(shipboard[0]) - 1
            ):  # Adjust for ship length
                ship_col += 1
            elif key == ord("\n"):  # Enter key to place the ship
                # Check if the battleship can be placed in the current orientation
                if orientation == "horizontal" and ship_col <= len(shipboard[0]) - 4:
                    if all(shipboard[ship_row][ship_col + j] == "-" for j in range(5)):
                        shipboard[ship_row][ship_col] = "<"
                        for j in range(1, 4):
                            shipboard[ship_row][ship_col + j] = "X"
                        shipboard[ship_row][ship_col + 4] = ">"
                        for j in range(5):
                            location.append(alphabets[ship_row] + str(ship_col + j + 1))
                        i += 1
                    else:
                        stdscr.addstr(
                            3 + len(shipboard),
                            0,
                            "Invalid option or already taken. Please try again.",
                        )
                        stdscr.refresh()
                        stdscr.getch()  # Wait for user to acknowledge the error
                elif orientation == "vertical" and ship_row <= len(shipboard) - 4:
                    if all(shipboard[ship_row + j][ship_col] == "-" for j in range(5)):
                        shipboard[ship_row][ship_col] = "∧"
                        for j in range(1, 4):
                            shipboard[ship_row + j][ship_col] = "X"
                        shipboard[ship_row + 4][ship_col] = "V"
                        for j in range(5):
                            location.append(alphabets[ship_row + j] + str(ship_col + 1))
                        i += 1
                    else:
                        stdscr.addstr(
                            3 + len(shipboard),
                            0,
                            "Invalid option or already taken. Please try again.",
                        )
                        stdscr.refresh()
                        stdscr.getch()  # Wait for user to acknowledge the error
                else:
                    stdscr.addstr(
                        3 + len(shipboard),
                        0,
                        "Invalid option or already taken. Please try again.",
                    )
                    stdscr.refresh()
                    stdscr.getch()  # Wait for user to acknowledge the error
    return shipboard


def createshipboard(Player, stdscr, is_computer):
    stdscr.clear()
    shipboard = createboard()

    createcruisers(Player, shipboard, stdscr, is_computer)
    createdestroyers(Player, shipboard, stdscr, is_computer)
    createbattleships(Player, shipboard, stdscr, is_computer)
    stdscr.refresh()
    stdscr.addstr(1, 0, Player)
    board_str = "\n".join([" ".join(row) for row in shipboard])

    # Print the string representation of the shipboard
    stdscr.addstr(1, 0, board_str)
    stdscr.refresh()
    stdscr.addstr("Press Enter to continue")

    return shipboard


def PlayerAttack(player, playershipboard, playerattackboard, opponentshipboard, stdscr):
    if curses.LINES < 25 or curses.COLS < 80:
        stdscr.addstr(0, 0, "Screen too small. Please resize.")
        stdscr.refresh()
        return
    Attacking = True
    validoptions = createvalidoptions()
    while Attacking:
        if OpponentAlive(opponentshipboard,player) == "ongoing":
            stdscr.clear()  # Clear the screen
            stdscr.addstr(0, 0, player)
            stdscr.addstr(1, 0, "Ships")
            PrintGrid(playershipboard, stdscr, offset_y=2)
            stdscr.addstr(13, 0, "Attack")
            PrintGrid(playerattackboard, stdscr, offset_y=14)
            stdscr.refresh()

            # Get user input for the target location
            stdscr.addstr(24, 0, "Enter a location to attack: ")
            stdscr.refresh()
            Target = stdscr.getstr().decode().strip().upper()  # Convert input to uppercase

            if Target not in validoptions:
                stdscr.addstr(25, 0, "Invalid Target")
                stdscr.refresh()
                stdscr.getch()  # Wait for user to press a key
            else:
                TargetStatus = opponentshipboard[alphabets.index(Target[0])][
                    int(Target[-1]) - 1
                ]
                PlayerAttackStatus = playerattackboard[alphabets.index(Target[0])][
                    int(Target[-1]) - 1
                ]
                if TargetStatus == "0" or PlayerAttackStatus == "M":
                    stdscr.addstr(25, 0, "Invalid Target")
                    stdscr.refresh()
                    stdscr.getch()  # Wait for user to press a key
                elif TargetStatus in ["<", ">", "∧", "V"]:
                    stdscr.addstr(25, 0, "You have hit your target.")
                    stdscr.refresh()
                    stdscr.getch()  # Wait for user to press a key
                    opponentshipboard[alphabets.index(Target[0])][int(Target[-1]) - 1] = "0"
                    playerattackboard[alphabets.index(Target[0])][int(Target[-1]) - 1] = "H"

                elif TargetStatus == "X":
                    stdscr.addstr(25, 0, "You have hit your target.")
                    stdscr.refresh()
                    stdscr.getch()  # Wait for user to press a key
                    opponentshipboard[alphabets.index(Target[0])][int(Target[-1]) - 1] = "0"
                    playerattackboard[alphabets.index(Target[0])][int(Target[-1]) - 1] = "H"

                else:
                    stdscr.addstr(25, 0, "You missed...")
                    stdscr.refresh()
                    stdscr.getch()  # Wait for user to press a key
                    playerattackboard[alphabets.index(Target[0])][int(Target[-1]) - 1] = "M"
                    Attacking = False
        else:
            return OpponentAlive(opponentshipboard, player)
    return OpponentAlive(opponentshipboard, player)


def ComputerAttack(
    player, playershipboard, playerattackboard, opponentshipboard, stdscr
):
    Attacking = True
    validoptions = createvalidoptions()
    while Attacking:
        stdscr.clear()  # Clear the screen
        stdscr.addstr(0, 0, player)
        stdscr.addstr(1, 0, "Ships")
        PrintGrid(playershipboard, stdscr, offset_y=2)
        stdscr.addstr(12, 0, "Attack")
        PrintGrid(playerattackboard, stdscr, offset_y=13)
        stdscr.refresh()
        Target = random.choice(validoptions)
        if playerattackboard[alphabets.index(Target[0])][int(Target[-1]) - 1] not in [
            "H",
            "M",
        ]:  # Ensure the target hasn't been hit before
            TargetStatus = opponentshipboard[alphabets.index(Target[0])][
                int(Target[-1]) - 1
            ]
            if TargetStatus == "X":
                stdscr.addstr(25, 0, f"Computer has hit your ship at {Target}")
                stdscr.refresh()
                stdscr.getch()  # Wait for user to press a key
                opponentshipboard[alphabets.index(Target[0])][int(Target[-1]) - 1] = "0"
                playerattackboard[alphabets.index(Target[0])][int(Target[-1]) - 1] = "H"
                if OpponentAlive(opponentshipboard, player) != "ongoing":
                    break
                stdscr.clear()  # Clear the screen
            elif TargetStatus in ["<", ">", "∧", "V"]:
                stdscr.addstr(25, 0, f"Computer has hit your ship at {Target}")
                stdscr.refresh()
                stdscr.getch()  # Wait for user to press a key
                opponentshipboard[alphabets.index(Target[0])][int(Target[-1]) - 1] = "0"
                playerattackboard[alphabets.index(Target[0])][int(Target[-1]) - 1] = "H"
            else:
                stdscr.addstr(25, 0, f"Computer missed at {Target}")
                stdscr.refresh()
                stdscr.getch()  # Wait for user to press a key
                playerattackboard[alphabets.index(Target[0])][int(Target[-1]) - 1] = "M"
                Attacking = False
    return OpponentAlive(opponentshipboard, player)


def OpponentAlive(opponentshipboard, player):
    for row in opponentshipboard:
        if "X" in row or "V" in row or "<" in row or ">" in row or "∧" in row:
            return "ongoing"
    return player


def gamestart(
    player1shipboard,
    player1attackboard,
    player2shipboard,
    player2attackboard,
    stdscr,
    mode,
):
    status = "ongoing"
    while status == "ongoing":
        status = PlayerAttack(
            "Player 1", player1shipboard, player1attackboard, player2shipboard, stdscr
        )
        if status == "Player 1":
            print("Player 1 won.")
            break
        if mode == "multiplayer":
            status = PlayerAttack(
                "Player 2",
                player2shipboard,
                player2attackboard,
                player1shipboard,
                stdscr,
            )
            if status == "Player 2":
                print("Player 2 won.")
        else:  # single-player mode
            status = ComputerAttack(
                "Computer",
                player2shipboard,
                player2attackboard,
                player1shipboard,
                stdscr,
            )
            if status == "Computer":
                print("Computer won.")


if __name__ == "__main__":
    curses.wrapper(main)
