# This is a text-based Hangman game. The user can establish any number of
# players including AI of varying difficulty.

from random import choice
from time import sleep
from english_words import english_words_alpha_set as words

# This simply prepares the dictionary of words to be reasonably guessable by players.

words = list(words)
words = [i for i in words if i.isalpha]
words = [i for i in words if i[0].islower]

# The class below holds the attributes for players

class player():
    num_of_players = 0

    def __init__(self, name):
        self.name = name.upper()
        self.score = 0
        player.num_of_players += 1

    def guesser(self):
        return input(f'{self.name}, guess a letter or the whole word: ')

# The class below holds all AI player methods and attributes
        
class ai_player(player):

    num_of_ai = 0
    
    def __init__(self):
        self.score = 0
        player.num_of_players += 1
        self.name = f'AI_{ai_player.num_of_ai+1}'
        self.possible_words = words
        self.letter_frequency = [0 for i in range(26)]
        self.incorrect_guesses = []
        self.correct_guesses = []
        self.order = ''
        self.length = False
        self.difficulty = int(input('Enter the AI difficulty (1, 2, or 3): '))
        ai_player.num_of_ai += 1 

    def new_round(self):
        self.possible_words = words
        self.incorrect_guesses = []
        self.correct_guesses = []
        self.order = ''
        self.length = False

    def narrower2(self):
        
        if self.length == False:
            self.possible_words = [i for i in self.possible_words
                               if len(i) == len(self.order)]
            self.length = True
            
        if self.difficulty == 3:
            self.possible_words = [i for i in self.possible_words if \
                               all(map(lambda x: False if x in i.upper() else True,
                                       [y for y in self.incorrect_guesses]))]

        self.possible_words = [i for i in self.possible_words if \
                               all(x[0].upper() == x[1] or x[1] == '_' \
                                   for x in zip(i, self.order))]
        
    def guesser(self):
        if self.difficulty == 1:
            while 1:
                val = chr(choice(range(26)) + 65)
                if val not in self.incorrect_guesses and \
                   val not in self.correct_guesses:
                    return val
            
        else:
            self.narrower2()
            self.letter_frequency = [0 for i in range(26)]

            for word in self.possible_words:
                for letter in word:
                    self.letter_frequency[ord(letter.upper()) - 65] += 1

            for letter in range(26):
                if chr(letter + 65) in self.correct_guesses \
                   or chr(letter + 65) in self.incorrect_guesses:
                    self.letter_frequency[letter] = 0

            
            if len(self.possible_words) == 1:
                return self.possible_words[0]
 
            else:  
                return chr(self.letter_frequency.index(max(self.letter_frequency)) + 65)


# This is just a list of all players to be referenced for turn sequence

players = []

# This is the entry sequence

while 1:
    try:
        for i in range(int(input('How many players: '))):
            name = input('Enter your name (Enter \'AI\' for AI player: ')
            print(f'HI {name.upper()}!')
            players.append(ai_player()) if name.upper() == 'AI' \
                                    else players.append(player(name))
        break
    except:
        pass

# All of the game methods

class game():

    def __init__(self):
        self.body_parts = ['O', '|', '/', '\\', '|', '/', '\\']
        self.man = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

        self.hangman = ['  _____', '  |   | ', f'  {self.man[0]}   | ',
               f' {self.man[2]}{self.man[1]}{self.man[3]}  | ',
               f' {self.man[5]} {self.man[6]}  | ', f'      | ', f' ^^^^^^^']
        
        self.incorrect_guesses = []
        self.correct_guesses = []
        #self.word = input('\nEnter your secret word: ').upper()
        self.word = choice([i for i in list(words) if 8< len(i) < 14]).upper()
        self.word_guessed = False        
        
    
    #Visual Functions
    def print_board(self):
        for i in range(len(self.incorrect_guesses)):
            self.man[i] = self.body_parts[i]
        self.hangman = ['  _____', '  |   | ', f'  {self.man[0]}   | ',
               f' {self.man[2]}{self.man[1]}{self.man[3]}  | ',
                        f'  {self.man[4]}   | ',
                        f' {self.man[5]} {self.man[6]}  | ', 
                        f'      | ', f' ^^^^^^^']
        print('\n' * 30)
        for i in self.hangman:
            print(i)

    def print_word(self):
        final = []
        print('Word:')
        for letter in self.word:
            final.append(letter if letter in self.correct_guesses else '_')
        for player in players:
            if isinstance(player, ai_player):
                player.order = ''.join(final)
        print(' '.join(final))

    def print_incorrect_guesses(self):
        print('Letters guessed: ')
        print(' '.join(self.incorrect_guesses))


    def checker(self, turn):
        x =  players[turn].guesser().upper()
        if len(x) == 1:
            if x in self.word:
                self.correct_guesses.append(x)
                for player in players:
                    if isinstance(player, ai_player):
                        player.correct_guesses.append(x)
            else:
                self.incorrect_guesses.append(x)
                for player in players:
                    if isinstance(player, ai_player):
                        player.incorrect_guesses.append(x)
        else:
            if x == self.word:
                self.word_guessed = True

    def play(self):
        while 1:
            for i in range(player.num_of_players):
                turn = i
                self.print_board()
                self.print_word()
                self.print_incorrect_guesses()
                self.checker(turn)

                #Check win conditions

                if all(map(lambda x: True if x in self.correct_guesses
                           else False,[i for i in self.word])):
                    self.print_word()
                    return turn

                elif len(self.incorrect_guesses) > 6:
                    self.print_board()
                    print(f'\nThe word was {self.word}')
                    return 'n'

                elif self.word_guessed:
                    print(f'\n{self.word}')
                    return turn

                sleep(0.5)

# Below is the control flow

rounds = int(input('How many rounds would you like to play: '))

for x in range(rounds):
    newGame = game()
    try:
        players[newGame.play()].score += 1
    except:
        pass

    for i in players:
        sleep(1)
        print(f'\n{i.name}\'s SCORE: {i.score}')
    sleep(1)
    if x < rounds - 1:
        print('\n'*30, f'ROUND {x + 2}', '\n'*20)
    sleep(2)
    for i in players:
        if isinstance(i, ai_player):
            i.new_round()

maximum = 0

for i in range(len(players)):
    if players[i].score > maximum:
        maximum = players[i].score
        max_score = players[i]
        
if all(players[i].score == max_score for i in range(len(players))):
       max_score.name = "Nobody"

try:
    print(f'\n{max_score.name} wins!')
except:
    pass
    
                
                






    
                
    
    
    



















            
        
        
    


    
