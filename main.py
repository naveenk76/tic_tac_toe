
import random

# -----------------------------
# TIC TAC TOE - VERSION 2.0
# -----------------------------

WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

# ANSI colors for supported terminals
RESET = "\033[0m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"


def create_board():
    return [" " for _ in range(9)]


def show_board(board):
    print()
    for row in range(3):
        cells = []
        for col in range(3):
            position = row * 3 + col
            value = board[position]

            if value == "X":
                value = f"{CYAN}X{RESET}"
            elif value == "O":
                value = f"{YELLOW}O{RESET}"
            else:
                value = str(position + 1)

            cells.append(f" {value} ")

        print(" | ".join(cells))
        if row < 2:
            print("---+---+---")
    print()


def check_winner(board, player):
    for combo in WINNING_COMBINATIONS:
        if all(board[i] == player for i in combo):
            return True
    return False


def is_draw(board):
    return " " not in board


def get_player_move(board, player):
    while True:
        choice = input(
            f"Player {player}, choose a position (1-9), "
            "or Q to quit: "
        ).strip().lower()

        if choice == "q":
            return None

        if not choice.isdigit():
            print("Please enter a number from 1 to 9.")
            continue

        position = int(choice) - 1

        if position < 0 or position > 8:
            print("Position must be between 1 and 9.")
        elif board[position] != " ":
            print("That position is already occupied.")
        else:
            return position


# -----------------------------
# AI LOGIC
# -----------------------------

def find_winning_move(board, player):
    for i in range(9):
        if board[i] == " ":
            board[i] = player

            if check_winner(board, player):
                board[i] = " "
                return i

            board[i] = " "

    return None


def easy_ai(board):
    empty_positions = [
        i for i in range(9) if board[i] == " "
    ]
    return random.choice(empty_positions)


def medium_ai(board):
    # Win if possible
    move = find_winning_move(board, "O")
    if move is not None:
        return move

    # Block the player's winning move
    move = find_winning_move(board, "X")
    if move is not None:
        return move

    # Take the center
    if board[4] == " ":
        return 4

    # Prefer corners
    corners = [i for i in [0, 2, 6, 8] if board[i] == " "]
    if corners:
        return random.choice(corners)

    return easy_ai(board)


def minimax(board, is_ai_turn, depth=0):
    # AI wins
    if check_winner(board, "O"):
        return 10 - depth

    # Human wins
    if check_winner(board, "X"):
        return depth - 10

    if is_draw(board):
        return 0

    if is_ai_turn:
        best_score = float("-inf")

        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, False, depth + 1)
                board[i] = " "
                best_score = max(best_score, score)

        return best_score

    best_score = float("inf")

    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            score = minimax(board, True, depth + 1)
            board[i] = " "
            best_score = min(best_score, score)

    return best_score


def hard_ai(board):
    best_score = float("-inf")
    best_move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False, 1)
            board[i] = " "

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


def ai_move(board, difficulty):
    if difficulty == "1":
        position = easy_ai(board)
    elif difficulty == "2":
        position = medium_ai(board)
    else:
        position = hard_ai(board)

    board[position] = "O"
    print(f"\n{YELLOW}AI has chosen position "
          f"{position + 1}.{RESET}")


# -----------------------------
# GAME MODES
# -----------------------------

def play_game(mode, difficulty, scores):
    board = create_board()

    print("\nStarting a new game!")
    if mode == "1":
        print("You are X. The AI is O.")
    else:
        print("Player 1 is X. Player 2 is O.")

    while True:
        show_board(board)

        # X always starts
        position = get_player_move(board, "X")

        if position is None:
            print("Game cancelled.")
            return

        board[position] = "X"

        if check_winner(board, "X"):
            show_board(board)
            print(f"{GREEN}Player X wins!{RESET}")
            scores["x"] += 1
            break

        if is_draw(board):
            show_board(board)
            print("It's a draw!")
            scores["draw"] += 1
            break

        if mode == "1":
            ai_move(board, difficulty)
        else:
            show_board(board)
            position = get_player_move(board, "O")

            if position is None:
                print("Game cancelled.")
                return

            board[position] = "O"

        if check_winner(board, "O"):
            show_board(board)

            if mode == "1":
                print(f"{RED}The AI wins!{RESET}")
                scores["ai"] += 1
            else:
                print(f"{YELLOW}Player O wins!{RESET}")
                scores["o"] += 1

            break

        if is_draw(board):
            show_board(board)
            print("It's a draw!")
            scores["draw"] += 1
            break

    print("\n--- SCOREBOARD ---")
    print(f"Player X: {scores['x']}")
    if mode == "1":
        print(f"AI wins:  {scores['ai']}")
    else:
        print(f"Player O: {scores['o']}")
    print(f"Draws:    {scores['draw']}")


def choose_difficulty():
    while True:
        print("\nChoose AI difficulty:")
        print("1. Easy   - Random moves")
        print("2. Medium - Wins and blocks")
        print("3. Hard   - Minimax AI")

        choice = input("Enter choice (1-3): ").strip()

        if choice in ["1", "2", "3"]:
            return choice

        print("Invalid choice. Try again.")


def main():
    scores = {
        "x": 0,
        "o": 0,
        "ai": 0,
        "draw": 0
    }

    while True:
        print(f"\n{CYAN}==============================")
        print("       TIC TAC TOE 2.0")
        print("==============================" + RESET)
        print("1. Play against AI")
        print("2. Two-player mode")
        print("3. View scoreboard")
        print("4. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            difficulty = choose_difficulty()
            play_game("1", difficulty, scores)

        elif choice == "2":
            play_game("2", None, scores)

        elif choice == "3":
            print("\n--- TOTAL SCORES ---")
            print(f"Player X wins: {scores['x']}")
            print(f"Player O wins: {scores['o']}")
            print(f"AI wins:       {scores['ai']}")
            print(f"Draws:         {scores['draw']}")

        elif choice == "4":
            print("Thanks for playing. Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-4.")


if __name__ == "__main__":
    main()
