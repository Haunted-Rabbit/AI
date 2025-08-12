from tkinter import *
import random

def minimax(board, depth, is_maximizing):
    # Base cases: Check if game is over
    if check_ai_winner(board, "O"):  # AI wins
        return 1
    elif check_ai_winner(board, "X"):  # You win
        return -1
    elif not empty_spaces_ai(board):  # Draw
        return 0

    if is_maximizing:  # AI's turn (maximize score)
        best_score = -float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ""
                    best_score = max(score, best_score)
        return best_score
    else:  # Your turn (minimize score)
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ""
                    best_score = min(score, best_score)
        return best_score
    
def check_ai_winner(board, player):
    # Check rows, columns, diagonals (for a given board state)
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]):  # Rows
            return True
        if all([board[j][i] == player for j in range(3)]):  # Columns
            return True
    if all([board[i][i] == player for i in range(3)]):  # Diagonal 1
        return True
    if all([board[i][2 - i] == player for i in range(3)]):  # Diagonal 2
        return True
    return False

def empty_spaces_ai(board):
    return any(board[i][j] == "" for i in range(3) for j in range(3))

def ai_move():
    best_score = -float("inf")
    best_move = None
    board = [[buttons[i][j]["text"] for j in range(3)] for i in range(3)]  # Get current board state

    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = "O"  # AI is "O"
                score = minimax(board, 0, False)  # Simulate
                board[row][col] = ""
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    
    if best_move:
        buttons[best_move[0]][best_move[1]].invoke()  # Trigger the button click
        



def next_turn(row, column):
    global player

    if buttons[row][column]['text'] == "" and not check_winner():
        buttons[row][column]['text'] = player
        
        if check_winner():
            label.config(text=f"{player} wins!")
        elif not empty_spaces():
            label.config(text="It's a draw!")
        else:
            player = "O" if player == "X" else "X"  # Switch player
            label.config(text=f"{player}'s turn")
            
            if player == "O":  # AI's turn
                window.after(500, ai_move)  # Delay for UX

def check_winner():
    # Check rows
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            highlight_winner(row, 0, row, 1, row, 2)
            return True

    # Check columns
    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
            highlight_winner(0, column, 1, column, 2, column)
            return True

    # Check diagonals
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        highlight_winner(0, 0, 1, 1, 2, 2)
        return True
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        highlight_winner(0, 2, 1, 1, 2, 0)
        return True
    
    return False

def highlight_winner(r1, c1, r2, c2, r3, c3):
    buttons[r1][c1].config(bg="green")
    buttons[r2][c2].config(bg="green")
    buttons[r3][c3].config(bg="green")

def empty_spaces():
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] == "":
                return True
    return False

def new_game():
    global player
    player = random.choice(players)
    label.config(text=f"{player}'s turn")
    
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="", bg="#F7F1F1")


#for splash screen
from PIL import ImageTk, Image
import tkinter as tk
import time

def start_main_window():
    splash.destroy()

# Splash screen setup
splash = tk.Tk()
splash.overrideredirect(True)  # Remove border/title bar
splash.geometry("400x300+500+250")  # Width x Height + X + Y

image = ImageTk.PhotoImage(Image.open("splash.png"))
label = tk.Label(splash, image=image)
label.pack()

# Optional background or image
splash.configure(bg="white")
label = tk.Label(splash, text="Welcome to Tic Tac Toe!", font=("Arial", 20), bg="white")
label.pack(expand=True)

# Show splash for 2 seconds then launch main
splash.after(2000, start_main_window)

splash.mainloop()




# Initialize the game window

window = Tk()
window.title("Tic Tac Toe")
window.config(bg="#36A2D4")

players = ["X", "O"]
player = random.choice(players)

# Game title
label1 = Label(window, text="Tic Tac Toe", font=("Arial", 40), bg="black", fg="white")
label1.pack()

# Turn indicator
label = Label(window, text=f"{player}'s turn", font=("Arial", 20), bg="red", fg="white")
label.pack()

# Game board
frame = Frame(window)
frame.pack()

buttons = []
for i in range(3):
    row = []
    for j in range(3):
        button = Button(frame, text="", font=("Arial", 20), width=5, height=2,
                       highlightbackground="black", highlightthickness=2,
                       relief="solid", command=lambda r=i, c=j: next_turn(r, c))
        button.grid(row=i, column=j, padx=5, pady=5)
        row.append(button)
    buttons.append(row)

# Reset button
reset_button = Button(window, text="Restart", font=('Arial', 20), command=new_game)
reset_button.pack(pady=10)

label3 = Label(window,text="Developer: Bunny",font=('Helvetica',10),fg="black",bg="#15C39D")
label3.pack()
window.mainloop()
