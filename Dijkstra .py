import pygame
import math
from queue import PriorityQueue

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Dijkstra  Path Finding Algorithm")

RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 255, 0) 
YELLOW = (255, 255, 0) 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
PURPLE = (128, 0, 128) 
ORANGE = (255, 165, 0) 
GREY = (128, 128, 128) 
TURQUOISE = (64, 224, 208) 

class Spot:
    def __init__(self, row, col, width, total_rows): 
        self.row = row
        self.col = col
        self.x = row * width # Width of the spot
        self.y = col * width # Height of the spot
        self.color = WHITE 
        self.neighbors = [] 
        self.width = width 
        self.total_rows = total_rows 

    def get_pos(self): 
        return self.row, self.col

    def is_closed(self): 
        return self.color == RED

    def is_open(self): 
        return self.color == GREEN

    def is_barrier(self): 
        return self.color == BLACK

    def is_start(self): 
        return self.color == ORANGE

    def is_end(self): 
        return self.color == TURQUOISE

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

    def draw(self, win): 
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid): 
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


def recontruct_path(came_from, current, draw):
    while current in came_from: 
        current = came_from[current] 
        current.make_path() 
        draw() 


def dijkstra(draw, grid, start, end): # Dijkstra algorithm
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    dist = {spot: float("inf") for row in grid for spot in row}
    dist[start] = 0

    while not open_set.empty():
        current = open_set.get()[2]

        if current == end:
            recontruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_dist = dist[current] + 1

            if temp_dist < dist[neighbor]:
                came_from[neighbor] = current
                dist[neighbor] = temp_dist

                if neighbor not in open_set.queue:
                    count += 1
                    open_set.put((dist[neighbor], count, neighbor))
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width): 
    grid = []
    gap = width // rows # Width of the spot
    for i in range(rows): # Loop through the rows
        grid.append([])
        for j in range(rows): # Loop through the columns
            spot = Spot(i, j, gap, rows) # Create a spot
            grid[i].append(spot) # Append the spot
    
    return grid


def draw_grid(win, rows, width): 
    gap = width // rows # Width of the spot
    for i in range(rows): # Loop through the rows
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # Draw the horizontal lines
        for j in range(rows): # Loop through the columns
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) # Draw the vertical lines


def draw(win, grid, rows, width): 
    win.fill(WHITE) 
   
    for row in grid: # Loop through the rows
        for spot in row: # Loop through the columns
            spot.draw(win) # Draw the spot
   
    draw_grid(win, rows, width) 
    pygame.display.update() # Update the display           


def get_clicked_pos(pos, rows, width): # Get the clicked position
    gap = width // rows # Width of the spot
    y, x = pos # Get the position
    row = y // gap # Get the row
    col = x // gap # Get the column
    
    return row, col # Return the row and column    


def main(win, width): 
    ROWS = 30 # Number of rows
    grid = make_grid(ROWS, width) 

    start = None 
    end = None 

    run = True 
    while run: 
        draw(win, grid, ROWS, width) 
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
                spot.reset() 
            
                if spot == start: 
                    start = None 

                elif spot == end: 
                    end = None 

            if event.type == pygame.KEYDOWN: # If a key is pressed
                if event.key == pygame.K_SPACE and start and end: # If the space bar is pressed and the algorithm has not started
                    for row in grid: # Loop through the rows
                        for spot in row: # Loop through the columns
                            spot.update_neighbors(grid) # Update the neighbors

                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end) # Run the algorithm        

                if event.key == pygame.K_c: # If the c key is pressed
                    start = None 
                    end = None 
                    grid = make_grid(ROWS, width) 

                    
    pygame.quit() 

main(WIN, WIDTH)    