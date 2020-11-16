"""Main module for the Hangman game"""

from pickle import load
from os import listdir
from hangman_class import Hangman

def main():
    """Main function to play Hangman"""

    print('\n\nH A N G M A N\n\n')
    print('Welcome! What do you want to do?')
    print('1: New game\n2: Load saved game\n')

    choice = ''
    while choice not in ('1', '2'):
        choice = input('Input your choice (1 or 2) >>> ')

    if choice == '1':
        hangman = Hangman('words.txt')
    elif choice == '2':
        hangman = load_game()
        if not hangman:
            # If there are no games saved, exit
            return

    while not hangman.game_over:
        hangman.play_turn()

def load_game():
    """
    Load a game of Hangman.

    Returns
    -------
    game_object : object
        The loaded game object with the saved states
    
    Returns None if there are no games saved.
    """

    saved_games = listdir('./saved_games')

    if len(saved_games) == 0:
        print('There are no games saved.')
        return None

    saved_games_repr = ('\n'.join([f'{i + 1} - {s.replace(".pickle", "")}' for i, s in enumerate(saved_games)]))
    print(f'\nSave games available: \n{saved_games_repr}')

    to_load = ''
    while to_load not in [str(n) for n in range(1, len(saved_games) + 1)]:
        to_load = input(f'\nPick a number to load from 1 - {len(saved_games)} >>> ')

    filename_to_load = saved_games[int(to_load) - 1]
    filepath_to_load = './saved_games/' + filename_to_load

    with open(filepath_to_load, 'rb') as f:
        game_object = load(f)
        
    return game_object

if __name__ == "__main__":
    main()