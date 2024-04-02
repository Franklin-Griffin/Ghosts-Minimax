from json import dump

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
    if is_valid_word(current_string, filtered_wordlist) and len(current_string) > 2:
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

wordlist = load_wordlist()
winning_combinations = []
losing_combinations = []

for letter1 in 'abcdefghijklmnopqrstuvwxyz':
    for letter2 in 'abcdefghijklmnopqrstuvwxyz':
        util = minimax(letter1 + letter2, float('-inf'), float('inf'), True, wordlist)[0]
        if util == 1:
            print(letter1 + letter2 + " is a winning starting combination")
            winning_combinations.append(letter1 + letter2)
        else:
            print(letter1 + letter2 + " is a losing starting combination")
            losing_combinations.append(letter1 + letter2)

txt_content = """If both players play perfectly...
Winning:
""" + '\n'.join(winning_combinations) + """

Losing:
""" + '\n'.join(losing_combinations)

json_content = {
    "winning": winning_combinations,
    "losing": losing_combinations
}

with open("./comboutility.txt", "w") as txt_file:
    txt_file.write(txt_content)

with open("./comboutility.json", "w") as json_file:
    dump(json_content, json_file)