import pyglet
import random
import timeit
import math
import numpy as np

white = (255, 255, 255)
green = (0, 155, 0)

n = 5
avg_degree = 5

X_coordinates = []
Y_coordinates = []
cell_map = []

start_offset = 0
end_offset = 500

r = math.sqrt(avg_degree / (n * math.pi)) * (end_offset - start_offset)
no_of_cells = int(math.ceil((end_offset - start_offset) / r))

window = pyglet.window.Window(500, 500)
# pyglet.gl.glClearColor(0.5,0.5,0.5,1)
# pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
# pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

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
            if x != y and x[0] < y[0]:
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

    @window.event
    def on_draw():
        window.clear()
        edges = 0
        # Draw edges
        for cell_set in cell_map:
            for adj in cell_set:
                if adj:
                    for coordinates in process(cell_set[0], adj, r_adjacency):
                        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                             ('v2i', (coordinates[0], coordinates[1], coordinates[2], coordinates[3])),
                                             ('c3B', (255, 0, 0,
                                                      255, 0, 0)))
                        edges += 1
                        # pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
                        # pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        # Draw nodes
        for node in range(nodes_count):
            pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
                                 ('v2i', (X_coordinates[node], Y_coordinates[node])),
                                 ('c3B', (255, 255, 0))
                                 )
        print('No. of edges: '+str(edges))



def main():

    start = timeit.default_timer()
    cellMapping()
    plotGraph(n, r)
    end = timeit.default_timer()
    print "\nElapsed time:" + str(end - start)
    pyglet.app.run()

main()



