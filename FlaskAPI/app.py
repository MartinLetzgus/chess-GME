import flask
from flask import Flask, jsonify, request, render_template
import json
import pickle
import sklearn
import numpy as np
import chess
import chess.engine
import chess.pgn
import io
from openings_list import openings


app = Flask(__name__)

def load_models():
    file_name = "models/mlp_model.p"
    model = pickle.load(open(file_name, 'rb'))
    print(model)
    return model

def get_engine():
    return(chess.engine.SimpleEngine.popen_uci('stockfish/stockfish14.exe'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    pgn = request.args["pgn"]
    # parse input features from request
    #pgn = str(list(request.form.values())[0])
    pgn_io = io.StringIO(pgn)

    # get stockfish analysis of the game
    engine = get_engine()
    game = chess.pgn.read_game(pgn_io)
    moves = [move for move in game.mainline_moves()]
    board = game.board()
    analysis = []
    for move in moves:
            board.push(move)
            score = engine.analyse(board, chess.engine.Limit(depth=15))['score']
            if (score.white().score() != None):
                analysis.append(score.white().score())
            else:
                analysis.append(score.white().mate())

    # compute features and preprocess
    advantage_at_5 = analysis[4]
    advantage_at_10 = analysis[9]
    nb_moves = len(analysis)
    nb_checks = pgn.count('+',pgn.find('\n\n1'))

    result = []
    prev_score = analysis[0]
    for i,score in enumerate(analysis[1:]):
        if (i%2!=0):
            result.append(score-prev_score)
        else:
            result.append(prev_score-score)
        prev_score = score
    bins = np.array([-100000,-1000,-500,-200,-100,-50,-10,0,1000])
    hist = list(np.histogram(result,bins=bins)[0])
    hist_p = [np.round(item/(len(analysis)-1),4) for item in hist]

    move_quality_8,move_quality_7,move_quality_6,move_quality_5,move_quality_4,move_quality_3,move_quality_2,move_quality_1 = hist_p

    resignation = (pgn.find('resignation')!=-1)
    win_on_time = (pgn.find('on time')!=-1)
    stalemate = (pgn.find('stalemate')!=-1)
    abandon = (pgn.find('abandoned')!=-1)
    checkmate = (pgn.find('checkmate')!=-1)
    drawn_agreement = (pgn.find('drawn by agreement')!=-1)
    drawn_material = (pgn.find('insufficient material')!=-1)
    drawn_rep_or_50 = ((pgn.find('drawn by repetition')!=-1) or (pgn.find('50-move rule')!=-1))

    result = []
    for i,score in enumerate(analysis[1:]):
        result.append(abs(score))
    bins = np.array([0,100,200,400,10000])
    hist = list(np.histogram(result,bins=bins)[0])
    hist_p = [np.round(item/(len(analysis)-1),4) for item in hist]

    analysis1, analysis2, analysis3, analysis4 = hist_p

    opening_begining = pgn.find('ECO "')
    opening = pgn[opening_begining+5:opening_begining+8]
    openings_mask = [item==opening for item in openings]
    Other = (opening in openings)

    data = [advantage_at_5,advantage_at_10,nb_moves,nb_checks,move_quality_1,move_quality_2,move_quality_3,move_quality_4,move_quality_5,move_quality_6,move_quality_7,move_quality_8,resignation,win_on_time,stalemate,abandon,checkmate,drawn_agreement,drawn_material,drawn_rep_or_50,analysis1,analysis2,analysis3,analysis4]
    
    data = data + openings_mask + [Other]
    
    data = np.array(data).reshape(1,-1)

    
    # load model and predict
    model = load_models()
    prediction = model.predict(data)[0]
    #response = json.dumps({'elo': prediction})
    #return response, 200
    return render_template('index.html', prediction_text='Guessed elo : {}'.format(int(np.round(prediction))))


if __name__ == '__main__':
    application.run(debug=True)