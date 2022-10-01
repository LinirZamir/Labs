listqueue = [(1,2),(1,2,3),(1,4,5,6)]
list2 = [(1,2,3),(1,2,3),(1,5,6)]
print(list(set(listqueue) - set(list2)))