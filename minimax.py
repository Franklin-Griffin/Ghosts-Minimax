from random import sample

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

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
    best = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    for i in wordlist:
        if len(i) < len(best) and word in i:
            best = i
    return best

def minimax(current_string, alpha, beta, is_maximizing_player, wordlist, filtered_wordlist=None): # returns eval, (letter, position)
    if filtered_wordlist is None:
        filtered_wordlist = filter_wordlist(current_string, wordlist)
    # Longer games are better as the opponent has more chances to make a mistake
    if is_valid_word(current_string, filtered_wordlist) and len(current_string) > 2:
        return (1 - (len(current_string) * 0.01), "") if is_maximizing_player else (-1 + (len(current_string) * 0.01), "")
    # push AI to winning honorably and elongate the game by creating a word,
    # rather than giving up and playing "a" front
    if not filtered_wordlist:
        return (2 - (len(current_string) * 0.01), "") if is_maximizing_player else (-2 + (len(current_string) * 0.01), "") # no continuations possible

    if is_maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for letter in "".join(sample(ALPHABET, len(ALPHABET))):
            for position in ['start', 'end']:
                new_string = make_move(current_string, letter, position)
                new_filtered_wordlist = update_wordlist(new_string, filtered_wordlist)
                eval, _ = minimax(new_string, alpha, beta, False, wordlist, new_filtered_wordlist)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (letter, position)
                    if eval == 2: # best case scenario
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
        for letter in "".join(sample(ALPHABET, len(ALPHABET))):
            for position in ['start', 'end']:
                new_string = make_move(current_string, letter, position)
                new_filtered_wordlist = update_wordlist(new_string, filtered_wordlist)
                eval, _ = minimax(new_string, alpha, beta, True, wordlist, new_filtered_wordlist)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (letter, position)
                    if eval == -2: # best case scenario
                        return eval, best_move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return min_eval, best_move