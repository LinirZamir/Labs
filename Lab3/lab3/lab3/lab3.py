# 6.034 Fall 2010 Lab 3: Games
# Name: <Your Name>
# Email: <Your Email>

from pyexpat import XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE
from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
## run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    if board.is_game_over():
        score = -1000
    else:
        ## Starting focused eval
        for move, next_board in get_all_next_moves(board):
            if next_board.longest_chain(next_board.get_other_player_id()) == 4:
                score = 1000
                break
            elif next_board.longest_chain(next_board.get_current_player_id()) == 4: 
                score = -1000
                break

        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.          
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score

## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.


def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):
    alpha_beta = [NEG_INFINITY, INFINITY]
    best_val = None

    for move, new_board in get_next_moves_fn(board):
        if alpha_beta[0] >= alpha_beta[1]:
            break
        new_val = -1* ab_find_board_value(new_board, depth-1, alpha_beta, eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn)

        if best_val == None or new_val > alpha_beta[0] :
            alpha_beta[0] = new_val  
            best_val = (new_val, move, new_board)
                    
    ## print "ALPHA-BETA: Decided on column %d with rating %d" % (best_val[1], best_val[0])

    return best_val[1]

def ab_find_board_value(board, depth, ab_val, eval_fn,
                             get_next_moves_fn=get_all_next_moves,
                             is_terminal_fn=is_terminal):
    """
    Minimax helper function: Return the minimax value of a particular board,
    given a particular depth to estimate to
    """
    if is_terminal_fn(depth, board):
        return eval_fn(board)

    ab_val = [-1* ab_val[1],-1* ab_val[0]]

    for move, new_board in get_next_moves_fn(board):
        if ab_val[0] >= ab_val[1]:
            break
        new_val = -1* ab_find_board_value(new_board, depth-1, ab_val, eval_fn,
                                                get_next_moves_fn, is_terminal_fn)

        if new_val > ab_val[0] :
            ab_val[0] = new_val    


    return ab_val[0]


## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)


## You can try out your new evaluation function by uncommenting this line:
#run_game(quick_to_win_player, alphabeta_player)


## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
## run_game(human_player, ab_iterative_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

def better_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    score = 0
    trap_count = 0
    if board.is_game_over():
        score = -1000
    else:
        for move, next_board in get_all_next_moves(board):
            if next_board.longest_chain(next_board.get_other_player_id()) == 4:
                score = 2000
                break
            elif next_board.longest_chain(next_board.get_current_player_id()) == 4: 
                score = -2000
                break
        ## prioritizing mid columns
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)
                if check_figure_seven(board,row,col,board.get_current_player_id()):
                    score+=pow(4,2)
                elif check_figure_seven(board,row,col,board.get_other_player_id()):
                    score-=pow(4,2)
                if check_trap(board,row,col,board.get_current_player_id()):
                    score+=pow(4,2)
                elif check_trap(board,row,col,board.get_other_player_id()):
                    score-=pow(4,2)
        ## prioritizing getting longer chains + blocking adversary short chains
        my_big_chains = filter(lambda x: len(x) > 1, board.chain_cells(board.get_current_player_id()))
        ##my_next_big_chains = list(board.chain_cells(board.get_current_player_id()))
        for x in my_big_chains: 
            score+=pow(len(x),2)        
        their_big_chains = filter(lambda x: len(x) > 1, board.chain_cells(board.get_other_player_id()))
        ##their_next_big_chains = list(board.chain_cells(board.get_other_player_id()))
        for y in their_big_chains: 
            score-=pow(len(y),2)
    return score

"""
        if len(x)==2:
                for move, next_board in get_all_next_moves(board):
                    my_next_big_chains = filter(lambda x: len(x)==3, next_board.chain_cells(board.get_current_player_id()))
                    if (all(x in my_next_big_chains for x in my_big_chains)):
                        trap_count+=1
                    else:
                        score+=pow(len(x),1.5)
                if(trap_count>1):
                    score+=pow(len(x),2) 
                    trap_count=0
                else:
                    score+=pow(len(x),1.5)
            else:
                score+=pow(len(x),1.5)        
  
        for move, next_board in get_all_next_moves(board):
            if next_board.longest_chain(next_board.get_other_player_id()) == 4:
                score = 1000
                break
            elif next_board.longest_chain(next_board.get_current_player_id()) == 4: 
                score = -1000
                break
            else:
                my_next_big_chains = filter(lambda x: len(x) > 1, next_board.chain_cells(board.get_current_player_id()))
                my_current_big_chains = filter(lambda x: len(x) > 1, board.chain_cells(board.get_current_player_id()))
                my_new=list(set(my_next_big_chains)-set(my_current_big_chains))
                for x in my_new: 
                    score+=pow(len(x),3)
                their_next_big_chains = filter(lambda x: len(x) > 1, next_board.chain_cells(board.get_other_player_id()))
                their_current_big_chains = filter(lambda x: len(x) > 1, board.chain_cells(board.get_other_player_id()))
                their_new=list(set(their_next_big_chains)-set(their_current_big_chains))
                for x in their_new: 
                    score-=pow(len(x),3)
            for row in range(6):
                for col in range(7):
                    if board.get_cell(row, col) == board.get_current_player_id():
                        score -= abs(3-col)
                    elif board.get_cell(row, col) == board.get_other_player_id():
                        score += abs(3-col)

"""
def check_figure_seven(board,row,col,player):
    try:
        if (col!=6 and \
            board.get_cell(row,col) == player and \
            board.get_cell(row-1,col+1) == player and \
            board.get_cell(row-2,col+2) == player and \
            board.get_cell(row-2,col+1) == player and \
            board.get_cell(row-2,col) == player) or \
            (col!=0 and \
            board.get_cell(row,col) == player and \
            board.get_cell(row-1,col-1) == player and \
            board.get_cell(row-2,col-2) == player and \
            board.get_cell(row-2,col-1) == player and \
            board.get_cell(row-2,col) == player):
                return True
    except IndexError:
        return False
    return False
        
def check_trap(board,row,col,player):
    ##Horizon 1
    try:
        if ((row<5 and \
        board.get_cell(row,col) == 0 and \
        board.get_cell(row,col+1) == player and \
        board.get_cell(row,col+2) == player and \
        board.get_cell(row,col+3) == player and \
        board.get_cell(row,col+4) == 0 and\
        board.get_cell(row+1,col) != 0 and\
        board.get_cell(row+1,col+4) != 0)  or \
    ##Horizon 2
        (row==5 and \
        board.get_cell(row,col) == 0 and \
        board.get_cell(row,col+1) == player and \
        board.get_cell(row,col+2) == player and \
        board.get_cell(row,col+3) == player and \
        board.get_cell(row,col+4) == 0)  or\
    ## Diagonal 1
        (board.get_cell(row,col) == 0 and \
        board.get_cell(row-1,col+1) == player and \
        board.get_cell(row-2,col+2) == player and \
        board.get_cell(row-3,col+3) == player and \
        board.get_cell(row-4,col+4) == 0 and\
        board.get_cell(row+1,col) != 0 and\
        board.get_cell(row-3,col+4) != 0)  or \
    ## Diagonal 2
        (board.get_cell(row,col) == 0 and \
        board.get_cell(row-1,col-1) == player and \
        board.get_cell(row-2,col-2) == player and \
        board.get_cell(row-3,col-3) == player and \
        board.get_cell(row-4,col-4) == 0 and\
        board.get_cell(row+1,col) != 0 and\
        board.get_cell(row-3,col-4) != 0)):
            return True
    except IndexError:
        return False
    return False


# Comment this line after you've fully implemented better_evaluate
# better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
#better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if True:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,1,1,1,0,2,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))




"""
This evaluator is from another online student. 
MY EVALUATOR WAS SUPERIOR! 

def other_evaluate(board):
    score = 0
    
    if board.longest_chain(board.get_current_player_id()) == 4:
        score = 2000 - board.num_tokens_on_board()
        
    elif board.longest_chain(board.get_other_player_id()) == 4:
        score = -2000 + board.num_tokens_on_board()
        
    else:
        cur_play = board.get_current_player_id()
        other_play = board.get_other_player_id()
        for row in range(2,6):
            for col in range(2,5):
                score += max([get_chain_len(i, board, row, col, cur_play) for i in range(3)])**2
                score -= max([get_chain_len(i, board, row, col, other_play) for i in range(3)])**2
                
    return score

def get_chain_len(chain_type, board, row, col, player):
    count = 0
    for i in xrange(3):
        
        if chain_type == 0 and board.get_cell(row, col+i) == player:
            count += 1
            
        elif chain_type == 1 and board.get_cell(row-i, col) == player:
            count += 1
            
        elif chain_type == 2 and board.get_cell(row-i, col+i) == player:
            count += 1
            
    return count

"""



## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)
## his_player = lambda board: run_search_function(board,search_fn=alpha_beta_search,eval_fn=other_evaluate,timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
## run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (True)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "Too long"
WHAT_I_FOUND_INTERESTING = "Everything"
WHAT_I_FOUND_BORING = "Nothing"
NAME = "Ben"
EMAIL = "asad"

