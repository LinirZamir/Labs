from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    var = state.get_current_variable()
    value = None
    if var is not None:
        value = var.get_assigned_value()
        con_list = state.get_constraints_by_name(var.get_name())
        for con in con_list:
            Y = state.get_variable_by_name(con.get_variable_j_name())
            for y in Y.get_domain():
                if not con.check(state, value, y):
                    Y.reduce_domain(y)
                if Y.domain_size() == 0:
                    return False
    return True
                
# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    singleton_queue = list()
    visited_singleton = list()
    for singleton_var in state.get_all_variables():
        if singleton_var.domain_size() == 1:
            singleton_queue.append(singleton_var)
    while not (len(singleton_queue) == 0):
        cur_single = singleton_queue.pop()
        visited_singleton.append(cur_single)
        x_val = cur_single.get_domain()[0]
        for con in state.get_constraints_by_name(cur_single.get_name()):
            Y = state.get_variable_by_name(con.get_variable_j_name())
            for y_val in Y.get_domain():
                if not con.check(state, x_val, y_val):
                    Y.reduce_domain(y_val)
                if Y.domain_size() == 0:
                    return False
            if (Y not in singleton_queue) and (Y not in visited_singleton) and Y.domain_size()==1:
                singleton_queue.append(Y)
    return True

## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    dist = 0
    for i in range(len(list1)):
        dist += pow(list1[i]-list2[i],2)
    # this is not the right solution!
    return pow(dist,0.5)

#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance, 5)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    count_yes = float(len(yes))
    count_no = float(len(no))
    total = count_yes + count_no

    (yes_a,yes_b) = information_helper(yes)
    (no_a,no_b) = information_helper(no)
    if (yes_a/count_yes==0 or yes_b/count_yes==0):
        disorder_yes = 0
    else:
        disorder_yes = -((yes_a/count_yes)*math.log((yes_a/count_yes),2))-((yes_b/count_yes)*math.log((yes_b/count_yes),2))
    if (no_a/count_no==0 or no_b/count_no==0):
        disorder_no = 0
    else:
        disorder_no = -((no_a/count_no)*math.log((no_a/count_no),2))-((no_b/count_no)*math.log((no_b/count_no),2))
    
    total_disorder = disorder_yes*(count_yes/total)+disorder_no*(count_no/total)
    return total_disorder

def information_helper(lst):
    ## Check 'yes' list first
    count_a = 1
    count_b = 0
    for item in lst[1:]:
        if item==lst[0]: 
            count_a+= 1
        else: 
            count_b+=1
    return (float(count_a),float(count_b))
#print CongressIDTree(senate_people, senate_votes, information_disorder)
#evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 45
rep_classified = limited_house_classifier(house_people, house_votes, N_1)

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 71
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)


## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

    
