import random

WIN_LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def create_board():
    return [" "] * 9

def print_board(board):
    for i in range(0, 9, 3):
        print(" | ".join(board[i:i+3]))
        if i < 6:
            print("--+---+--")

def check_winner(board, player):
    return any(all(board[i] == player for i in line) for line in WIN_LINES)

def check_tie(board):
    return " " not in board and not check_winner(board, "X") and not check_winner(board, "O")

def available_moves(board):
    return [i for i, c in enumerate(board) if c == " "]

class LearningAgent:
    def __init__(self, epsilon=0.2, alpha=0.5):
        self.q = {}              # (board state, move) -> value
        self.epsilon = epsilon   # chance of trying a random move
        self.alpha = alpha       # learning rate

    def get_q(self, state, move):
        return self.q.get((state, move), 0.0)

    def choose_move(self, board, explore=True):
        moves = available_moves(board)
        if explore and random.random() < self.epsilon:
            return random.choice(moves)
        state = tuple(board)
        best = max(self.get_q(state, m) for m in moves)
        return random.choice([m for m in moves if self.get_q(state, m) == best])

    def learn(self, history, reward):
        for state, move in reversed(history):
            old = self.get_q(state, move)
            self.q[(state, move)] = old + self.alpha * (reward - old)
            reward *= 0.9  # earlier moves get less credit

def play_training_game(agent):
    board = create_board()
    history = []
    player = "X"  # random opponent
    while True:
        if player == "X":
            board[random.choice(available_moves(board))] = "X"
        else:
            move = agent.choose_move(board)
            history.append((tuple(board), move))
            board[move] = "O"
        if check_winner(board, player):
            result = "win" if player == "O" else "loss"
            break
        if check_tie(board):
            result = "tie"
            break
        player = "O" if player == "X" else "X"
    agent.learn(history, {"win": 1, "tie": 0.5, "loss": -1}[result])
    return result

def train(agent, games=20000):
    wins = 0
    for g in range(1, games + 1):
        if play_training_game(agent) == "win":
            wins += 1
        if g % 5000 == 0:
            print(f"After {g} games, agent win rate: {wins / g:.0%}")

def get_human_move(board):
    while True:
        try:
            move = int(input("Your move (1-9): ")) - 1
            if move in available_moves(board):
                return move
        except ValueError:
            pass
        print("Invalid move, try again.")

def play_human_game(agent):
    board = create_board()
    player = "X"  # you are X, agent is O
    while True:
        print_board(board)
        if player == "X":
            move = get_human_move(board)
        else:
            move = agent.choose_move(board, explore=False)
            print(f"Agent plays {move + 1}")
        board[move] = player
        if check_winner(board, player):
            print_board(board)
            print("You win!" if player == "X" else "Agent wins!")
            return
        if check_tie(board):
            print_board(board)
            print("It's a tie!")
            return
        player = "O" if player == "X" else "X"

def main():
    agent = LearningAgent()
    print("Training the agent...")
    train(agent)
    while True:
        play_human_game(agent)
        if input("Play again? (yes/no): ").lower().strip() != "yes":
            break
    print("Thanks for playing!")

if __name__ == "__main__":
    main()