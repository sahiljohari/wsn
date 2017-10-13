import pygame
import random
import timeit
import math
import numpy as np

pygame.init()
display_width = 500
display_height = 500
clock = pygame.time.Clock()
graphDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Wireless Sensor Network Graph')
white = (255, 255, 255)
green = (0, 155, 0)

n = 4000
avg_degree = 32

X_coordinates = []
Y_coordinates = []
cell_map = []

start_offset = 0
end_offset = 500

r = math.sqrt(avg_degree / (n * math.pi)) * (end_offset - start_offset)
no_of_cells = int(math.ceil((end_offset - start_offset) / r))

done = False

def cellMapping():

    for node in range(n):
        X_coordinates.append(random.randint(start_offset, end_offset))
        Y_coordinates.append(random.randint(start_offset, end_offset))

    X_coordinates.sort()
    # start = timeit.default_timer()
    for cell_y in np.arange(start_offset, start_offset + (no_of_cells * r), r):
        for cell_x in np.arange(start_offset, start_offset + no_of_cells * r, r):

            primary_cell = []
            adjacent_cell1 = []
            adjacent_cell2 = []
            adjacent_cell3 = []
            adjacent_cell4 = []

            for i in range(n):
                if cell_x < X_coordinates[i] < (cell_x + r) + start_offset and cell_y <= Y_coordinates[i] <= cell_y + r:
                    primary_cell.append((X_coordinates[i], Y_coordinates[i]))

                if cell_x - r < X_coordinates[i] <= cell_x and cell_y + r < Y_coordinates[i] <= cell_y + r + r and (math.ceil(cell_x/r)+1 != 1 or math.ceil(cell_x/r)+1 == no_of_cells):
                    adjacent_cell1.append((X_coordinates[i], Y_coordinates[i]))

                if cell_x < X_coordinates[i] <= cell_x + r + start_offset and cell_y + r < Y_coordinates[i] <= cell_y + r + r:
                    adjacent_cell2.append((X_coordinates[i], Y_coordinates[i]))

                if cell_x + r < X_coordinates[i] <= cell_x + r + start_offset + r and cell_y + r < Y_coordinates[i] <= cell_y + r + r and (math.ceil(cell_x/r)+1 == 1 or math.ceil(cell_x/r)+1 != no_of_cells):
                    adjacent_cell3.append((X_coordinates[i], Y_coordinates[i]))

                if cell_x + r < X_coordinates[i] <= cell_x + r + start_offset + r and cell_y < Y_coordinates[i] <= cell_y + r and (math.ceil(cell_x/r)+1 == 1 or math.ceil(cell_x/r)+1 != no_of_cells):
                    adjacent_cell4.append((X_coordinates[i], Y_coordinates[i]))

            cell_map.append([primary_cell, adjacent_cell1, adjacent_cell2, adjacent_cell3, adjacent_cell4])

def process(srcCell, destCell, r_adjacency):
    line = []
    for x in srcCell:
        for y in destCell:
            if x != y:
                distance = ((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2)
                if distance < (r_adjacency ** 2):
                    line_coordinates = []
                    line_coordinates.append(x[0])
                    line_coordinates.append(x[1])
                    line_coordinates.append(y[0])
                    line_coordinates.append(y[1])
                    line.append(line_coordinates)
    return line

def plotGraph(nodes_count, r_adjacency):

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # Draw nodes
        for nodes in range(nodes_count):
            pygame.draw.circle(graphDisplay, green, (X_coordinates[nodes], Y_coordinates[nodes]), 2, 0)

        # Draw edges
        for cell_set in cell_map:
            for adj in cell_set:
                if adj:
                    for coordinates in process(cell_set[0], adj, r_adjacency):
                        pygame.draw.line(graphDisplay, white, (coordinates[0], coordinates[1]),
                                         (coordinates[2], coordinates[3]), 1)

        pygame.display.update()
        clock.tick(60)

def main():

    start = timeit.default_timer()
    cellMapping()
    end = timeit.default_timer()
    print "\nElapsed time:" + str(end - start)

    plotGraph(n, r)
main()
