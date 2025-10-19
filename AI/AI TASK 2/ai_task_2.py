"""
Tic-Tac-Toe AI (Unbeatable)
---------------------------
- Human vs AI in the terminal
- AI uses Minimax + Alpha-Beta Pruning
- Supports choosing X or O, first/second player
- Clear board rendering and robust input validation
"""

from typing import List, Optional, Tuple

# Types
Board = List[str]  # 9 cells: 'X', 'O', or ' '
Player = str       # 'X' or 'O'

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6)              # diagonals
]

def print_board(board: Board) -> None:
    cells = [c if c != ' ' else str(i + 1) for i, c in enumerate(board)]
    print(f"\n {cells[0]} | {cells[1]} | {cells[2]}")
    print("---+---+---")
    print(f" {cells[3]} | {cells[4]} | {cells[5]}")
    print("---+---+---")
    print(f" {cells[6]} | {cells[7]} | {cells[8]}\n")

def winner(board: Board) -> Optional[Player]:
    for a, b, c in WIN_LINES:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_full(board: Board) -> bool:
    return all(c != ' ' for c in board)

def available_moves(board: Board) -> List[int]:
    return [i for i, c in enumerate(board) if c == ' ']

def minimax(board: Board, ai: Player, human: Player,
            depth: int, alpha: int, beta: int,
            maximizing: bool) -> Tuple[int, Optional[int]]:
    # Terminal checks
    w = winner(board)
    if w == ai:
        return 10 - depth, None
    if w == human:
        return depth - 10, None
    if is_full(board):
        return 0, None

    best_move: Optional[int] = None

    # Move ordering: try center, corners, edges (helps pruning)
    pref = [4, 0, 2, 6, 8, 1, 3, 5, 7]
    moves = [m for m in pref if board[m] == ' ']

    if maximizing:
        value = -10**9
        for m in moves:
            board[m] = ai
            score, _ = minimax(board, ai, human, depth + 1, alpha, beta, False)
            board[m] = ' '
            if score > value:
                value, best_move = score, m
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value, best_move
    else:
        value = 10**9
        for m in moves:
            board[m] = human
            score, _ = minimax(board, ai, human, depth + 1, alpha, beta, True)
            board[m] = ' '
            if score < value:
                value, best_move = score, m
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value, best_move

def ai_move(board: Board, ai: Player, human: Player) -> int:
    # If AI can win in 1, do it; if must block, do it (fast checks)
    for m in available_moves(board):
        board[m] = ai
        if winner(board) == ai:
            board[m] = ' '
            return m
        board[m] = ' '
    for m in available_moves(board):
        board[m] = human
        if winner(board) == human:
            board[m] = ' '
            return m
        board[m] = ' '
    # Otherwise use minimax
    _, move = minimax(board, ai, human, depth=0, alpha=-10**9, beta=10**9, maximizing=True)
    return move if move is not None else available_moves(board)[0]

def read_human_move(board: Board) -> int:
    while True:
        raw = input("Your move (1-9): ").strip()
        if not raw.isdigit():
            print("Please enter a number from 1 to 9.")
            continue
        pos = int(raw) - 1
        if pos < 0 or pos > 8:
            print("Out of range. Choose 1-9.")
            continue
        if board[pos] != ' ':
            print("That cell is taken. Choose another.")
            continue
        return pos

def choose_symbol() -> Tuple[Player, Player]:
    while True:
        s = input("Choose your symbol (X/O): ").strip().upper()
        if s in ("X", "O"):
            human = s
            ai = "O" if human == "X" else "X"
            return human, ai
        print("Invalid choice. Enter X or O.")

def choose_first(human: Player) -> Player:
    while True:
        s = input("Who goes first? (Y)ou / (A)I: ").strip().lower()
        if s in ("y", "you"):
            return human
        if s in ("a", "ai", "computer"):
            return "O" if human == "X" else "X"
        print("Invalid choice. Type Y or A.")

def play_once() -> None:
    board: Board = [' '] * 9
    human, ai = choose_symbol()
    turn: Player = choose_first(human)

    print("\nBoard positions are numbered 1-9 as shown:\n")
    print_board(['1','2','3','4','5','6','7','8','9'])

    while True:
        print_board(board)
        if winner(board) or is_full(board):
            break

        if turn == human:
            print("Your turn.")
            move = read_human_move(board)
            board[move] = human
            turn = ai
        else:
            print("AI is thinking...")
            move = ai_move(board, ai, human)
            board[move] = ai
            turn = human

    print_board(board)
    w = winner(board)
    if w == human:
        print("You win! 🎉 (That’s rare!)")
    elif w == ai:
        print("AI wins! 🤖 (Unbeatable strikes again.)")
    else:
        print("It's a draw! 🤝")

def main():
    print("=== Tic-Tac-Toe (Unbeatable AI) ===")
    while True:
        play_once()
        again = input("\nPlay again? (Y/N): ").strip().lower()
        if again not in ("y", "yes"):
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
