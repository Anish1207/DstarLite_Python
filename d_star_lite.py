import heapq
import sys


def stateNameToCoords(name):
	return [int(name.split('x')[1].split('y')[0]), int(name.split('x')[1].split('y')[1])]

def topKey(queue):
	queue.sort()
	# print(queue)
	if len(queue) > 0:
		return queue[0][:2]
	else:
		# print('empty queue!')
		return (float('inf'), float('inf'))

def heuristic_from_s(Graph, id, s):
	x_distance = abs(int(id.split('x')[1][0]) - int(s.split('x')[1][0]))
	y_distance = abs(int(id.split('y')[1][0]) - int(s.split('y')[1][0]))
	return max(x_distance, y_distance)

def calculateKey(Graph, id, s_current, k_m):
	return (min(Graph.graph[id].g, Graph.graph[id].rhs) + heuristic_from_s(Graph, id, s_current) + k_m, 
			min(Graph.graph[id].g, Graph.graph[id].rhs))

def updateVertex(Graph, queue, id, s_current, k_m):
#	s_goal = Graph.goal

	if id != Graph.goal:
		min_rhs = float('inf')
		for i in Graph.graph[id].children:
			min_rhs = min(min_rhs, Graph.graph[i].g + Graph.graph[id].children[i])
		Graph.graph[id].rhs = min_rhs

	id_in_queue = [item for item in queue if id in item]

	if id_in_queue != []:
		if len(id_in_queue) != 1:
			raise ValueError('more than one ' + id + ' in the queue!')
		queue.remove(id_in_queue[0])
		
	if Graph.graph[id].rhs != Graph.graph[id].g:
		heapq.heappush(queue, calculateKey(Graph, id, s_current, k_m) + (id,))


def computeShortestPath(Graph, queue, s_start, k_m):
	while (Graph.graph[s_start].rhs != Graph.graph[s_start].g) or (topKey(queue) < calculateKey(Graph, s_start, s_start, k_m)):
		# print(Graph.graph[s_start])
		# print('topKey')
		# print(topKey(queue))
		# print('calculateKey')
		# print(calculateKey(Graph, s_start, 0))
		k_old = topKey(queue)
		u = heapq.heappop(queue)[2]

		if k_old < calculateKey(Graph, u, s_start, k_m):
			heapq.heappush(queue, calculateKey(Graph, u, s_start, k_m) + (u,))

		elif Graph.graph[u].g > Graph.graph[u].rhs:
			Graph.graph[u].g = Graph.graph[u].rhs
			for i in Graph.graph[u].parents:
				updateVertex(Graph, queue, i, s_start, k_m)
		
		else:
			Graph.graph[u].g = float('inf')
			updateVertex(Graph, queue, u, s_start, k_m)
			for i in Graph.graph[u].parents:
				updateVertex(Graph, queue, i, s_start, k_m)
		# Graph.printGValues()


def nextInShortestPath(Graph, s_current):
	min_rhs = float('inf')
	s_next = None
	
	if Graph.graph[s_current].rhs == float('inf'):
		print('You are done stuck')
		sys.exit()


	else:
		for i in Graph.graph[s_current].children:
			# print(i)
			child_cost = Graph.graph[i].g + Graph.graph[s_current].children[i]
			# print(child_cost)
			if (child_cost) < min_rhs:
				min_rhs = child_cost
				s_next = i
		if s_next:
			return s_next
		else:
			raise ValueError('could not find child for transition!')

def scanForObstacles(Graph, queue, s_current, k_m):
	states_to_update = {}

	for neighbor in Graph.graph[s_current].children:
		neighbor_coords = stateNameToCoords(neighbor)
		states_to_update[neighbor] = Graph.cells[neighbor_coords[1]][neighbor_coords[0]]

	new_obstacle = False
	for state in states_to_update:
		if states_to_update[state] < 0:  # found cell with obstacle
			# print('found obstacle in ', state)
			for neighbor in Graph.graph[state].children:
				# first time to observe this obstacle where one wasn't before
				if(Graph.graph[state].children[neighbor] != float('inf')):
					neighbor_coords = stateNameToCoords(state)
					Graph.cells[neighbor_coords[1]][neighbor_coords[0]] = -2
					Graph.graph[neighbor].children[state] = float('inf')
					Graph.graph[state].children[neighbor] = float('inf')
					updateVertex(Graph, queue, state, s_current, k_m)
					new_obstacle = True
		# elif states_to_update[state] == 0: #cell without obstacle
			# for neighbor in Graph.graph[state].children:
				# if(Graph.graph[state].children[neighbor] != float('inf')):

	# print(graph)
	return new_obstacle



def moveAndRescan(Graph, queue, s_current,k_m):
	if(s_current == Graph.goal):
		return 'goal', k_m
	else:
		s_last = s_current
		s_new = nextInShortestPath(Graph, s_current)
		new_coords = stateNameToCoords(s_new)

#		if(Graph.cells[new_coords[1]][new_coords[0]] ==-1):  # just ran into new obstacle
#			s_new = s_last  # need to hold tight and scan/replan first

		results = scanForObstacles(Graph, queue, s_new, k_m)
		# print(graph)
		k_m += heuristic_from_s(Graph, s_last, s_new)
		computeShortestPath(Graph, queue, s_current, k_m)

		return s_new, k_m


def initDStarLite(Graph, queue, s_start, s_goal, k_m):
	Graph.graph[s_goal].rhs = 0
	heapq.heappush(queue, calculateKey(Graph, s_goal, s_start, k_m) + (s_goal,))
	print(queue[0])
	computeShortestPath(Graph, queue, s_start, k_m)
	
	return (Graph, queue, k_m)
