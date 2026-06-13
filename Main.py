def print_board(board):
    print("\n")
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < 2:
            print("-" * 9)
    print("\n")


def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def check_draw(board):
    return all(cell != " " for row in board for cell in row)


def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]


def minimax(board, depth, is_maximizing, alpha, beta):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = -100
        for row, col in get_available_moves(board):
            board[row][col] = "O"
            score = minimax(board, depth + 1, False, alpha, beta)
            board[row][col] = " "
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Beta cutoff — prune remaining branches
        return best_score
    else:
        best_score = 100
        for row, col in get_available_moves(board):
            board[row][col] = "X"
            score = minimax(board, depth + 1, True, alpha, beta)
            board[row][col] = " "
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # Alpha cutoff — prune remaining branches
        return best_score


def get_ai_move(board):
    best_score = -100
    best_move = None
    alpha = -100
    beta = 100
    for row, col in get_available_moves(board):
        board[row][col] = "O"
        score = minimax(board, 0, False, alpha, beta)
        board[row][col] = " "
        if score > best_score:
            best_score = score
            best_move = (row, col)
        alpha = max(alpha, best_score)
    return best_move


def get_human_move(board):
    while True:
        try:
            move = input("Your turn (X) -- enter row and column (1-3), e.g. '1 2': ")
            row, col = map(int, move.split())
            row -= 1
            col -= 1
            if not (0 <= row <= 2 and 0 <= col <= 2):
                print("ERROR: Out of range! Enter row and column between 1 and 3.")
                continue
            if board[row][col] != " ":
                print("ERROR: Position already taken! Choose another.")
                continue
            return row, col
        except (ValueError, IndexError):
            print("ERROR: Invalid input! Enter two numbers separated by a space, e.g. '2 3'.")


def play_game():
    board = [[" "] * 3 for _ in range(3)]

    print("*** Welcome to Tic Tac Toe! ***")
    print("You are X -- the AI is O.")
    print("Positions are entered as: row col (e.g. '1 2' = row 1, column 2)")

    choice = input("Do you want to go first? (y/n): ").strip().lower()
    human_first = choice == "y"
    current = "X" if human_first else "O"

    while True:
        print_board(board)

        if current == "X":
            row, col = get_human_move(board)
            board[row][col] = "X"
        else:
            print("AI is thinking...")
            row, col = get_ai_move(board)
            board[row][col] = "O"
            print(f"AI played: row {row + 1}, col {col + 1}")

        if check_winner(board, current):
            print_board(board)
            if current == "X":
                print("YOU WIN! The AI made a mistake!")
            else:
                print("AI WINS! Better luck next time.")
            break

        if check_draw(board):
            print_board(board)
            print("DRAW! Well played.")
            break

        current = "O" if current == "X" else "X"

    again = input("Play again? (y/n): ").strip().lower()
    if again == "y":
        play_game()
    else:
        print("Thanks for playing!")


if __name__ == "__main__":
    play_game()
