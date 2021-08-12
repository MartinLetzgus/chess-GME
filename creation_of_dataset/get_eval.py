import pickle
import chess
import chess.pgn
import chess.engine
import numpy as np
import io
import time

start_time = time.time()

time_limit = 0.01
#Depth, the higher the better but the higher the slower
depth=10
#Here you need to dl the engine of your choice
engine = chess.engine.SimpleEngine.popen_uci('C:/Users/marti/Downloads/stockfish_14_win_x64_avx2/stockfish_14_win_x64_avx2/stockfish14.exe')

#Here the dataset obviously
games = pickle.load( open( "smol_dataset.p", "rb" ) )

evals = []

for i,game in enumerate(games):
    if(i%100==0):
        print(str(i)+'/'+str(len(games))+'     time : '+str((time.time() - start_time))+'s')
        pickle.dump(evals, open( "evals.p", "wb" ) )
    try:
        pgn = io.StringIO(game['pgn'])
        url = game['url']
        first_game = chess.pgn.read_game(pgn)
        moves = [move for move in first_game.mainline_moves()]
        board = first_game.board()
        anal = []
        for move in moves:
            board.push(move)
            score = engine.analyse(board, chess.engine.Limit(depth=depth))['score']
            if (score.white().score() != None):
                anal.append(score.white().score())
            else:
                anal.append(score.white().mate())
        evals.append([url,anal])
    except:
        print(game)
    
pickle.dump(evals, open( "evals.p", "wb" ) )
    
print("--- %s seconds ---" % (time.time() - start_time))
    
    
    
    
    
engine.quit()
