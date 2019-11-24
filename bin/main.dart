import 'dart:io';
import 'dart:math';
import 'package:Maze_using_Dart/Maze_using_Dart.dart' as Maze_using_Dart;


main(List<String> arguments) {
//    print('Hello world: ${Maze_using_Dart.calculate()}!');
    print("Please enter the number of lines for the Maze (bigger that 4): ");
    int numberOfLines = number_input(5);

    print("Please enter the number of Columns for the Maze (bigger that 4): ");
    int numberOfColumns = number_input(5);

    print("Please enter the number of Bricks for the Maze (bigger that 4): ");
    int numberOfBrics = number_input(5);

    //  initialize the game grid List of Lists
    //  add 2 additional lines and columns to accommodate the framing around the game
    final grid = List<List<String>>.generate(
        numberOfLines + 2, (i) => List<String>.generate(numberOfColumns + 2, (j) => " "));

    initialize_borders(grid);

    var startingPosition = get_start_position(grid);
    print(startingPosition);
    grid[startingPosition["line"]][startingPosition["column"]] = "0";

    print_grid_BW(grid);
}

get_start_position(gameGrid) {
    Map<String, int> position = {
        "line" : 0,
        "column" : 0
    };
    var rng = new Random(100);
    position["line"] = rng.nextInt(gameGrid.length-1);
    if (position["line"] == 0) {    //  checks if it overlaps with the frame
        position["line"] = 1;
    }
    position["column"] = rng.nextInt(gameGrid[0].length-1);
    if (position["column"] == 0) {  //  checks if it overlaps with the frame
        position["column"] = 1;
    }
    return position;
}

void print_grid_BW(gameGrid) {
//    gameGrid.forEach((element) => print(element.toString()));
    print("\n");
    for (int line=0; line < gameGrid.length; line++) {  // print list using traditional for loop
        for(int column = 0; column < gameGrid[line].length; column++) {
            stdout.write(gameGrid[line][column]);
        }
        stdout.write("\n");
    }
}

void initialize_borders(gameGrid) {
    int lines = gameGrid.length;
    int columns = gameGrid[0].length;

    // design the frame of the game board - setting the corners
    gameGrid[0][0] = "┌";
    gameGrid[0][columns - 1] = "┐";
    gameGrid[lines - 1][0] = "└";
    gameGrid[lines - 1][columns - 1] = "┘";

    // design the frame of the game board - setting the top and bottom frames
    for (int i = 1; i < columns - 1; i++) {
        gameGrid[0][i] = '─';
        gameGrid[lines - 1][i] = '─';
    };

    // design the frame of the game board - setting the left and right frames
    for (int i = 1; i < lines - 1; i++) {
        gameGrid[i][0] = '│';
        gameGrid[i][columns - 1] = '│';
    };
}

int number_input(int minNumber) {
    int numberOfLines = 0;
    while (true) {
        try{
            numberOfLines = int.parse(stdin.readLineSync());
        } on FormatException {
            continue;
        }
        if(numberOfLines >= minNumber) {
            return numberOfLines;
        }
    }
}
