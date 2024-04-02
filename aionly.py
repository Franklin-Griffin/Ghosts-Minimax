from json import load
from random import choice, random

def load_wordlist(filename="wordlist.txt"):
    with open(filename) as f:
        return [word.strip().lower() for word in f.readlines()]

def is_valid_word(word, wordlist): # binary search
    lo, hi = 0, len(wordlist) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_word = wordlist[mid]
        if mid_word == word:
            return True
        elif mid_word < word:
            lo = mid + 1
        else:
            hi = mid - 1
    return False

def filter_wordlist(current_string, wordlist):
    return [word for word in wordlist if current_string in word]

def make_move(current_string, letter, position):
    return current_string + letter if position == 'end' else letter + current_string

def update_wordlist(current_string, filtered_wordlist):
    return [word for word in filtered_wordlist if current_string in word]

def leads_to_word(word, wordlist):
    for i in wordlist:
        if word in i:
            return True
    return False

def word_continuation(word, wordlist):
    for i in wordlist:
        if word in i:
            return i
    return False

def minimax(current_string, alpha, beta, is_maximizing_player, wordlist, filtered_wordlist=None): # returns eval, (letter, position)
    if filtered_wordlist is None:
        filtered_wordlist = filter_wordlist(current_string, wordlist)
    if is_valid_word(current_string, wordlist) and len(current_string) > 2:
        return (1, "") if is_maximizing_player else (-1, "")
    if not filtered_wordlist: # no continuations possible
        return (1, "") if is_maximizing_player else (-1, "")

    if is_maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            for position in ['start', 'end']:
                new_string = make_move(current_string, letter, position)
                new_filtered_wordlist = update_wordlist(new_string, filtered_wordlist)
                eval, _ = minimax(new_string, alpha, beta, False, wordlist, new_filtered_wordlist)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (letter, position)
                    if eval == 1: # best case scenario
                        return eval, best_move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            for position in ['start', 'end']:
                new_string = make_move(current_string, letter, position)
                new_filtered_wordlist = update_wordlist(new_string, filtered_wordlist)
                eval, _ = minimax(new_string, alpha, beta, True, wordlist, new_filtered_wordlist)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (letter, position)
                    if eval == -1: # best case scenario
                        return eval, best_move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return min_eval, best_move

def play_game(wordlist):
    A_turn = random() >= 0.5 # rand float

    with open("./comboutility.json", "r") as f:
        comboutility = load(f)
    current_string = choice(comboutility["winning"])

    if A_turn:
        print(f"AI A chose the initial string \"{current_string}\"")
    else:
        print(f"AI B chose the initial string \"{current_string}\"")

    A_turn = not A_turn

    while True:
        if A_turn and not leads_to_word(current_string, wordlist):
            print("Challenge from AI A: no words can be created from this string. AI A wins!")
            return
        if not A_turn and not leads_to_word(current_string, wordlist):
            print("Challenge from AI B: no words can be created from this string. AI B wins!")
            return
        
        if is_valid_word(current_string, wordlist) and len(current_string) > 2:
            if A_turn:
                print("AI B created a word. AI A wins!")
            else:
                print("AI A created a word. AI B wins!")
            return
        
        _, move = minimax(current_string, float('-inf'), float('inf'), A_turn, wordlist)
        letter, position = move
        current_string = make_move(current_string, letter, position)
        if A_turn:
            print(f"AI A adds '{letter}' at the {position}: {current_string}")
        else:
            print(f"AI B adds '{letter}' at the {position}: {current_string}")

        A_turn = not A_turn

wordlist = load_wordlist()
while True:
    play_game(wordlist)
    print()