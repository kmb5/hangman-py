"""Main Hangman game class and its methods"""

from pickle import dump
from os.path import exists
from random import choice
from hangman_turns_representation import HANGMANPICS

class Hangman():
    """Main Hangman game class"""

    def __init__(self, dictionary_path: str):
        self.dictionary_path = dictionary_path
        self.num_turns = len(HANGMANPICS)
        self.current_turn = 0
        self.guessed_letters = []
        self.game_over = False
        self.word_to_guess = self._pick_word()
        self.allowed_letters = self._get_allowed_letters()

    def play_turn(self):
        """
        Play a turn of Hangman
        """
        
        print('\nOptions:')
        print('- You can save your game any time by typing "save" instead of a letter.')
        print('- You can quit any time by typing "quit" instead of a letter.\n')


        obfuscated_word = self._get_obfuscated_word()
        print('\n' + obfuscated_word)


        already_guessed_incorrect = sorted([l for l in self.guessed_letters if l not in self.word_to_guess])
        if len(already_guessed_incorrect) > 0:
            print(f'\nMisses: {(", ").join(already_guessed_incorrect)}')
        print('\n' + HANGMANPICS[self.current_turn] + '\n')

        # Handle game over states
        if '_' not in obfuscated_word:
            print('You won!')
            self.game_over = True
            return

        if self.current_turn == self.num_turns - 1:
            print('You lost!')
            self.game_over = True
            return

        # Handle guess
        guess = ''
        while True:
            guess = input('Input a letter >>> ').lower()
            if guess == 'save':
                self._save_game()
                continue
            elif guess == 'quit':
                really = input('Really quit? y/n >>> ').lower()
                if really == 'y':
                    print('Thanks for playing!')
                    self.game_over = True
                    return

            validation = self._validate_guess(guess)
            if validation['validation_passed']:
                break
            print(validation['error_msg'])

        print(f'You guessed {guess}.')

        if guess not in self.word_to_guess:
            # Only increment the turn if the user guessed a
            # letter which is not in the word
            self.current_turn += 1

        self.guessed_letters.append(validation['guessed_letter'])
    
    def _save_game(self):
        """
        Save the game as a python pickle file
        """

        # Allowed characters in the name of the file
        allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789_'

        stop_loop = False
        while not stop_loop:
            file_name = input('\nPick a file name (only English letters, numbers and underscores are allowed) >>> ')
            for char in file_name:
                if char not in allowed_chars:
                    print('Invalid file name!')
                    stop_loop = False
                    break
                stop_loop = True

            file_path = './saved_games/' + file_name + '.pickle'
            if exists(file_path):
                print(f'There is already a saved game with the same name ({file_name})!')
                overwrite = input('Do you want to overwrite? (y/n) >>> ').lower()
                if overwrite != 'y':
                    stop_loop = False

        with open(file_path, 'wb') as f:
            # Dump the current instance of the object
            dump(self, f)

        print('\nGame saved successfully.\n')

    def _get_obfuscated_word(self) -> str:
        """
        Get the word to guess but replace all characters
        that haven't been guessed yet with a _ and leave
        a space between each letter
        """

        obfuscated_word = [letter if letter in self.guessed_letters else '_' for letter in self.word_to_guess]
        return (' ').join(obfuscated_word)

    def _validate_guess(self, guess: str) -> dict:
        """
        To make sure the input given by the user is a valid guess

        Parameters
        ----------
        guess : str
            The guess as inputted by the user

        Returns
        -------
        validation_dict : dict
            The result of the validation.
            If it succeeds, guessed_letter will be the letter guessed,
            and validation_passed will be True.
            If it fails, validation_passed will be false, and the error details
            are stored in error_msg as a string

        """

        guess = guess.lower()

        validation_dict = {
            'validation_passed': False,
            'guessed_letter': '',
            'error_msg': ''
        }

        if guess not in self.allowed_letters:
            validation_dict['error_msg'] = f'Wrong input, has to be one of: {(", ").join(self.allowed_letters)}\n(or maybe you wanted to type "quit" or "save"?)\n'
            return validation_dict
        if guess in self.guessed_letters:
            validation_dict['error_msg'] = f'You already guessed the letter "{guess}". Pick another.\n'
            return validation_dict

        validation_dict['guessed_letter'] = guess
        validation_dict['validation_passed'] = True

        return validation_dict


    def _get_allowed_letters(self) -> list:
        """
        Gets all unique letters from the given dictionary
        to find out which letters are allowed and which aren't
        (this is because if a foreign-language dictionary is set,
        the letters can be á, é, ö, etc.)

        Returns
        -------
        allowed_letters : list
            A list of all unique letters in the given dictionary
            (sorted alphabetically)

        """

        dictionary = self._load_dictionary()
        allowed_letters = []
        for word in dictionary:
            for letter in word:
                if letter not in allowed_letters:
                    allowed_letters.append(letter)

        return sorted(allowed_letters)
    
    def _pick_word(self) -> str:
        """
        Loads in the dictionary and
        picks a random word from it

        Returns
        -------
        word : str
            The randomly choosen word
        """
        dictionary = self._load_dictionary()
        word = choice(dictionary)

        return word


    def _load_dictionary(self) -> list:
        """
        Load a .txt file from self.dictionary_path, which is
        a list of words, each word on a new line
        It filters out words which are not between 5-12 chars long,
        lowercases all words and gets rid of the duplicates.

        Returns
        -------
        dictionary : list
            A list of words from the dictionary file given in __init__
        
        """
        with open(self.dictionary_path, 'r') as f:
            words = f.readlines()
        # get rid of \n
        words_without_newline_char = [
            word.replace('\n', '') for word in words]
        # lowercase & keep only words between 5-12 chars long
        dictionary = [
            word.lower() for word in words_without_newline_char
            if len(word) in range(5, 13)]
        # remove duplicates
        dictionary = list(set(dictionary))
        
        return dictionary
