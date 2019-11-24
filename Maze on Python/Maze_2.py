# Start of the code ###
import copy
import random
import sys
import os
from os import system, name  # used to clear the terminal
import keyboard  # used to detect key press

# import sleep to show output for some time period
from time import sleep

# Definition of the Escape codes to change the character colour
GREEN_T = '\033[32m'
WHITE_T = '\033[37m'
RED_T = '\033[91m'
YELLOW_T = '\033[93m'
LIGHT_PURPLE_T = '\033[94m'
PURPLE_T = '\033[95m'
CYAN_T = '\033[96m'
LIGHT_GRAY_T = '\033[97m'
BLACK_T = '\033[98m'
DEFAULT_T = '\033[m'  # reset Text to the defaults

# Definition of the different characters inside the game board
EMPTY_CHAR = ' '
BRICK_CHAR = '▓'
STARTING_CHAR = '0'
TARGET_CHAR = 'T'
PATH_CHAR = 'X'
# PATH_CHAR = '█'

board_square = {
    'line': 1,
    'column': 1,
    'colour': WHITE_T,
    'char': EMPTY_CHAR,
    'visited': False,
    'previous_line': -1,
    'previous_column': -1
}


# Function to print the array in Black and White format
def print_array_BW(array_input):
    x = 0
    print(' ', DEFAULT_T, end='')
    while x < len(array_input[0]):
        print(str(x % 10), DEFAULT_T, end='')
        x += 1
    print('')
    x = 0
    for line in array_input:
        print(str(x % 10), DEFAULT_T, end='')
        x += 1
        print(WHITE_T + ' '.join(line), DEFAULT_T)
    return


# Function to print the array in colour format
def print_array_Colour(array_input):
    x = 0
    print(' ', YELLOW_T, end='')
    while x < len(array_input[0]):
        print(YELLOW_T, str(x % 10), end='')
        x += 1
    print('')
    x = 0
    for line in array_input:
        print(YELLOW_T, str(x % 10), DEFAULT_T, end='')
        x += 1
        for column in line:
            if column == EMPTY_CHAR:
                print(column, DEFAULT_T, end='')
            else:
                if column == BRICK_CHAR:
                    print(YELLOW_T + column, DEFAULT_T, end='')
                else:
                    if column == STARTING_CHAR:
                        print(CYAN_T + column, DEFAULT_T, end='')
                    else:
                        if column == TARGET_CHAR:
                            print(RED_T + column, DEFAULT_T, end='')
                        else:
                            if column == PATH_CHAR:
                                print(CYAN_T + column, DEFAULT_T, end='')
                            else:
                                print(YELLOW_T + column, DEFAULT_T, end='')
        print("\n", end='')
    return


# Request input for the number of lines for the board
def number_lines_input():
    while True:
        number_of_lines = input("Enter the number of lines (min 5) or ""exit"" to terminate :")
        if number_of_lines.isdigit():
            number_of_lines = int(number_of_lines)
            if number_of_lines >= 5:
                return number_of_lines
        elif isinstance(number_of_lines, str):
            if number_of_lines == 'exit':
                print("Exiting the program")
                exit(0)


# Request input for the number of columns for the board
def number_columns_input():
    while True:
        number_of_columns = input("Enter the number of columns (min 5) or ""exit"" to terminate :")
        if number_of_columns.isdigit():
            number_of_columns = int(number_of_columns)
            if number_of_columns >= 5:
                return number_of_columns
        elif isinstance(number_of_columns, str):
            if number_of_columns == 'exit':
                print("Exiting the program")
                exit(0)


# Request input on the number of obstacles to be randomly present in the game
def number_bricks_input(lines, columns):
    while True:
        bricks = input("Enter the number of bricks ▓ (min 1 & max " + str(int(lines * columns / 3)) + " ): ")
        if bricks.isdigit():
            bricks = int(bricks)
            if 1 <= bricks <= lines * columns / 3:
                return bricks


def add_game_frame(lines, columns, array_input):
    # design the frame of the game board - setting the corners
    array_input[0][0] = '┌'
    array_input[0][columns + 1] = '┐'
    array_input[lines + 1][0] = '└'
    array_input[lines + 1][columns + 1] = '┘'
    # design the frame of the game board - setting the side, top and bottom borders
    c = 0
    l = 0
    while l < lines + 3:
        while c < columns + 3:
            if l == 0 and 0 < c < columns + 1:
                array_input[l][c] = '─'
            elif 0 < l < lines + 1 and (c == 0 or c == columns + 1):
                array_input[l][c] = '│'
            elif l == lines + 1 and 0 < c < columns + 1:
                array_input[l][c] = '─'
            c += 1
        c = 0
        l += 1
    return


# set the starting point of the maze randomly and assign the STARTING_CHAR symbol in CYAN
def add_STARTING_CHAR(lines, columns, array_input):
    output_square = board_square.copy()
    output_square['colour'] = CYAN_T
    output_square['char'] = STARTING_CHAR
    output_square['line'] = random.randint(1, lines)
    output_square['column'] = random.randint(1, columns)
    # write the starting char in the array
    array_input[output_square['line']][output_square['column']] = STARTING_CHAR
    return output_square


# set the target destination point of the maze randomly and assign the "X" symbol
def add_TARGET_CHAR(lines, columns, start_square, array_input):
    output_square = board_square.copy()
    output_square['line'] = random.randint(1, lines)
    output_square['column'] = random.randint(1, columns)
    output_square['colour'] = RED_T
    output_square['char'] = TARGET_CHAR
    while abs(output_square['line'] - start_square['line']) < 3 and abs(
            output_square['column'] - start_square['column']) < 3:  # allow at least 3 spaces between start and target
        output_square['line'] = random.randint(1, lines)
        output_square['column'] = random.randint(1, columns)
    # write the target char in the array
    array_input[output_square['line']][output_square['column']] = TARGET_CHAR
    return output_square


# distribute the bricks randomly through the game not overlapping with "X" and "0" positions
def add_bricks(lines, columns, bricks, array_input):
    brick_list = []
    i = bricks
    while i > 0:  # allow at least 3 spaces between start and target
        brick_line = random.randint(1, lines)
        brick_column = random.randint(1, columns)
        if array_input[brick_line][brick_column] == EMPTY_CHAR:
            array_input[brick_line][brick_column] = BRICK_CHAR
            brick_square = board_square.copy()
            brick_square['line'] = brick_line
            brick_square['column'] = brick_column
            brick_square['colour'] = RED_T
            brick_square['char'] = BRICK_CHAR
            brick_square['visited']: False
            brick_list.append(brick_square)
            i = i - 1
    return brick_list


# write the path in the game board using the path returned by find path (passed in the argument
def add_path(array_path, array_input):
    for item in array_path:
        array_input[item['line']][item['column']] = item['char']
    return


# finds the path backwars, from the destination to the initial point by navigating through the 'previous_line' and 'previous_column'
def return_path(initial_square, destination_square, visited_array):
    path_way = []
    working_square = visited_array[destination_square['line']][destination_square['column']].copy()
    if working_square['previous_line'] == -1 or working_square['previous_column'] == -1:
        return path_way
    working_square = visited_array[working_square['previous_line']][working_square['previous_column']].copy()
    while working_square['line'] != initial_square['line'] or working_square['column'] != initial_square['column']:
        working_square['char'] = PATH_CHAR
        working_square['colour'] = CYAN_T
        path_way.append(working_square)
        working_square = visited_array[working_square['previous_line']][working_square['previous_column']].copy()
    return path_way


#  adds to the discover queue all the valid neighbour squares to a given input square and updates the visited array
def add_neighbours(input_square, discover_queue, visited_array):
    my_neighbours = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    for x in my_neighbours:
        line = input_square['line'] + x[0]
        column = input_square['column'] + x[1]
        if line >= 1 and line <= len(visited_array) - 2:
            if column >= 1 and column <= len(visited_array[0]) - 2:
                if visited_array[line][column]['visited'] == False:
                    visited_array[line][column]['visited'] = True
                    visited_array[line][column]['previous_line'] = input_square['line']
                    visited_array[line][column]['previous_column'] = input_square['column']

                    working_square = board_square.copy()
                    working_square['visited'] = False
                    working_square['line'] = line
                    working_square['column'] = column
                    working_square['previous_line'] = input_square['line']
                    working_square['previous_column'] = input_square['column']
                    discover_queue.insert(0, working_square)
    return


#  Main functiona to find the shortest path between source and destination using the BFS method
def find_path(initial_square, destination_square, array_input):
    # initialize the array for tracking the visited squares for the search algorithm
    # by default the BFS_square sets the visited field as False
    visited_array = [[board_square.copy() for x in range(len(array_input[0]))] for y in range(len(array_input))]

    # mark non empty spaces as visited in the visited_array (except target square)
    line = 0
    column = 0
    while line < len(array_input):
        while column < len(array_input[line]):
            visited_array[line][column]['line'] = line
            visited_array[line][column]['column'] = column
            if array_input[line][column] != EMPTY_CHAR and array_input[line][column] != TARGET_CHAR:
                visited_array[line][column]['visited'] = True  # borders, bricks and start position are set to visited
            column += 1
        column = 0
        line += 1

    # create a new copy of a BFS_square with the starting position and add it to the head of the queue
    new_square = board_square.copy()
    new_square['line'] = initial_square['line']
    new_square['column'] = initial_square['column']

    discover_queue = []
    discover_queue.append(new_square)

    while len(discover_queue) > 0:
        working_square = discover_queue.pop()
        if working_square['line'] == destination_square['line'] and working_square['column'] == destination_square[
            'column']:
            break
        else:
            if working_square['visited'] == False:
                #                working_square['visited'] = True
                add_neighbours(working_square, discover_queue, visited_array)
    i = 1

    path_way = return_path(initial_square, destination_square, visited_array)
    return path_way


# define clear function to clear the console
def clear_console():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


key_types = ("ESC", "right", "left", "up", "down", "space")



def wait_key():
#    ''' Wait for a key press on the console and return it. '''
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    return result

def move_path(position, direction, array_input):
    my_position = position.copy()
    if direction == 'up':
        my_position['line'] -= 1
    elif direction == 'down':
        my_position['line'] += 1
    elif direction == 'left':
        my_position['column'] -= 1
    elif direction == 'right':
        my_position['column'] += 1

    if array_input[my_position['line']][my_position['column']] == EMPTY_CHAR or array_input[my_position['line']][my_position['column']] == TARGET_CHAR:
        array_input[my_position['line']][my_position['column']] = PATH_CHAR
        return my_position
    return position



def gamer_mode(initial_square, destination_square, array_input):
    my_position = initial_square.copy()
    gamer_board = copy.deepcopy(array_input)
    print_array_Colour(gamer_board)
    print("Use the arrow keys to move from your position (0), press 'q' to quite the game or space to play again")
    while True:
        key = wait_key()
        if key == 'q':
            print('Quiting the game...')
            exit(0)
        elif key == ' ':
            print('Will show you th correct answer and restart the game.')
            break
        elif key == '[':
            key = wait_key()
            if key == 'A':   # Arrow up key pressed - move up
                my_position = move_path(my_position, 'up', gamer_board)
            elif key == 'B':    #  Arrow down key pressed - move down
                my_position = move_path(my_position, 'down', gamer_board)
            elif key == 'C':  #  Arrow right key pressed - move right
                my_position = move_path(my_position, 'right', gamer_board)
            elif key == 'D':  # Arrow left key pressed - move left
                my_position = move_path(my_position, 'left', gamer_board)
            else:
                print('You pressed a normal key: ' + key)
                continue
        clear_console()
        print_array_Colour(gamer_board)
        if my_position['line'] == destination_square['line'] and my_position['column'] == destination_square['column']:
            print("congratulations you reached the target")
            return
    return


###################   Main Program Start  #############################################################################

while True:
    number_lines = number_lines_input()  # get input for the number of lines and store the result
    number_columns = number_columns_input()  # get input for the number of columns and store the result
    number_bricks = number_bricks_input(number_lines,
                                        number_columns)  # get input for the number of bricks and store the result
    retries = 0
    while True:
        board = [[' ' for x in range(number_columns + 2)] for y in
                 range(number_lines + 2)]  # initialize the 2 dimension array of the maze game board with spaces
        add_game_frame(number_lines, number_columns,
                       board)  # insert the frame characters of the game board in the array 'board'
        start_square = dict(add_STARTING_CHAR(number_lines, number_columns,
                                              board))  # insert the starting point character in the array 'board' and get the values in the format of 'board_square' dictionary
        target_square = dict(add_TARGET_CHAR(number_lines, number_columns, start_square,
                                             board))  # insert the target point character in the array 'board'
        brick_list = add_bricks(number_lines, number_columns, number_bricks,
                                board)  # insert all the brick characters in the array 'board'
        gamer_mode(start_square, target_square, board)  # print in black and white before the path is discovered
        path_list = find_path(start_square, target_square,
                              board)  # find path on the board array from start to target positions avoiding bricks
        if len(path_list) > 0:
            break
        else:
            print('Run ' + str(
                retries) + ' It was not possible to find a path, retrying ... \n \n')  # print the output result of the game
            retries += 1

    add_path(path_list,
             board)  # add the path to the board array by replacing the empty squares with PATH_CHAR characters
    print(
        "\nThe symbol 0 marks the starting point and T marks the target destination")  # print the output result of the game
    print_array_Colour(board)  # print the same in colours
