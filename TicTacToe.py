import os;
import random;
import copy;

def clearTerminal() -> None:
    os.system( "cls" if os.name == "nt" else "clear"); # Clear terminal output. These are just system commands that clear display. Windows == nt -> "cls", POSIX (Unix, Linux, MacOS, etc) != nt -> "clear"

def cyanText(string: str) -> str:
    return f"\033[96m{string}\033[00m"; # Uses ANSI Escape Codes to change the text color that is outputted. Only works if the terminal supports it.

def greenText(string: str) -> str:
    return f"\033[92m{string}\033[00m"; # Uses ANSI Escape Codes to change the text color that is outputted. Only works if the terminal supports it.

def drawGameboard(board: list, playersCharacter: str, statusMessage: str = "") -> None:
    clearTerminal();
    boardStateText = [cyanText(text) if text == playersCharacter else greenText(text) if text != "" else index for index, text in enumerate(board)]; # Create a list of labels for each position (either its index or the currently placed piece)

    # Print board as a neat table
    print(f"""{statusMessage}\nYou are playing as {cyanText(playersCharacter)}
    
 {boardStateText[0]} │ {boardStateText[1]} │ {boardStateText[2]}
───│───│───
 {boardStateText[3]} │ {boardStateText[4]} │ {boardStateText[5]}
───│───│─── 
 {boardStateText[6]} │ {boardStateText[7]} │ {boardStateText[8]} 
    """);
    
def ask(query: str, allowedResponses: list) -> str:
    result = input(query).lower().strip(); # Make string lowercase and strip and whitespaces that may be at the start and end
    if result in allowedResponses:
        return result;
    else:
        print("Unexpected Input Provided. Please try again.")
        return ask(query, allowedResponses); # Reask question to make sure a result within the "allowedResponses" is given   
    
def coinFlip() -> tuple:
    print("To decide who goes first we will flip a coin.");
    userCoinSelection = ask("Heads or Tails? (heads, tails): ", ["tails", "heads"]); 
    randomCoinSelection = random.SystemRandom().choice(["tails", "heads"]); # OS provided randomness that randomly selects heads or tails
    return (
        userCoinSelection == randomCoinSelection, # user starts first
        "X" if userCoinSelection == randomCoinSelection else "O", # playersCharacter
        "O" if userCoinSelection == randomCoinSelection else "X", # computersCharacter
    );

def checkWin(board: list) -> tuple:
    # Returns true if the game has ended and why it ended.
    # Check if all tiles are filled for draw
    if "" not in board: return (True, "Draw.");

    # Check horizontal.
    if board[0] == board[1] == board[2] and board[0] != "": return (True, board[0]);
    if board[3] == board[4] == board[5] and board[3] != "": return (True, board[3]);
    if board[6] == board[7] == board[8] and board[6] != "": return (True, board[6]);

    # Check vertical
    if board[0] == board[3] == board[6] and board[0] != "": return (True, board[0]);
    if board[1] == board[4] == board[7] and board[1] != "": return (True, board[1]);
    if board[2] == board[5] == board[8] and board[2] != "": return (True, board[2]);

    # Check diagonals
    if board[0] == board[4] == board[8] and board[0] != "": return (True, board[4]);
    if board[6] == board[4] == board[2] and board[6] != "": return (True, board[4]);

    return (False, " "); # Nobody has won
    
def computerLogic(board: list, computersCharacter: str, playersCharacter: str) -> list:
    # Check if computer can win in next move
    for index, played in enumerate(board):
        if played == "":
            boardCopy = copy.deepcopy(board);
            boardCopy[index] = computersCharacter;
            gameEnded, whoWon = checkWin(boardCopy);
            if gameEnded == True and whoWon == computersCharacter:
                return boardCopy;

    # Blocks player if they can win in next move
    for index, played in enumerate(board):
        if played == "":
            boardCopy = copy.deepcopy(board);
            boardCopy[index] = playersCharacter;
            gameEnded, whoWon = checkWin(boardCopy);
            if gameEnded == True and whoWon == playersCharacter:
                boardCopy[index] = computersCharacter;
                return boardCopy;    

    
    avaliableCorners = [index for index in [0, 2, 4, 6, 8] if board[index] == ""];
    avaliable = [index for index in range(len(board)) if board[index] == ""];

    # Randomly picks any avaliable corner or centre or it moves on
    if avaliableCorners:
        boardCopy = copy.deepcopy(board);
        boardCopy[random.SystemRandom().choice(avaliableCorners)] = computersCharacter;
        return boardCopy;

    # Randomly picks any avaliable space left over
    if avaliable:
        boardCopy = copy.deepcopy(board);
        boardCopy[random.SystemRandom().choice(avaliable)] = computersCharacter;
        return boardCopy;
    
def mainLoop() -> None:
    clearTerminal();
    playersTurn, playersCharacter, computersCharacter = coinFlip();
    board = [""] * 9; # Init empty array for board state
    drawGameboard(board, playersCharacter, "You go first!" if playersTurn else "");

    while True:
        avaliableSpaces = [str(index) for index in range(len(board)) if board[index] == ""]; # Get all avaliable spaces

        gameEnd, whoWon = checkWin(board); 
        if gameEnd: # If the game has ended
            drawGameboard(board, playersCharacter, greenText("Computer Won!") if whoWon == computersCharacter else cyanText("You Won!") if whoWon == playersCharacter else whoWon); # Print out who won or just a newline
            return mainLoop() if ask("Would you like to play again? (yes, no): ", ["yes", "no"]) == "yes" else None; # If the user wants to play again, recall the function. Otherwise return nothing.

        if playersTurn:
            command = ask("Where would you like to go? (pick a number on the board): ", avaliableSpaces + ["exit"]);
            if command == "exit": # Enable exit as a command that just quits the program
                quit();
            board[int(command)] = playersCharacter;
        elif not playersTurn:
            board = computerLogic(board, computersCharacter, playersCharacter);

        playersTurn = not playersTurn;
        drawGameboard(board, playersCharacter);

mainLoop(); # Start loop