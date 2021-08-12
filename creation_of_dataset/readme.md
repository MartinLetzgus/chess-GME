## Creation of dataset

**chess_scraper.py** allows to add more games to a pickle file based on a player to explore
**distrib.py** shows the actual distribution of elo in the dataset (to help reach the wanted distribution)
**get_eval.py** computes the stockfish evaluation of every game

**explored.p** is as pickle file keeping track of the players already explored

## Clean dataset

Jupyter notebook : **clean_dataset.py**

Join the computed evaluation of the game to the dataset as a new column, drop na and duplicates, delete games with under 10 moves and save the resulting dataset as a csv file.