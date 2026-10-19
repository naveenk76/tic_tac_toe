import random

board = [" " for _ in range(9)]


def show_board():
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()


def check_winner(player):
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for combination in winning_combinations:
        if (
            board[combination[0]] == player
            and board[combination[1]] == player
            and board[combination[2]] == player
        ):
            return True

    return False


def ai_move():
    # 1. Win if possible
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"

            if check_winner("O"):
                return

            board[i] = " "

    # 2. Block the player's winning move
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"

            if check_winner("X"):
                board[i] = "O"
                return

            board[i] = " "

    # 3. Take the center if available
    if board[4] == " ":
        board[4] = "O"
        return

    # 4. Otherwise choose a random empty position
    empty_positions = []

    for i in range(9):
        if board[i] == " ":
            empty_positions.append(i)

    if empty_positions:
        position = random.choice(empty_positions)
        board[position] = "O"


def play_game():
    print("=== TIC TAC TOE ===")
    print("You are X. The AI is O.")
    print("Choose a position from 1 to 9.")

    print("""
     1 | 2 | 3
    ---+---+---
     4 | 5 | 6
    ---+---+---
     7 | 8 | 9
    """)

    while True:
        show_board()

        # Player's turn
        try:
            choice = int(input("Enter your position (1-9): "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice < 1 or choice > 9:
            print("Choose a number between 1 and 9.")
            continue

        if board[choice - 1] != " ":
            print("That position is already occupied!")
            continue

        board[choice - 1] = "X"

        if check_winner("X"):
            show_board()
            print("Congratulations! You defeated the AI!")
            break

        if " " not in board:
            show_board()
            print("It's a draw!")
            break

        # AI's turn
        ai_move()
        print("AI has made its move.")

        if check_winner("O"):
            show_board()
            print("The AI wins! Better luck next time.")
            break

        if " " not in board:
            show_board()
            print("It's a draw!")
            break


play_game()
