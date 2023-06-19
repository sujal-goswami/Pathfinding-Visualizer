import pygame
import math
from queue import PriorityQueue

WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0) # RGB
GREEN = (0, 255, 0) # RGB
BLUE = (0, 255, 0) # RGB
YELLOW = (255, 255, 0) # RGB
WHITE = (255, 255, 255) # RGB
BLACK = (0, 0, 0) # RGB
PURPLE = (128, 0, 128) # RGB
ORANGE = (255, 165, 0) # RGB
GREY = (128, 128, 128) # RGB
TURQUOISE = (64, 224, 208) # RGB

class Spot:
    def __init__(self, row, col, width, total_rows): # Constructor
        self.row = row
        self.col = col
        self.x = row * width # Width of the spot
        self.y = col * width # Height of the spot
        self.color = WHITE # Default color
        self.neighbors = [] # Neighbors of the spot
        self.width = width # Width of the spot
        self.total_rows = total_rows # Total rows

    def get_pos(self): # Get position
        return self.row, self.col

    def is_closed(self): # Is the spot closed
        return self.color == RED

    def is_open(self): # Is the spot open
        return self.color == GREEN

    def is_barrier(self): # Is the spot a barrier
        return self.color == BLACK

    def is_start(self): # Is the spot the start
        return self.color == ORANGE

    def is_end(self): # Is the spot the end
        return self.color == TURQUOISE

    def reset(self): # Reset the spot
        self.color = WHITE

    def make_start(self): # Make the spot the start
        self.color = ORANGE

    def make_closed(self): # Make the spot closed
        self.color = RED

    def make_open(self): # Make the spot open
        self.color = GREEN

    def make_barrier(self): # Make the spot a barrier
        self.color = BLACK

    def make_end(self): # Make the spot the end
        self.color = TURQUOISE

    def make_path(self): # Make the spot the path
        self.color = PURPLE

    def draw(self, win): # Draw the spot
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid): # Update the neighbors
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Left
            self.neighbors.append(grid[self.row][self.col - 1])    


    def __lt__(self, other):
        return False


def h(p1, p2): # Heuristic function
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2) # Manhattan distance    

# def h2(p1, p2): # Heuristic function
#     x1, y1 = p1
#     x2, y2 = p2
#     return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) # Euclidean distance

def recontruct_path(came_from, current, draw): # Reconstruct the path
    while current in came_from: # While the current spot is in the came from
        current = came_from[current] # Current spot is the came from of the current spot
        current.make_path() # Make the current spot the path
        draw() # Draw the current spot


def algorithm(draw, grid, start, end): # Algorithm
    count = 0
    open_set = PriorityQueue() # Open set
    open_set.put((0, count, start)) # Put the start in the open set
    came_from = {} # Came from
    g_score = {spot: float("inf") for row in grid for spot in row} # G score
    g_score[start] = 0 # G score of the start
    f_score = {spot: float("inf") for row in grid for spot in row} # F score
    f_score[start] = h(start.get_pos(), end.get_pos()) # F score of the start

    open_set_hash = {start} # Open set hash

    while not open_set.empty(): # While the open set is not empty
        for event in pygame.event.get(): # Loop through the events
            if event.type == pygame.QUIT: # If the event is quit
                pygame.quit() # Quit pygame

        current = open_set.get()[2] # Get the current spot
        open_set_hash.remove(current) # Remove the current spot from the open set hash

        if current == end: # If the current spot is the end
            recontruct_path(came_from, end, draw) # Reconstruct the path
            end.make_end() # Make the end
            return True 

        for neighbor in current.neighbors: # Loop through the neighbors
            temp_g_score = g_score[current] + 1 # Temp g score

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current # Came from
                g_score[neighbor] = temp_g_score # G score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) # F score
                if neighbor not in open_set_hash: # If the neighbor is not in the open set hash
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor)) # Put the neighbor in the open set
                    open_set_hash.add(neighbor) # Add the neighbor to the open set hash
                    neighbor.make_open() # Make the neighbor open

        draw()

        if current != start: # If the current spot is not the start
            current.make_closed() # Make the current spot closed

    return False


def make_grid(rows, width): # Make the grid
    grid = []
    gap = width // rows # Width of the spot
    for i in range(rows): # Loop through the rows
        grid.append([])
        for j in range(rows): # Loop through the columns
            spot = Spot(i, j, gap, rows) # Create a spot
            grid[i].append(spot) # Append the spot
    
    return grid


def draw_grid(win, rows, width): # Draw the grid
    gap = width // rows # Width of the spot
    for i in range(rows): # Loop through the rows
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # Draw the horizontal lines
        for j in range(rows): # Loop through the columns
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) # Draw the vertical lines


def draw(win, grid, rows, width): # Draw the grid
    win.fill(WHITE) # Fill the screen with white
   
    for row in grid: # Loop through the rows
        for spot in row: # Loop through the columns
            spot.draw(win) # Draw the spot
   
    draw_grid(win, rows, width) # Draw the grid
    pygame.display.update() # Update the display           


def get_clicked_pos(pos, rows, width): # Get the clicked position
    gap = width // rows # Width of the spot
    y, x = pos # Get the position
    row = y // gap # Get the row
    col = x // gap # Get the column
    
    return row, col # Return the row and column    


def main(win, width): # Main function
    ROWS = 20 # Number of rows
    grid = make_grid(ROWS, width) # Make the grid

    start = None # Start
    end = None # End

    run = True # Run
    while run: # While running
        draw(win, grid, ROWS, width) # Draw the grid
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col] # Get the spot
                if not start and spot != end: # If there is no start and the spot is not the end
                    start = spot # Make the spot the start
                    start.make_start() # Make the spot the start

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()
                        

            elif pygame.mouse.get_pressed()[2]: # Right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col] # Get the spot
                spot.reset() # Reset the spot
                
                if spot == start: # If the spot is the start
                    start = None # Make the start none

                elif spot == end: # If the spot is the end
                    end = None # Make the end none

            if event.type == pygame.KEYDOWN: # If a key is pressed
                if event.key == pygame.K_SPACE and start and end: # If the space bar is pressed and the algorithm has not started
                    for row in grid: # Loop through the rows
                        for spot in row: # Loop through the columns
                            spot.update_neighbors(grid) # Update the neighbors

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end) # Run the algorithm        

                if event.key == pygame.K_c: # If the c key is pressed
                    start = None # Make the start none
                    end = None # Make the end none
                    grid = make_grid(ROWS, width) # Make the grid

                    
    pygame.quit() # Quit pygame

main(WIN, WIDTH) # Run the main function    