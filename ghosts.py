DEPTH = 5

def load_wordlist(filename="wordlist.txt"):
    with open(filename) as f:
        return [word.strip() for word in f.readlines()]

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

def minimax(current_string, depth, alpha, beta, is_maximizing_player, wordlist): # returns eval, (letter, position)
    if depth == 0:
        return 0, "" # never occurs when move is needed (iteration 1)
    if is_valid_word(current_string, wordlist):
        return (1, "") if is_maximizing_player else (-1, "")
    if not leads_to_word(current_string, wordlist):
        return (1, "") if is_maximizing_player else (-1, "")

    if is_maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            for position in ['start', 'end']:
                new_string = make_move(current_string, letter, position)
                eval, _ = minimax(new_string, depth - 1, alpha, beta, False, wordlist)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (letter, position)
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
                eval, _ = minimax(new_string, depth - 1, alpha, beta, True, wordlist)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (letter, position)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return min_eval, best_move

def make_move(current_string, letter, position):
    return current_string + letter if position == 'end' else letter + current_string

def play_game(wordlist):
    player_first = input("Do you want to go first? (yes/no): ").strip().lower().startswith('y')
    current_string = "pe" if not player_first else input("Enter the initial 2 letters: ")
    if not player_first:
        print("AI chose the initial string \"pe\"")

    player_turn = not player_first

    while True:
        if not player_turn and not leads_to_word(current_string, wordlist):
            print("Challenge from AI: no words can be created from this string. AI wins!")
            return
        
        if is_valid_word(current_string, wordlist):
            if player_turn:
                print("AI created a word. Player wins!")
            else:
                print("Player created a word. AI wins!")
            return

        if player_turn:
            move = input("Your move (format: letter [start/end] OR challenge): ")
            if move == "challenge":
                if not leads_to_word(current_string, wordlist):
                    print("Challenge successful: no words can be created from this string. Player wins!")
                else:
                    print(f"Challenge failed: {word_continuation(current_string, wordlist)} can be created. AI wins!")
                return
            letter, position = move.split()
            current_string = make_move(current_string, letter, position)
        else:
            _, move = minimax(current_string, DEPTH, float('-inf'), float('inf'), True, wordlist)
            letter, position = move
            current_string = make_move(current_string, letter, position)
            print(f"AI adds '{letter}' at the {position}: {current_string}")
        
        player_turn = not player_turn

wordlist = load_wordlist()
while True:
    play_game(wordlist)
    if input("Play again? (yes/no): ").strip().lower().startswith('n'):
        break
