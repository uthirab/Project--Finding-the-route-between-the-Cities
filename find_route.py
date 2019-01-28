import sys
from itertools import repeat
#gets input from the user during compiling
arg1=sys.argv[1]
arg2=sys.argv[2]
arg3=sys.argv[3]
arg4=sys.argv[4]
#if its a informed search input file for heuristic is taken 
if arg1=='inf':
	file_2= sys.argv[5]
else:
	file_2= ''
#initializing variables
from_city, to_city, distance, from_city_h, distance_h = [], [], [], [], []
fringe, fringed, visitednode = [], [], []
fringedic, parentdistancedic = {}, {}
distance1, route = list(), list()
parentchilddic = {}
f = arg3
t = arg4
d = 0
global dis_h
dis_h=0
input_file = open(arg2, 'r')

#storing the tree in form of array
for i in input_file:
    linestriped = i.rstrip()
    splitedline = linestriped.split(" ")
    if splitedline[0] == '' or splitedline[0] == 'END':
        break
    from_city.append(splitedline[0])
    to_city.append(splitedline[1])
    distance.append(splitedline[2])

if file_2:
    input_file1 = open(file_2, 'r')
    for i in input_file1:
        linestriped = i.rstrip()
        splitedline = linestriped.split(" ")
        if splitedline[0] == '' or splitedline[0] == 'END':
            break
        from_city_h.append(splitedline[0])
        distance_h.append(splitedline[1])
else:
    distance_h = list(repeat(0,len(from_city)))

#function that retrieves the heuristic value
def heuristicdis(f):
    if len(from_city_h) >1:
        for i in range(0,len(from_city_h)):
            if from_city_h[i]==f:
                dish=distance_h[i]
		return dish
    else:
        return 0

#Prints the route 
def routeprint():
    print 'distance: ' + str(total_distance) + 'Km'
    if route > 1:
        for i in range(len(route) - 2):
            first = route.pop()
            fdis = distance1.pop()
            second = route.pop()
            print str(first) + ' to ' + str(second) + ', ' + str(fdis) + 'Km'
            if not route:
                break
    else:
        print 'route:'

#backtracks the route
def backtrack(t, f):
    while t != f:
        if t not in parentchilddic:
            print('Distance : Infinty')
            break
        temp = parentchilddic[t]

        for i in range(len(from_city)):
            if from_city[i] == t:
                if to_city[i] == temp:
                    distance1.append(int(distance[i]))
            elif to_city[i] == t:
                if from_city[i] == temp:
                    distance1.append(int(distance[i]))
        route.append(t)
        route.append(temp)
        t = temp

#checks if the goal state is reached and if not gives the next node to expand 
def check(fringedics, t, d):
    if len(fringedics) < 1 or t == fringedics[0][0]:

        return 0
    else:
        f1 = fringedics[0][0]
        d = fringedics[0][1]
        del fringedic[f1]
        fringeaddition(f1, t, d)

#Calculates the distance from the parent node 
def parentdistancefun(f, d):
    if f in parentchilddic:
        parent = parentchilddic[f]
        if not parent:
            return 0
        else:
            if parentdistancedic[parent] is not 0:
                parentdistancedic[f] = d
                return d
            else:
                d = int(parentdistancedic[parent]) + int(d)
                parentdistancedic[f] = d
                return d
    else:
        parentdistancedic[f] = d
        return 0
#expands the node and add to the fringe 
def fringeaddition(f, t, d):
    parentdistance = parentdistancefun(f, d)
    for i in range(len(from_city)):
        if from_city[i] == f and to_city[i] not in visitednode and to_city[i] not in fringedic:
            dish_h=heuristicdis(to_city[i])
	    fringedic[to_city[i]] = str(int(distance[i]) + int(parentdistance)+ int(dis_h))
            parentchilddic[to_city[i]] = from_city[i]
        elif to_city[i] == f and from_city[i] not in visitednode and from_city[i] not in fringedic:
	    dish_h=heuristicdis(from_city[i])
            fringedic[from_city[i]] = str(int(distance[i]) + int(parentdistance) + int(dis_h))
            parentchilddic[from_city[i]] = to_city[i]
    fringedics = sorted(fringedic.iteritems(), key=lambda (k, v): (v, k))
    visitednode.append(f)
    set(visitednode)
    state = check(fringedics, t, d)
    if state == 0:
        return fringedics


fringedics = fringeaddition(f, t, d)
backtrack(t, f)
total_distance = sum(distance1)
routeprint()
