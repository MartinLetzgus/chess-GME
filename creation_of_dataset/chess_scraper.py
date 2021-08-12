from chessdotcom import get_leaderboards , get_player_stats , get_player_game_archives
import requests
import time
import pickle
import random

start_time = time.time()

month = "2021/07"


def get_most_recent_game(username, x=1):
    url = 'https://api.chess.com/pub/player/'+username+'/games/' + month
    games = requests.get(url).json()
    last_game_played = games['games'][-x]
    return(last_game_played)
    
def get_most_recent_games(username, nb_games=10):
    url = 'https://api.chess.com/pub/player/'+username+'/games/' + month
    games = requests.get(url).json()
    try:
        last_game_played = games['games'][-nb_games-1:-1]
    except:
        last_game_played = games['games']
    return(last_game_played)

def get_player_ratings(username):
    data = get_player_stats(username).json
    return(data['stats']['chess_blitz']['last']['rating'])
    
def check_elo_close(game, allowed_dif=100):
    return(abs(game['white']['rating']-game['black']['rating'])<=allowed_dif)
    
def check_rated(game):
    return(game['rated'])
    
def mean_elo(game):
    return((game['white']['rating']+game['black']['rating'])/2)
    
def get_players(game):
    return([game['white']['username'],game['black']['username']])
    
def get_ratings(game):
    return([game['white']['rating'],game['black']['rating']])
    
def check_time(game,time):
    return(game['time_control']==time)
    
def check_mode(game,mode):
    return(game['time_class']==mode)
    
games = pickle.load( open( "martinovichev.p", "rb" ) )    
explored = pickle.load( open( "explored.p", "rb" ) )  

mode = "blitz"
to_explore = ['martinovichev']
min_rating = 4000
max_rating = 0

new_games_wanted = 150

max_games = len(games)+new_games_wanted
        
while (len(games)<max_games):
    player = to_explore[0]
    recent_games = get_most_recent_games(player,4)
    for game in recent_games:
        if check_rated(game) and check_elo_close(game):
            if check_mode(game, mode):
                games.append(game)
                if (len(games)%10==0):
                    print(len(games))
                    pickle.dump(games, open( "martinovichev.p", "wb" ) )
                players = get_players(game)
                if (players[0] not in explored) and (players[0] not in to_explore):
                    to_explore.append(players[0])
                if (players[1] not in explored) and (players[1] not in to_explore):
                    to_explore.append(players[1])
    explored.append(player)
    to_explore.remove(player)
    
pickle.dump(games, open( "martinovichev.p", "wb" ) )
pickle.dump(explored, open( "explored.p", "wb" ) )
    
print('games in file : '+str(len(games)))
print('players explored : '+str(len(explored)))
print('Players to explore next :')
for i in range (50):
    player = random.choice(to_explore)
    print(player, get_player_ratings(player))

print("--- %s seconds ---" % (time.time() - start_time))