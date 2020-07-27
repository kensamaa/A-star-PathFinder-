import pygame
import math
from queue import PriorityQueue#FIFO

WIDTH = 800#size 
WIN = pygame.display.set_mode((WIDTH, WIDTH))#how big the display is
pygame.display.set_caption("A* Path Finding Algorithm")#title of the dispaly
#colors code
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)#finish
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)#obstacl
PURPLE = (128, 0, 128)#path
ORANGE = (255, 165 ,0)#start
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:#the square in the display and the node in the algorithm
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE#at the start we gonna have all white cubes
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col
	#set the colors of the spots depends on event
	def is_closed(self):#is the spot looked or considered (red square)
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE
#set the colors of the spots depends on event
	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):#draw the cub
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []#add the neigbor spots of this self spot one spot has 4 neighbors up down left right
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN spot
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP spot
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT spot
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT spot
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):#handl what happend when we compar two spots
		return False


def h(p1, p2):#point1(x,y) point2
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)#absolute distance of (x1-x2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:#while current is in came from,a came from b , c came from b
		current = came_from[current]
		current.make_path()#purpl color
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()#fifo with priority
	open_set.put((0, count, start))#start is the node aka spot we add it to the queue
	came_from = {}#what node did this node came from ,to find the best path
	g_score = {spot: float("inf") for row in grid for spot in row}#keeps track of the current shorts distance from start node to end,set all to infiniti
	g_score[start] = 0#g score of start node is 0
	f_score = {spot: float("inf") for row in grid for spot in row}#keeps track of the predicted distance from this node  to end,how long will it take
	f_score[start] = h(start.get_pos(), end.get_pos())#distance from start to finish node

	open_set_hash = {start}#to check if node is in it cause we cant chen in the queu

	while not open_set.empty():#runs until open set is empty or not means we considered every node we going to 
		for event in pygame.event.get():#if we want to quit
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]#start in 2 cause set is gonna store start and end node
		open_set_hash.remove(current)#remove from sethash to make sure we dont have duplicate

		if current == end:#if the node we arrived to is the end node
			reconstruct_path(came_from, end, draw)#make the path we found
			end.make_end()#not to draw purpl of end node
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:#if we found a better way to reach the neigbor we update the score
				came_from[neighbor] = current#update the neigbor we came from
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:#check if neigbor is in the set
					count += 1#we add the neibgho cause we have better path than before
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()#we already considered the neighbor+changing the color

		draw()

		if current != start:
			current.make_closed()#if the node we just considered is not start we make red we already considered it,its not gonna be added to opneset

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))#draw a line(display,color,start,end)
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))#draw a line(display,color,start,end)


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

'''
first left click is for start point 
the second left click is for end point 
after is obstacle 
if we right click any spot, it removes it ,the left click to add it again
space key is for start of the programe
'''
def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)#generat grid doubl list filled with spots

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)#draw the grid
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT mouse button
				pos = pygame.mouse.get_pos()#get the position of the mouse on the screen
				row, col = get_clicked_pos(pos, ROWS, width)#get col row where we clicked
				spot = grid[row][col] #index spot in the grid there
				if not start and spot != end:#if its the first click then its a start
					start = spot
					start.make_start()#orange color

				elif not end and spot != start:#if its not the first and then its the end spot or target
					end = spot
					end.make_end()#end color

				elif spot != end and spot != start:#else its a barrier or obstacle
					spot.make_barrier() #black color

			elif pygame.mouse.get_pressed()[2]: # RIGHT mouse button
				pos = pygame.mouse.get_pos()#get postion of the mouse
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:#if if we pressed a key 
				if event.key == pygame.K_SPACE and start and end:#if the key is space
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)#update what the neigbors of the spot if we clciked space and its not start or end

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)#let the algorithm work

				if event.key == pygame.K_c:#reset  
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)#calling the main
