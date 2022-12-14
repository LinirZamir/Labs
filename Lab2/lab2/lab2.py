# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    queue = []
    extended_list = []
    queue.append([start])
    extended_list.append(start)
    while not (queue[0][-1]==goal) and queue:
        head_node = queue[0]
        connected_nodes = graph.get_connected_nodes(head_node[-1])
        queue.pop(0)
        for x in connected_nodes:
            if not x in extended_list:
                tmp_list = [i for i in head_node]
                tmp_list.append(x)
                queue.append(tmp_list)
        extended_list.append(queue[0][-1])
    return queue[0]


## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    queue = []
    extended_list = []
    queue.append([start])
    extended_list.append(start)
    while not (queue[0][-1]==goal) and queue:
        head_node = queue[0]
        connected_nodes = graph.get_connected_nodes(head_node[-1])
        queue.pop(0)
        for x in connected_nodes:
            if not x in extended_list:
                tmp_list = [i for i in head_node]
                tmp_list.append(x)
                queue.insert(0,tmp_list)
        extended_list.append(queue[0][-1])
    return queue[0]




## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    queue = []
    extended_list = []
    queue.append([start])
    extended_list.append(start)
    while not (queue[0][-1]==goal) and queue:
        heurist_list=[]
        head_node = queue[0]
        connected_nodes = graph.get_connected_nodes(head_node[-1])
        queue.pop(0)
        for x in connected_nodes:
            if not x in head_node:
                heurist_list.append(x)
        heurist_list.sort(reverse = True, key=lambda a : graph.get_heuristic(a,goal))
        for x in heurist_list:
            if not x in extended_list:
                tmp_list = [i for i in head_node]
                tmp_list.append(x)
                queue.insert(0,tmp_list)
        extended_list.append(queue[0][-1])
    return queue[0]

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    queue = []
    extended_list = []
    queue.append([start])
    extended_list.append(start)
    while not (queue[0][-1]==goal) and queue:
        heurist_list=[]
        head_node = queue[0]
        connected_nodes = graph.get_connected_nodes(head_node[-1])
        queue.pop(0)
        for x in connected_nodes:
            if not x in extended_list:
                tmp_list = [i for i in head_node]
                tmp_list.append(x)
                queue.append(tmp_list)
        try: 
            if(len(queue[0])==len(queue[-1])):
                queue.sort(reverse = False, key=lambda a : graph.get_heuristic(a[-1],goal))
                del queue[beam_width:]
        except:
            return []
        extended_list.append(queue[0][-1])
    return queue[0]

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    sum_length = 0
    prev = node_names[0]
    for x in node_names[1:]:
        edge_val = graph.get_edge(prev,x)
        sum_length = sum_length + edge_val.length
        prev = x
    return sum_length


"""
### WITHOUT EXTENDED LIST - NUMBER OF OPERATIONS IS EXPONENTIALLY LARGE
def branch_and_bound(graph, start, goal):
    queue = []
    oper_queue = 0
    oper_enqueue = 0
    extended_list = []
    queue.append([start])
    oper_queue = oper_queue + 1
    extended_list.append(start)
    while not (queue[0][-1]==goal) and queue:
        head_node = queue[0]
        connected_nodes = graph.get_connected_nodes(head_node[-1])
        oper_enqueue = oper_enqueue + 1
        queue.pop(0)
        for x in connected_nodes:
            if not x in head_node:
                tmp_list = [i for i in head_node]
                tmp_list.append(x)
                queue.insert(0,tmp_list)
                oper_queue = oper_queue + 1
                queue.sort(reverse = False, key=lambda a : path_length(graph,a))
        extended_list.append(queue[0][-1])
    print("Numbber of queueue operations: ", oper_queue)
    print("Numbber of enqueueue operations: ", oper_enqueue)
    return queue[0]
"""

def branch_and_bound(graph, start, goal):
    queue = []
    oper_queue = 0
    oper_enqueue = 0
    extended_list = []
    queue.append([start])
    oper_queue = oper_queue + 1
    extended_list.append(start)
    while not (queue[0][-1]==goal) and queue:
        head_node = queue[0]
        connected_nodes = graph.get_connected_nodes(head_node[-1])
        oper_enqueue = oper_enqueue + 1
        queue.pop(0)
        for x in connected_nodes:
            if not x in extended_list:
                tmp_list = [i for i in head_node]
                tmp_list.append(x)
                queue.insert(0,tmp_list)
                oper_queue = oper_queue + 1
                queue.sort(reverse = False, key=lambda a : path_length(graph,a))
        extended_list.append(queue[0][-1])
    return queue[0]

def a_star(graph, start, goal):
    queue = []
    extended_list = []
    queue.append([start])
    extended_list.append(start)
    while not (queue[0][-1]==goal) and queue:
        head_node = queue[0]
        connected_nodes = graph.get_connected_nodes(head_node[-1])
        queue.pop(0)
        for x in connected_nodes:
            if not x in extended_list:
                tmp_list = [i for i in head_node]
                tmp_list.append(x)
                queue.insert(0,tmp_list)
                ## add admissible heuristic 
                queue.sort(reverse = False, key=lambda a : path_length(graph,a)+graph.get_heuristic(a[-1],goal))
        extended_list.append(queue[0][-1])
    return queue[0]

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    for x in graph.nodes:
        D = path_length(graph, a_star(graph,x,goal))
        H = graph.get_heuristic(x,goal)
        if D<H: return False
    return True

def is_consistent(graph, goal):
    for x in graph.nodes:
        for y in graph.nodes:
            if x!=y:
                D = path_length(graph, a_star(graph,y,x))
                H1 = graph.get_heuristic(x,goal)
                H2 = graph.get_heuristic(y,goal)
                if D<abs(H1-H2): return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '50'
WHAT_I_FOUND_INTERESTING = 'all'
WHAT_I_FOUND_BORING = 'none'
