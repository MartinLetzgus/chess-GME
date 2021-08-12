import chess
import chess.pgn
import chess.engine

def stockfish_evaluation(board, color='white', time_limit = 0.01):
    engine = chess.engine.SimpleEngine.popen_uci('C:/Users/marti/Downloads/stockfish_14_win_x64_avx2/stockfish_14_win_x64_avx2/stockfish14.exe')
    info = engine.analyse(board, chess.engine.Limit(time=time_limit))
    if color == 'white':
        score = info['score'].white().score()
    else:
        score = info['score'].black().score()
    engine.quit()
    return score

pgn = open('test.pgn')
first_game = chess.pgn.read_game(pgn)

# Move 48
board = first_game.board()
moves = [move for move in first_game.mainline_moves()]

# Iterate through all moves and play them on a board
result = []
for move in moves[0:10]:
    board.push(move)
    result.append(stockfish_evaluation(board))
print(result)