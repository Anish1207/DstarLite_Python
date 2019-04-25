import heapq
import pygame
import math

from graph import Node, Graph
from grid import GridWorld
from d_star_lite import initDStarLite, moveAndRescan

# Define some colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
GRAY = (145, 145, 102)
DARKGRAY = (100, 100, 100)
BLUE  = (0, 0, 80)

colors = {
	 		 0: WHITE,
			 1: GREEN,
			-1: GRAY,
			-2: BLACK
		 }

# This sets the width and height of each grid location
width = 40
height = 40

# This sets the margin between each cell
margin = 2

dimension_x = 20	
dimension_y = 20
VIEWING_RANGE = 1

# Set the height and width of the screen
WINDOW_SIZE = [(width + margin) * dimension_x + margin,
			   (height + margin) * dimension_y + margin]

def draw_arrow(screen, colour, start, end):
    pygame.draw.line(screen,colour,start,end,1)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    rad=12
    pygame.draw.polygon(screen, BLACK, ((end[0]+rad*math.sin(math.radians(rotation)), end[1]+rad*math.cos(math.radians(rotation))), (end[0]+rad*math.sin(math.radians(rotation-120)), end[1]+rad*math.cos(math.radians(rotation-120))), (end[0]+rad*math.sin(math.radians(rotation+120)), end[1]+rad*math.cos(math.radians(rotation+120)))))

def stateNameToCoords(name):
    return [int(name.split('x')[1].split('y')[0]), int(name.split('x')[1].split('y')[1])]




transparent = pygame.Surface((3*width+3*margin,3*height+3*margin))  # the size of your rect
transparent.set_alpha(128)                # alpha level
transparent.fill(DARKGRAY)           # this fills the entire surface




def main():

	# Loop until the user clicks the close button.
	done = False

	
	graph = GridWorld(dimension_x, dimension_y)
	

	s_start=input("Enter start (xnym, where n,m are coordinates) : ")
	s_goal= input("Enter goal (xnym, where n,m are coordinates)  : ")
#	s_start = 'x1y2'
#	s_goal = 'x9y7'
	goal_coords = stateNameToCoords(s_goal)
	start_coords= stateNameToCoords(s_start)

	graph.setStart(s_start)
	graph.setGoal(s_goal)
	k_m = 0
	s_last = s_start
	queue = []

	graph, queue, k_m = initDStarLite(graph, queue, s_start, s_goal, k_m)

	s_current = s_start
	pos_coords = stateNameToCoords(s_current)

	
	robot_centers=[]


	# Initialize pygame
	pygame.init()

	screen = pygame.display.set_mode(WINDOW_SIZE)

	# Set title of screen
	pygame.display.set_caption("D* Lite Path Planning")

	# Used to manage how fast the screen updates
	clock = pygame.time.Clock()
	basicfont = pygame.font.SysFont('Comic Sans MS', 22)


	# -------- Main Program Loop -----------
	while done==False:
		for event in pygame.event.get():  # User did something
			if event.type == pygame.QUIT:  # If user clicked close
				done = True  # Flag that we are done so we exit this loop
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				print('move')
				s_new, k_m = moveAndRescan(graph, queue, s_current, k_m)
				
				if s_new == 'goal':
					print('Goal Reached!')
					done = True
				else:
					# print('setting s_current to ', s_new)
					s_current = s_new
					pos_coords = stateNameToCoords(s_current)
					# print('got pos coords: ', pos_coords)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				# User clicks the mouse. Get the position
				pos = pygame.mouse.get_pos()
				# Change the x/y screen coordinates to grid coordinates
				column = pos[0] // (width + margin)
				row = pos[1] // (height + margin)
				# Set that location to one
				if(graph.cells[row][column] == 0):
					graph.cells[row][column] = -1

		# Set the screen background
		screen.fill(BLACK)


		# Draw the grid
		for row in range(dimension_y):
			for column in range(dimension_x):
				

				pygame.draw.rect(screen, colors[graph.cells[row][column]],
								 [(margin + width) * column + margin,
								  (margin + height) * row + margin, width, height])
				node_name = 'x' + str(column) + 'y' + str(row)
				

		# fill in goal cell with GREEN
		pygame.draw.rect(screen, GREEN, [(margin + width) * start_coords[0] + margin,
										 (margin + height) * start_coords[1] + margin, width, height])
		

		# fill in goal cell with RED
		pygame.draw.rect(screen, RED, [(margin + width) * goal_coords[0] + margin,
										 (margin + height) * goal_coords[1] + margin, width, height])

		# draw moving robot, based on pos_coords

		# Set the new robot centre
		robot_center = [int(pos_coords[0] * (width + margin) + width / 2) + margin , int(pos_coords[1] * (height + margin) + height / 2) + margin]
		draw_arrow(screen, BLACK, robot_center,robot_center)

		# maintain a list of all cells traversed
		robot_centers.append(robot_center)

		if len(robot_centers)>1:
			for i in range(0,len(robot_centers)-1):
				pygame.draw.line(screen,BLACK,robot_centers[i],robot_centers[i+1],3)

		# grey out visible boxes for robot
		screen.blit(transparent,(robot_center[0]-1.5*width-margin,robot_center[1]-1.5*height-margin))    # (0,0) are the top-left coordinates

		# Limit to 60 frames per second
		clock.tick(20)

		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()

	# Be IDLE friendly. If you forget this line, the program will 'hang'
	# on exit.
	pygame.quit()





if __name__ == "__main__":
	main()
