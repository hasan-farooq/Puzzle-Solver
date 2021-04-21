
import pygame
import math
from queue import PriorityQueue

WIDTH = 600
WINDOW = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding")

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)
orange = (128,128,128)
purple = (128,0,128)
some_color = (64,224,128)
line_color = (100,100,10)


class Cell:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.color = white
        self.neighbors = []
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == red

    def is_open(self):
        return self.color == green

    def is_obstacle(self):
        return self.color == black

    def is_start(self):
        return self.color == orange

    def is_end(self):
        return self.color == purple

    def is_reset(self):
        return self.color == white

# ---------------------------

    def closed(self):
        self.color = red

    def open(self):
        self.color = green

    def obstacle(self):
        self.color = black

    def start(self):
        self.color = orange

    def end(self):
        self.color = purple

    def reset(self):
        self.color = white

    def path(self):
        self.color = some_color
    
    def draw(self,window):
        pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.width))

# -------------------------------

    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row+1][self.col])
        # UP
        if self.row > 0 and not grid[self.row-1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row-1][self.col])
#       LEFT
        if self.col > 0 and not grid[self.row][self.col-1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col-1])
#       RIGHT
        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col+1])


    def __lt__(self,cell):
        return False


def heuristic(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def initialize_grid(rows,width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i,j,gap,rows)
            grid[i].append(cell)

    return grid

def reconstruct_path(came_from, cell, draw):
    while cell in came_from:
        cell = came_from[cell]
        cell.path()
        draw()

def draw_grid(window,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window,line_color,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(window,line_color,(j*gap,0),(j*gap,width))

def draw(window, grid, rows, width):
    window.fill(white)
    for row in grid:
        for cell in row:
            cell.draw(window)

    draw_grid(window,rows,width)
    pygame.display.update()

def get_click_position(position,rows,width):
    gap = width // rows
    x, y = position
    row = x // gap
    col = y // gap

    return row,col

def path_finder(draw, grid, start, goal):
    count = 0
    opened = PriorityQueue()   # returns the smallest value in the list
    opened.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_position(), goal.get_position())

    opened_elements = {start}  # bcz priority queue has no cheking elements method

    while not opened.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = opened.get()[2]
        opened_elements.remove(current)

        if current == goal:
            reconstruct_path(came_from, goal, draw)
            goal.end()
            start.start()
            return True

        for neighbor in current.neighbors:
            temp_g = g_score[current]+1

            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + heuristic(neighbor.get_position(),goal.get_position())
                if neighbor not in opened_elements:
                    count += 1
                    opened.put((f_score[neighbor], count, neighbor))
                    opened_elements.add(neighbor)
                    neighbor.open()    
        draw()

        if current != start:
            current.closed()

    return False



def main(window, width):
    rows = 30
    grid = initialize_grid(rows,width)
    start = None
    goal = None
    run = True
    started = False

    while run:
        draw(window,grid,rows,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:       #left button
                position = pygame.mouse.get_pos()
                row, col = get_click_position(position,rows, width)
                cell = grid[row][col]
                if not start:
                    start = cell
                    start.start()
                elif not goal:
                    goal = cell
                    goal.end()
                elif cell != goal and cell != start:
                    cell.obstacle()

            elif pygame.mouse.get_pressed()[2]:       #right button
                position = pygame.mouse.get_pos()
                row, col = get_click_position(position,rows, width)
                cell = grid[row][col]
                cell.reset()
                if cell == start:
                    start = None
                elif cell == goal:
                    goal = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    path_finder(lambda:draw(window,grid,rows,width),grid,start,goal)


    pygame.quit()



main(WINDOW,WIDTH)



