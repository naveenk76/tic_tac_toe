
import tkinter as tk
from tkinter import messagebox
import random

# -------------------------------
# COLORS AND SETTINGS
# -------------------------------

WHITE = "#FFFFFF"
BACKGROUND = "#F2F6FC"
BLUE = "#2563EB"
DARK_BLUE = "#1E3A8A"
LIGHT_BLUE = "#DBEAFE"
TEXT = "#1E293B"
MUTED = "#64748B"
GREEN = "#16A34A"
ORANGE = "#EA580C"

BOARD_SIZE = 9

board = [" " for _ in range(BOARD_SIZE)]
buttons = []

game_mode = "AI"
difficulty = "Medium"
game_over = False

scores = {
    "player": 0,
    "ai": 0,
    "player2": 0,
    "draw": 0
}

# -------------------------------
# WINNING COMBINATIONS
# -------------------------------

WINNING_COMBINATIONS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
]


# -------------------------------
# GAME LOGIC
# -------------------------------

def check_winner(player):
    for combo in WINNING_COMBINATIONS:
        if all(board[i] == player for i in combo):
            return combo
    return None


def is_draw():
    return " " not in board


def find_winning_move(player):
    for i in range(BOARD_SIZE):
        if board[i] == " ":
            board[i] = player

            if check_winner(player):
                board[i] = " "
                return i

            board[i] = " "

    return None


# -------------------------------
# AI
# -------------------------------

def easy_ai():
    empty_positions = [
        i for i in range(BOARD_SIZE)
        if board[i] == " "
    ]

    return random.choice(empty_positions)


def medium_ai():
    # Win when possible
    move = find_winning_move("O")

    if move is not None:
        return move

    # Block the human player's win
    move = find_winning_move("X")

    if move is not None:
        return move

    # Prefer the center
    if board[4] == " ":
        return 4

    # Prefer corners
    corners = [
        i for i in (0, 2, 6, 8)
        if board[i] == " "
    ]

    if corners:
        return random.choice(corners)

    return easy_ai()


def minimax(is_ai_turn, depth=0):
    if check_winner("O"):
        return 10 - depth

    if check_winner("X"):
        return depth - 10

    if is_draw():
        return 0

    if is_ai_turn:
        best_score = float("-inf")

        for i in range(BOARD_SIZE):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False, depth + 1)
                board[i] = " "
                best_score = max(best_score, score)

        return best_score

    best_score = float("inf")

    for i in range(BOARD_SIZE):
        if board[i] == " ":
            board[i] = "X"
            score = minimax(True, depth + 1)
            board[i] = " "
            best_score = min(best_score, score)

    return best_score


def hard_ai():
    best_score = float("-inf")
    best_move = None

    for i in range(BOARD_SIZE):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False, 1)
            board[i] = " "

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


def get_ai_move():
    if difficulty == "Easy":
        return easy_ai()

    if difficulty == "Medium":
        return medium_ai()

    return hard_ai()


# -------------------------------
# GUI UPDATES
# -------------------------------

def update_scoreboard():
    player_score.config(
        text=f"YOU\n{scores['player']}"
    )

    if game_mode == "AI":
        opponent_score.config(
            text=f"AI\n{scores['ai']}"
        )
    else:
        opponent_score.config(
            text=f"PLAYER 2\n{scores['player2']}"
        )

    draw_score.config(
        text=f"DRAWS\n{scores['draw']}"
    )


def set_status(message, color=TEXT):
    status_label.config(
        text=message,
        fg=color
    )


def update_board():
    for i in range(BOARD_SIZE):
        if board[i] == "X":
            buttons[i].config(
                text="X",
                fg=BLUE,
                disabledforeground=BLUE
            )

        elif board[i] == "O":
            buttons[i].config(
                text="O",
                fg=ORANGE,
                disabledforeground=ORANGE
            )

        else:
            buttons[i].config(
                text="",
                fg=TEXT
            )


def highlight_winner(combo):
    for i in combo:
        buttons[i].config(
            bg=LIGHT_BLUE,
            activebackground=LIGHT_BLUE
        )


def enable_board():
    for i in range(BOARD_SIZE):
        if board[i] == " ":
            buttons[i].config(
                state="normal",
                bg=WHITE
            )


def disable_board():
    for button in buttons:
        button.config(state="disabled")


# -------------------------------
# GAME FLOW
# -------------------------------

def finish_game(winner):
    global game_over

    game_over = True
    disable_board()

    if winner == "X":
        if game_mode == "AI":
            scores["player"] += 1
            message = "You win! Great job!"
        else:
            scores["player"] += 1
            message = "Player 1 wins!"

        color = GREEN

    elif winner == "O":
        if game_mode == "AI":
            scores["ai"] += 1
            message = "The AI wins. Try again!"
        else:
            scores["player2"] += 1
            message = "Player 2 wins!"

        color = ORANGE

    else:
        scores["draw"] += 1
        message = "It's a draw!"
        color = DARK_BLUE

    combo = check_winner(winner) if winner else None

    if combo:
        highlight_winner(combo)

    update_scoreboard()
    set_status(message, color)


def check_game_state(player):
    if check_winner(player):
        finish_game(player)
        return True

    if is_draw():
        finish_game(None)
        return True

    return False


def player_move(position):
    global game_over

    if game_over or board[position] != " ":
        return

    board[position] = "X"
    buttons[position].config(state="disabled")
    update_board()

    if check_game_state("X"):
        return

    if game_mode == "TWO":
        set_status("Player 2's turn — choose a square", ORANGE)
    else:
        set_status("AI is thinking...", MUTED)
        disable_board()
        root.after(350, ai_turn)


def ai_turn():
    if game_over:
        return

    position = get_ai_move()

    if position is None:
        return

    board[position] = "O"
    buttons[position].config(state="disabled")
    update_board()

    if check_game_state("O"):
        return

    enable_board()
    set_status("Your turn — choose a square", BLUE)


def two_player_turn(position):
    global game_over

    if game_over or board[position] != " ":
        return

    # The board tells us whose turn it is.
    x_count = board.count("X")
    o_count = board.count("O")

    if x_count == o_count:
        current_player = "X"
    else:
        current_player = "O"

    board[position] = current_player
    buttons[position].config(state="disabled")
    update_board()

    if check_game_state(current_player):
        return

    if current_player == "X":
        set_status("Player 2's turn — choose a square", ORANGE)
    else:
        set_status("Player 1's turn — choose a square", BLUE)


def on_square_click(position):
    if game_over or board[position] != " ":
        return

    if game_mode == "AI":
        player_move(position)
    else:
        two_player_turn(position)


def restart_game():
    global board, game_over

    board = [" " for _ in range(BOARD_SIZE)]
    game_over = False

    for button in buttons:
        button.config(
            text="",
            state="normal",
            bg=WHITE,
            activebackground=LIGHT_BLUE,
            fg=TEXT
        )

    if game_mode == "AI":
        set_status("Your turn — choose a square", BLUE)
    else:
        set_status("Player 1's turn — choose a square", BLUE)


def change_mode(mode):
    global game_mode

    game_mode = mode

    if mode == "AI":
        ai_mode_button.config(
            bg=BLUE, fg=WHITE,
            relief="flat"
        )
        two_mode_button.config(
            bg=WHITE, fg=BLUE,
            relief="solid"
        )
        difficulty_menu.config(state="normal")
        set_status("Your turn — choose a square", BLUE)

    else:
        two_mode_button.config(
            bg=BLUE, fg=WHITE,
            relief="flat"
        )
        ai_mode_button.config(
            bg=WHITE, fg=BLUE,
            relief="solid"
        )
        difficulty_menu.config(state="disabled")
        set_status("Player 1's turn — choose a square", BLUE)

    update_scoreboard()
    restart_game()


def change_difficulty(value):
    global difficulty
    difficulty = value


def reset_scores():
    if messagebox.askyesno(
        "Reset scores",
        "Are you sure you want to reset all scores?"
    ):
        for key in scores:
            scores[key] = 0

        update_scoreboard()
        restart_game()


# -------------------------------
# MAIN WINDOW
# -------------------------------

root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("470x700")
root.resizable(False, False)
root.configure(bg=BACKGROUND)

# Header
header = tk.Frame(root, bg=BACKGROUND)
header.pack(fill="x", pady=(24, 12))

tk.Label(
    header,
    text="TIC TAC TOE",
    font=("Segoe UI", 25, "bold"),
    bg=BACKGROUND,
    fg=DARK_BLUE
).pack()

tk.Label(
    header,
    text="Challenge your strategy",
    font=("Segoe UI", 11),
    bg=BACKGROUND,
    fg=MUTED
).pack(pady=(4, 0))


# Mode selection
mode_frame = tk.Frame(root, bg=BACKGROUND)
mode_frame.pack(pady=12)

ai_mode_button = tk.Button(
    mode_frame,
    text="VS AI",
    width=12,
    font=("Segoe UI", 10, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=BLUE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=lambda: change_mode("AI")
)
ai_mode_button.grid(row=0, column=0, padx=5)

two_mode_button = tk.Button(
    mode_frame,
    text="2 PLAYERS",
    width=12,
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=BLUE,
    activebackground=LIGHT_BLUE,
    relief="solid",
    bd=1,
    cursor="hand2",
    command=lambda: change_mode("TWO")
)
two_mode_button.grid(row=0, column=1, padx=5)


# Difficulty selection
difficulty_frame = tk.Frame(root, bg=BACKGROUND)
difficulty_frame.pack(pady=(4, 12))

tk.Label(
    difficulty_frame,
    text="AI DIFFICULTY",
    font=("Segoe UI", 9, "bold"),
    bg=BACKGROUND,
    fg=MUTED
).pack(side="left", padx=8)

difficulty_var = tk.StringVar(value="Medium")

difficulty_menu = tk.OptionMenu(
    difficulty_frame,
    difficulty_var,
    "Easy",
    "Medium",
    "Hard",
    command=change_difficulty
)
difficulty_menu.config(
    font=("Segoe UI", 10),
    bg=WHITE,
    fg=TEXT,
    relief="solid",
    bd=1,
    highlightthickness=0,
    cursor="hand2"
)
difficulty_menu["menu"].config(
    font=("Segoe UI", 10),
    bg=WHITE
)
difficulty_menu.pack(side="left")


# Scoreboard
score_frame = tk.Frame(root, bg=BACKGROUND)
score_frame.pack(fill="x", padx=25, pady=10)

player_score = tk.Label(
    score_frame,
    text="YOU\n0",
    font=("Segoe UI", 12, "bold"),
    bg=WHITE,
    fg=BLUE,
    width=10,
    height=3,
    relief="solid",
    bd=1
)
player_score.pack(side="left", expand=True, fill="x", padx=4)

opponent_score = tk.Label(
    score_frame,
    text="AI\n0",
    font=("Segoe UI", 12, "bold"),
    bg=WHITE,
    fg=ORANGE,
    width=10,
    height=3,
    relief="solid",
    bd=1
)
opponent_score.pack(side="left", expand=True, fill="x", padx=4)

draw_score = tk.Label(
    score_frame,
    text="DRAWS\n0",
    font=("Segoe UI", 12, "bold"),
    bg=WHITE,
    fg=DARK_BLUE,
    width=10,
    height=3,
    relief="solid",
    bd=1
)
draw_score.pack(side="left", expand=True, fill="x", padx=4)


# Status message
status_label = tk.Label(
    root,
    text="Your turn — choose a square",
    font=("Segoe UI", 11, "bold"),
    bg=BACKGROUND,
    fg=BLUE
)
status_label.pack(pady=(8, 12))


# Game board
board_frame = tk.Frame(
    root,
    bg=BACKGROUND
)
board_frame.pack(padx=25, pady=5)

for i in range(BOARD_SIZE):
    button = tk.Button(
        board_frame,
        text="",
        font=("Segoe UI", 30, "bold"),
        width=4,
        height=1,
        bg=WHITE,
        fg=TEXT,
        activebackground=LIGHT_BLUE,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda position=i: on_square_click(position)
    )

    button.grid(
        row=i // 3,
        column=i % 3,
        padx=4,
        pady=4,
        ipadx=5,
        ipady=12
    )

    buttons.append(button)


# Controls
control_frame = tk.Frame(root, bg=BACKGROUND)
control_frame.pack(fill="x", padx=30, pady=22)

restart_button = tk.Button(
    control_frame,
    text="↻  Restart Game",
    font=("Segoe UI", 11, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=DARK_BLUE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=restart_game
)
restart_button.pack(fill="x", ipady=9)

reset_button = tk.Button(
    root,
    text="Reset all scores",
    font=("Segoe UI", 9),
    bg=BACKGROUND,
    fg=MUTED,
    activebackground=BACKGROUND,
    relief="flat",
    cursor="hand2",
    command=reset_scores
)
reset_button.pack()

update_scoreboard()

root.mainloop()
