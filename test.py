import argparse
import curses
import random
import secrets
import sys

parser = argparse.ArgumentParser(description='Battleship Game')  # the argument parser
parser.add_argument('xaxis', type=int, help='number of columns in game board ( 5 < xaxis <=10)') # xaxis argument
parser.add_argument('yaxis', type=int, help='number of rows in game board( 5 < yaxis <=10)') # yaxis argument
args = parser.parse_args() 

# assign rows and columns of board with command line args
ROWS = args.yaxis
COLS = args.xaxis

# Restrict the ROWS and COLS in the range (5, 10), both inclusive.
if ROWS < 5:
    ROWS = 5
if ROWS > 10:
    ROWS = 10

if COLS < 5:
    COLS = 5
if COLS > 10:
    COLS = 10

# menu options
menu = ["vs CPU", "vs Friend", "Exit"] 

# orientation options
horizontal = ["horizontal", "h"]
vertical = ["vertical", "v"]

# all the ship types. More ship types can be added in this list
SHIP_TYPES = [("Carrier", 5, "Cr"), ("Battleship", 4, "B"), ("Submarine", 3, "S"), ("Cruiser", 3, "Cs"), ("Destroyer", 2, "D")]

# Cell Codes for graphical representation 
CODE_EMPTY = '   '
CODE_HIT =   ' * ' 
CODE_MISS =  ' . '  
CODE_SUNK =  ' # ' 


ROW_HEIGHT = 2
COL_WIDTH = len(CODE_EMPTY) + 1  # +1 to account for the width of cell border

# blank line used throughout the script to override any prewritten text. 
blank = "                                                 " 


def main(stdscr):

    #curses.curs_set(0) #hide the cursor

    # all the color schemes used in my game
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) 
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_CYAN)
    
    stdscr.border(0)  # border of the standard screen
    curses.mousemask(1) # to enable listening for mouse events 
    
    main_menu(stdscr, 0)  

def main_menu(win, selected_row_idx):
    win.keypad(1)  # for simplified listening of keyboard events
    h, w = win.getmaxyx() #max height and width of the curses window

    while True:
        win.clear()
        for idx, row in enumerate(menu): 
            x = w//2 - len(row)//2 # to centre the row horizontally
            y = h//2 - len(menu) + idx # to centre the row vertically

            if idx == selected_row_idx:
                win.attron(curses.color_pair(1)) # highlight the selected option
                win.addstr(y, x, row)    
                win.attroff(curses.color_pair(1))
            else:
                win.addstr(y, x, row)
        win.refresh()
        
        key = win.getch()
        win.clear()
        
        # keyboard cycling through options
        if key == curses.KEY_UP:
            selected_row_idx -= 1
            
        elif key == curses.KEY_DOWN:
            selected_row_idx += 1

        elif key == curses.KEY_ENTER or key in [10, 13]:
            start_game(win, selected_row_idx)
            
        # underflow and overflow handling
        if selected_row_idx < 0:
            selected_row_idx = len(menu) - 1
        elif selected_row_idx >= len(menu):
            selected_row_idx = 0


def start_game(win, option):
    if option == 0:
        init_ai_game(win)
    elif option == 1:
        init_friend_game(win)
    elif option == 2:
        sys.exit(0)


def init_ai_game(win):
    win.clear()
    win.refresh()
    player1 = Player("Player 1")
    player2 = Player("CPU")
    player2.is_bot = True 

    player1.place_ships(win) 
    win.clear()
    h, w = win.getmaxyx()
    msg = player1.name + " ! Your ships have been placed. Press any key to continue."
    win.addstr(h//2, w//2  - len(msg)//2, msg)
    win.refresh() 
    
    win.getch()
    for type in SHIP_TYPES:
        player2.place_ship_random(type)
    h, w = win.getmaxyx()
    win.clear()
    msg = player2.name + " has placed their ships. Press any key to continue."
    win.addstr(h//2, w//2  - len(msg)//2, msg)
    
    win.refresh()
    
    win.getch()

    gameloop(player1, player2, win)


def init_friend_game(win):
    win.clear()
    win.refresh()
    # Initialize players. Here, player names can be taken as user input but I have hard coded the names.
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    # Place ships for Player 1
    player1.place_ships(win)
    win.clear()
    h, w = win.getmaxyx()
    msg = player1.name + " ! Your ships have been placed. Press any key to continue."
    win.addstr(h//2, w//2  - len(msg)//2, msg)
    win.refresh()
    
    win.getch()  # wait for user input
    
    # Place ships for player 2
    player2.place_ships(win)
    win.clear()
    h, w = win.getmaxyx()
    msg = player2.name + " ! Your ships have been placed. Press any key to continue."
    win.addstr(h//2, w//2  - len(msg)//2, msg)
    win.refresh()
    win.getch()

    gameloop(player1, player2, win) # start the game loop


def tie(p1, p2, win):
    win.clear()
    h, w = win.getmaxyx()
    win.addstr(h//2, w//2 - 1, "Tie")
    offx = COL_WIDTH
    offy = ROW_HEIGHT*3
    win.refresh()
    # Display both the boards as unhidden.
    p1.draw_board(offx, offy, Coordinate(-1, -1), False, win)
    p2.draw_board(offx + COLS * (COL_WIDTH) + 2*offx, offy, Coordinate(-1, -1), False, win)
    
    win.refresh()
    win.getch()
    main_menu(win, 0)


def game_over(winner, loser, win):
    win.clear()
    h, w = win.getmaxyx()
    curses.flash()  # Flash the screen
    
    win.addstr(h//2, w//2 - 4, "Game Over")
    win.addstr(h//2 + 1, w//2 - 4, winner.name + " wins! ")
    offx = COL_WIDTH
    offy = ROW_HEIGHT*3
    win.refresh()

    # Show both the boards as unhidden 
    winner.draw_board(offx, offy, Coordinate(-1, -1), False, win)
    loser.draw_board(offx + COLS * COL_WIDTH + 2*offx, offy, Coordinate(-1, -1), False, win)
    win.getch()
    main_menu(win, 0)

def gameloop(p1, p2, win):

    # offsets serve as the origin 
    offx = COL_WIDTH
    offy = 3*ROW_HEIGHT
    
    
    win.refresh()

    # p1 plays the first move
    current_player = p1 
    enemy = p2
    
    selected_cell = Coordinate(0, 0)
    
    # number of turns yet
    turns = 0    

    #user input
    userrow = 0
    usercol = 0    
            
    while True:
        win.clear()
        
        while True:
            # if number of turns is even, it means both players have made their move
            # checking for winner before player 2 has made move would give the first player an unfair advantage
            if turns % 2 == 0:
                # check for game over
                if current_player.is_lost() and enemy.is_lost():
                    tie(current_player, enemy, win)
                elif current_player.is_lost():
                    game_over(winner=enemy, loser=current_player, win=win)
                elif enemy.is_lost():
                    game_over(winner=current_player, loser=enemy, win=win)

            # CPU player/Bot does not need a UI to make move.
            if current_player.is_bot:
                #Try random moves
                while True:
                    selected_cell = current_player.ai_move(enemy)
                    success, msg = enemy.handle_hit(selected_cell)
                    # if move was made successfully 
                    if success:
                        current_player, enemy = enemy, current_player
                        turns += 1
                        selected_cell = Coordinate(-1, -1)
                        win.clear()
                        msg = "CPU has made its move. Press any key to continue."
                        win.addstr(0, 0, msg)
                        win.refresh()
                        win.getch()
                        win.clear()
                        break  # no need of trying any further
                continue

            # Message to the player
            win.addstr(0, 0, " "*COL_WIDTH*5 + current_player.name + "! Your Turn" + blank)
            win.addstr(1, 0, "Click on a location on Enemy Board to fire" + blank)
            win.addstr(2, 0, " Or Select a location on Enemy Board with Cursor Keys and Press Space to Fire")
            win.addstr(3, 0, "Alternatively, you can Enter the Column Letter and Row Number to Fire.")
            # Display Enemy Board and Score
            display_boards_and_scores(current_player, enemy, offx, offy, selected_cell, win)

            # handling user input
            key = win.getch()

            if ord('A') <= key <= ord('Z') or ord('a') <= key <= ord('z'):
                usercol = key - ord('A') + 1 if key <=ord('Z') else key - ord('a') + 1 #a/A means usercol = 1
                userrow = 0
                
            elif chr(key).isdigit():  # as ROWS<=10, so y is always a single digit( or character)
                userrow = userrow * 10 + key - ord('0') #use the entered digits to make a number
                

            elif key not in [10, 13]: #if row/col input is interrupted, reassign both as zero
                userrow = 0
                usercol = 0

            # keyboard input 
            if key == curses.KEY_DOWN:
                selected_cell.y += 1
            elif key == curses.KEY_UP:
                selected_cell.y -= 1
            elif key == curses.KEY_LEFT:
                selected_cell.x -= 1
            elif key == curses.KEY_RIGHT:
                selected_cell.x += 1
            
            # underflow and overflow handling 
            if selected_cell.x < 0:
                selected_cell.x = COLS - 1
            if selected_cell.x >= COLS:
                selected_cell.x = 0
            if selected_cell.y < 0:
                selected_cell.y = ROWS - 1
            if selected_cell.y >=ROWS:
                selected_cell.y = 0    

            # mouse input
            if key == curses.KEY_MOUSE:
                
                click = curses.getmouse()
                mousex = click[1]
                mousey = click[2]
                row = (mousey - offy) // ROW_HEIGHT
                col = (mousex - 1 - offx)//COL_WIDTH
                selected_cell = Coordinate(col, row)
                if COLS <= selected_cell.x or selected_cell.x < 0  or selected_cell.y < 0 or selected_cell.y >= ROWS :
                    continue
                            
            # Space pressed or Mouse clicked/pressed means Fire
            if key == ord(' ') or key == curses.KEY_MOUSE or (key in [10, 13] and usercol > 0 and userrow > 0):
                if userrow > 0 and usercol > 0:
                    selected_cell = Coordinate(usercol - 1, userrow - 1)
                    userrow = 0 
                    usercol = 0
                # Try to fire at the selected cell
                success, msg = enemy.handle_hit(selected_cell)
                if success:
                    display_boards_and_scores(current_player, enemy, offx, offy, selected_cell, win)
                    current_player, enemy = enemy, current_player
                    turns += 1
                    selected_cell = Coordinate(0, 0)
                    msg += ". Press any key to Pass Turn." + blank 
                    win.attron(curses.color_pair(2))
                    win.addstr(0, 0, msg)
                    win.addstr(1, 0, blank + blank)
                    win.addstr(2, 0, blank + blank)
                    win.addstr(3, 0, blank + blank)
                    win.refresh()
                    win.attroff(curses.color_pair(2))
                    
                    win.getch() 
                    
                    win.clear()
                    h, w = win.getmaxyx()
                    # only regular players who are not bots need the UI
                    if not current_player.is_bot:
                        # This prevents players from accidently seeing each other's board 
                        msg = current_player.name + " ! Your turn. Press any key to continue"
                        win.addstr(h//2, w//2 - len(msg)//2, msg)
                        win.refresh()
                        win.getch()
                        win.clear()
                        win.refresh()
                else:
                    # unsuccessful move, so just display the message and don't count the turn
                    win.addstr(1, 0, blank + blank)
                    win.addstr(2, 0, blank + blank)
                    win.addstr(3, 0, blank + blank)
                    win.attron(curses.color_pair(4))
                    win.addstr(0, 0, msg + blank + blank)
                    win.attroff(curses.color_pair(4))
                    win.refresh()
                    win.getch()


def display_boards_and_scores(current_player, enemy, offx, offy, selected_cell, win):       
    # Display enemy's board
    title = "Enemy Board"
    enemy.draw_board(offx, offy, selected_cell, True, win)
    win.addstr(offy + ROW_HEIGHT*(ROWS) + 1, offx + COL_WIDTH * COLS//2 - len(title), title)
    sunk = 0 #number of own ships sunk
    sunk = enemy.ships_sunk_count()
    score_text = 'Ships Sunk : ' + str(sunk)        
    win.addstr(offy + ROW_HEIGHT*(ROWS + 1), offx + COL_WIDTH * COLS//2 - len(title), score_text)
    score_text = 'Ships remaining: ' + str(len(enemy.ships) - sunk) # remaining = total - sunk       
    win.addstr(offy + ROW_HEIGHT*(ROWS + 1) + 1, offx + COL_WIDTH * COLS//2 - len(title), score_text )
    
    # Display Current player's board and score
    title = "My Board"
    offx2 = offx + COLS * (COL_WIDTH) + 2*offx
    win.addstr(offy + ROW_HEIGHT*(ROWS) + 1, offx2 + COL_WIDTH * COLS//2 - len(title), title)
    current_player.draw_board(offx2, offy, Coordinate(-1, -1), False, win)
    sunk = current_player.ships_sunk_count()
    score_text = 'Ships Sunk : ' + str(sunk)        
    win.addstr(offy + ROW_HEIGHT*(ROWS + 1), offx2 + COL_WIDTH * COLS//2 - len(title), score_text)
    score_text = 'Ships remaining: ' + str(len(current_player.ships) - sunk)        
    win.addstr(offy + ROW_HEIGHT*(ROWS + 1) + 1, offx2 + COL_WIDTH * COLS//2 - len(title), score_text)
    
    win.refresh() # refresh the window
    
class Ship:
    def __init__(self, type):
        self.name = type[0]
        self.length = type[1]
        self.code = type[2]
        self.orientation = None
        self.coords = []
        self.hits = 0
        
    def place(self, startx, starty, orientation):
        self.coords = []
        self.hits = 0
        # add all the coordinates of this ship according to the start location and orientation
        if orientation in horizontal:
            for x in range(self.length):
                self.coords.append(Coordinate(startx + x, starty))
        elif orientation in vertical:
            for y in range(self.length):
                self.coords.append(Coordinate(startx, starty + y))

    def is_sunk(self):
        return self.hits == self.length


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def left(self):
        return Coordinate(self.x - 1, self.y)

    def right(self):
        return Coordinate(self.x + 1, self.y)
    
    def up(self):
        return Coordinate(self.x, self.y - 1)
    
    def down(self):
        return Coordinate(self.x, self.y + 1)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Player:
    
    def __init__(self, name):
        self.name = name 
        self.board = []
        self.ships = []
        self.enemy = None
        self.is_bot = False

        # initialize empty board of ROWS by COLS
        for r in range(ROWS):
            self.board.append([CODE_EMPTY]*COLS)
    
    def place_ship(self, ship, coords, orientation):
        if orientation in vertical:
            if coords.y + ship.length > ROWS: # if the ship cannot fit in this location and orientation
                return False # means failure
            
        elif orientation in horizontal:
            if coords.x + ship.length > COLS: # if the ship cannot fit in this location and orientation
                return False # means failure

        #if we have come this far, then it means no failure 
        ship.place(coords.x, coords.y , orientation) # place the ship

        # if any coordinate of the ship is out of bounds, then it means failure
        for c in ship.coords:
            if self.board[c.y][c.x] != CODE_EMPTY:
                return False
        
        #no invalid coordinates in ship, then update the board
        for c in ship.coords:
            self.board[c.y][c.x] = ship.code
        self.ships.append(ship) # add the ship to the player's list of ships
        return True # means SUCCESS

    def handle_hit(self, coord):
        code = self.board[coord.y][coord.x]
        msg = ""
        if code == CODE_HIT or code == CODE_SUNK or code == CODE_MISS: # failure
            return False, "You already fired there !"

        if code == CODE_EMPTY:
            self.board[coord.y][coord.x] = CODE_MISS  # failure
            return True, "It was a Miss"

        else:
            # hit the ship if any of its coords lie in this coord
            for ship in self.ships:
                msg += ship.name + " : "
                for c in ship.coords:
                    msg += str(c) + " "
                    if c == coord: 
                        ship.hits = ship.hits + 1  # number of hits the ship has taken increased by 1
                        if ship.is_sunk():  # if the ship has sunk, mark all its cells as sunk
                            for c2 in ship.coords:
                                self.board[c2.y][c2.x] = CODE_SUNK
                            return True, "You sunk my " + ship.name + ""  # success
                        
                        else:
                            # if the ship is not sunk, mark it only as a hit.
                            self.board[c.y][c.x] = CODE_HIT
                            return True, "It was a Hit"  # success
                    msg += "\n"
        return False, "End of Method reached : " + code + "\n" + msg
        # if we have reached so far, it means there is some problem
        # this helped me in pointing out and error with the way ship codes are stored on board
    
    def is_lost(self):
        # if even one of the player's ships is sailing, the player has not lost
        for ship in self.ships:
            if not ship.is_sunk():
                return False
        return True

    def ships_sunk_count(self):
        sunk = 0 
        for ship in self.ships:
            if ship.is_sunk():
                sunk += 1
        return sunk

    def place_ship_random(self, type):
        ship = Ship(type)
        
        while True:
            orientation = 'h' if random.random() < 0.5 else 'v'  # random 50-50 chance orientation

            #random coordinates
            x = secrets.randbelow(COLS)
            y = secrets.randbelow(ROWS)

            # make sure none of the cells of the ship will be placed out of bounds
            if orientation == 'h':
                if x + ship.length > COLS:
                    x -= (x + ship.length - COLS)
            elif orientation == 'v':
                if y + ship.length > ROWS:
                    y -= (y + ship.length - ROWS)

            if self.place_ship(ship, Coordinate(x, y), orientation):
                return

    def place_ships(self, win):
        win.clear()
        win.refresh()
        h, w = win.getmaxyx()
        win.addstr(0, 0, self.name + " ! Press Enter to  continue with this placement.")
        win.addstr(1, 0, self.name + " ! Or Press  " + "Spacebar"+ " to start placing ships manually .")
        for type in SHIP_TYPES:
            self.place_ship_random(type)
        win.refresh()
            
        offx = COL_WIDTH
        offy = 3 * ROW_HEIGHT
        selected_cell = Coordinate(-1, -1)
        self.draw_board(offx, offy, selected_cell, False, win)
        title = self.name + "'s Board"
        win.addstr(offy + ROW_HEIGHT*(ROWS + 1), offx + COL_WIDTH * COLS//2 - len(title) // 2, title)
        win.refresh()
        
        while True:
            key = win.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                return
            
            elif key == ord(' '):
                self.board = []
                for r in range(ROWS):
                    self.board.append([CODE_EMPTY]*COLS)
                self.ships = []
                break

        selected_cell = Coordinate(0, 0)
        for type in SHIP_TYPES:
            while True:
                win.addstr(0, 0, self.name + " Place your ships." + blank)
                win.addstr(1, 0, "Ship : " + type[0] + blank )
                
                mouse_controls_msg = ["Use Curser Keys or Mouse to select a cell"]
                keyboard_controls_msg = ["Press " + "H" + " for horizontal placement", "Press " + "V" + " for vertical placement" ]
                
                controls_msg = [mouse_controls_msg, keyboard_controls_msg]

                cx = offx + ROWS * COL_WIDTH + offx
                cy = offy + COLS//2
                
                win.addstr(cy - ROW_HEIGHT, cx + len(mouse_controls_msg[0])//2 - len("CONTROLS")//2, "CONTROLS")
                for cm in controls_msg:
                    for m in cm:
                        win.addstr(cy, cx, m)
                        cy += 1
                    cy += 1
                win.refresh()
                        
                
                win.refresh()
                self.draw_board(offx, offy, selected_cell, False, win)
                orientation = 'none'

                key = win.getch()

                if key == curses.KEY_DOWN:
                    selected_cell.y += 1
                elif key == curses.KEY_UP:
                    selected_cell.y -= 1
                elif key == curses.KEY_LEFT:
                    selected_cell.x -= 1
                elif key == curses.KEY_RIGHT:
                    selected_cell.x += 1


                elif key == curses.KEY_MOUSE:

                    _, mousex, mousey, _, bstate = curses.getmouse()
                    
                    row = (mousey - offy) // ROW_HEIGHT
                    col = (mousex - 1 - offx)//COL_WIDTH
                    selected_cell = Coordinate(col, row)

                    if COLS <= selected_cell.x  or selected_cell.x < 0  or selected_cell.y < 0 or selected_cell.y >= ROWS :
                        continue
                
                if selected_cell.x < 0:
                    selected_cell.x = COLS - 1
                if selected_cell.x >= COLS:
                    selected_cell.x = 0
                if selected_cell.y < 0:
                    selected_cell.y = ROWS - 1
                if selected_cell.y >=ROWS:
                    selected_cell.y = 0    

                if key == ord('h'):
                    orientation = 'h'
                    
                elif  key == ord('v'):
                    orientation = 'v'

                if orientation != 'none':
                    ship = Ship(type)
                    success = self.place_ship(ship, selected_cell, orientation)
                    if success:
                        win.clear()
                        win.attron(curses.color_pair(2))
                        win.addstr(h - ROW_HEIGHT*2, 0, type[0] + " added successfully ")   
                        win.attron(curses.color_pair(2))
                        self.draw_board(offx, offy, selected_cell, False, win)
                        
                        break
                    else:
                        win.clear()
                        win.attron(curses.color_pair(4))
                        win.addstr(h- ROW_HEIGHT*2, 0, "Cannot place it there.")
                        win.attroff(curses.color_pair(4))
                        
                win.refresh()
                #self.draw_board(offx, offy, selected_cell, False, win)
 
    def draw_board(self, offx, offy, selected_cell, hidden, win):

        for y in range(ROWS):
            for x in range(COLS):
                
                if x == 0:
                    win.addstr(offy + y*ROW_HEIGHT, offx - COL_WIDTH//2, str(y+1))

                if y == 0:
                    win.addstr(offy - ROW_HEIGHT, offx + COL_WIDTH * x  + COL_WIDTH//2, chr(65 + x))

                code = self.board[y][x]
                
                selected = Coordinate(x, y) == selected_cell

                if code == CODE_EMPTY or code == CODE_HIT or code == CODE_MISS or code == CODE_SUNK:
                    draw_cell(Coordinate(x, y ), offx, offy, code, selected, win)
                else:
                    if hidden:
                        draw_cell(Coordinate(x, y), offx, offy, CODE_EMPTY, selected, win)
                    else:
                        draw_cell(Coordinate(x, y), offx, offy, " " + code + " ", selected, win)

            #win.addch((y *ROW_HEIGHT + offy, COLS * COL_WIDTH + offx, curses.ACS_VLINE)    
    
    def ai_move(self, enemy):
        for y in range(ROWS):
            for x in range(COLS):
                if enemy.board[y][x] == CODE_HIT:
                    cell = Coordinate(x, y)
                    neighbors = [cell.left(), cell.right(), cell.up(), cell.down()]
                    random_cell = random.choice(neighbors)
                    if random_cell.x < 0 or random_cell.x >=COLS or random_cell.y < 0 or random_cell.y >=ROWS:
                        continue
                    return random_cell
        randomy = secrets.randbelow(ROWS)
        randomx = secrets.randbelow(COLS)

        return Coordinate(randomx, randomy)

    
def draw_cell(coord, offx, offy, code, selected,win):
    
    if selected:
        win.attron(curses.color_pair(7))
        win.addstr(coord.y*ROW_HEIGHT + offy, coord.x*COL_WIDTH + 1 + offx, str(code))
        win.attroff(curses.color_pair(7))
    else: 
        if code == CODE_HIT or code == CODE_SUNK:
            win.attron(curses.color_pair(6))
            win.addstr(coord.y*ROW_HEIGHT + offy, coord.x*COL_WIDTH + 1 + offx, str(code))
            win.attroff(curses.color_pair(6))

        elif code == CODE_MISS:
            win.attron(curses.color_pair(1))
            win.addstr(coord.y*ROW_HEIGHT + offy, coord.x*COL_WIDTH + 1 + offx, str(code))
            win.attroff(curses.color_pair(1))

        elif code == CODE_EMPTY:
            win.addstr(coord.y*ROW_HEIGHT + offy, coord.x*COL_WIDTH + 1 + offx, str(code))
            
        else:
            win.attron(curses.color_pair(5))
            win.addstr(coord.y*ROW_HEIGHT + offy, coord.x*COL_WIDTH + 1 + offx, str(code))
            win.attroff(curses.color_pair(5))
    
    win.attron(curses.color_pair(3))
    win.addch(coord.y*ROW_HEIGHT + offy, coord.x*COL_WIDTH + offx, curses.ACS_VLINE)
    win.addch(coord.y*ROW_HEIGHT + offy, coord.x*COL_WIDTH + COL_WIDTH + offx, curses.ACS_VLINE)
    for i in range(COL_WIDTH + 1):
        if i == 0:
            win.addch(coord.y*ROW_HEIGHT + offy - ROW_HEIGHT//2, coord.x*COL_WIDTH + offx + i, "+") 
        elif i == COL_WIDTH :
            win.addch(coord.y*ROW_HEIGHT + offy - ROW_HEIGHT//2, coord.x*COL_WIDTH + offx + i, "+") 
        else:   
            win.addch(coord.y*ROW_HEIGHT + offy - ROW_HEIGHT//2, coord.x*COL_WIDTH + offx + i, "-")
    for i in range(COL_WIDTH + 1):
        if i == 0:
            win.addch(coord.y*ROW_HEIGHT + offy + ROW_HEIGHT//2, coord.x*COL_WIDTH + offx + i, "+") 
        elif i == COL_WIDTH :
            win.addch(coord.y*ROW_HEIGHT + offy + ROW_HEIGHT//2, coord.x*COL_WIDTH + offx + i, "+") 
        else:   
            win.addch(coord.y*ROW_HEIGHT + offy + ROW_HEIGHT//2, coord.x*COL_WIDTH + offx + i, "-")
    win.attroff(curses.color_pair(3))

    win.refresh()


curses.wrapper(main)