import random
import timeit
import math

add_library('numpy')

n = 100
r = 0.5
# avg_degree = 3.2
X_coordinates = []
Y_coordinates = []

size(500, 500)
background(0)

for node in range(n):
    X_coordinates.append(random.randint(0, 500))
    Y_coordinates.append(random.randint(0, 500))

# r = int(math.ceil(math.sqrt(avg_degree/(n*math.pi))))
no_of_cells = int(math.ceil(500 / r))

for nodes in range(n):
    stroke(255, 255, 0)
    point(X_coordinates[nodes], Y_coordinates[nodes])

X_coordinates.sort()
start_offset = 0
cell_y = 0
# while cell_y < (no_of_cells * r):
for cell_y in numpy.arange(start_offset, start_offset + (no_of_cells * r), r):
    cell_x = start_offset
    for col in range(1, no_of_cells + 1):
        while cell_x < (col * r) + start_offset:
            if col == 1:
                primary_cell = []
                adjacent_cell1 = []
                adjacent_cell2 = []
                adjacent_cell3 = []
                adjacent_cell4 = []

                primary_cell.append([(X_coordinates[i], Y_coordinates[i]) for i in range(len(X_coordinates))
                                     if cell_x <= X_coordinates[i] <= (col * r) + start_offset
                                     and cell_y <= Y_coordinates[i] <= cell_y + r])

                adjacent_cell1.append([(X_coordinates[i], Y_coordinates[i]) for i in range(len(X_coordinates))
                                       if cell_x + r < X_coordinates[i] <= (col * r) + start_offset + r
                                       and cell_y < Y_coordinates[i] <= cell_y + r])

                adjacent_cell2.append([(X_coordinates[i], Y_coordinates[i]) for i in range(len(X_coordinates))
                                       if cell_x < X_coordinates[i] <= (col * r) + start_offset
                                       and cell_y + r < Y_coordinates[i] <= cell_y + r + r])

                adjacent_cell3.append([(X_coordinates[i], Y_coordinates[i]) for i in range(len(X_coordinates))
                                       if cell_x + r < X_coordinates[i] <= (col * r) + start_offset + r
                                       and cell_y + r < Y_coordinates[i] <= cell_y + r + r])

                # distance = [((y[0]-x[0])**2) + ((y[1]-x[1])**2) for x in primary_cell for y in primary_cell if x != y]

                if primary_cell[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in primary_cell[0]
                    ] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
        
                if adjacent_cell1[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in adjacent_cell1[0]
                    ] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
        
                if adjacent_cell2[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in
                    adjacent_cell2[0]] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
        
                if adjacent_cell3[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in
                    adjacent_cell3[0]] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
        
                if adjacent_cell4 and adjacent_cell4[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in
                    adjacent_cell4[0]] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])

                print('First column')
                print(primary_cell)
                print(adjacent_cell1)
                print(adjacent_cell2)
                print(adjacent_cell3)

            elif col == no_of_cells:
                primary_cell = []
                adjacent_cell1 = []
                adjacent_cell2 = []
                adjacent_cell3 = []
                adjacent_cell4 = []

                primary_cell.append([(X_coordinates[i], Y_coordinates[i]) for i in range(len(X_coordinates))
                                     if cell_x < X_coordinates[i] < (col * r) + start_offset
                                     and cell_y <= Y_coordinates[i] <= cell_y + r])

                adjacent_cell1.append([(X_coordinates[i], Y_coordinates[i]) for i in range(len(X_coordinates))
                                       if cell_x - r < X_coordinates[i] <= cell_x
                                       and cell_y + r < Y_coordinates[i] <= cell_y + r + r])

                adjacent_cell2.append([(X_coordinates[i], Y_coordinates[i]) for i in range(len(X_coordinates))
                                       if cell_x < X_coordinates[i] <= (col * r) + start_offset
                                       and cell_y + r < Y_coordinates[i] <= cell_y + r + r])
                
                
                if primary_cell[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in primary_cell[0]
                    ] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
        
                if adjacent_cell1[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in adjacent_cell1[0]
                    ] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
        
                if adjacent_cell2[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in
                    adjacent_cell2[0]] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
        
                if adjacent_cell3[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in
                    adjacent_cell3[0]] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
        
                if adjacent_cell4 and adjacent_cell4[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in
                    adjacent_cell4[0]] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
                    
                # print('\nLast column')
                # print(primary_cell)
                # print(adjacent_cell1)
                # print(adjacent_cell2)

            else:
                primary_cell = []
                adjacent_cell1 = []
                adjacent_cell2 = []
                adjacent_cell3 = []
                adjacent_cell4 = []

                primary_cell.append([(X_coordinates[i], Y_coordinates[i]) for i in range(len(X_coordinates))
                                     if cell_x < X_coordinates[i] < (col * r) + start_offset
                                     and cell_y <= Y_coordinates[i] <= cell_y + r])

                adjacent_cell4.append([(X_coordinates[i], Y_coordinates[i]) for i in range(len(X_coordinates))
                                       if cell_x - r < X_coordinates[i] <= cell_x
                                       and cell_y + r < Y_coordinates[i] <= cell_y + r + r])

                adjacent_cell2.append([(X_coordinates[i], Y_coordinates[i]) for i in range(len(X_coordinates))
                                       if cell_x < X_coordinates[i] <= (col * r) + start_offset
                                       and cell_y + r < Y_coordinates[i] <= cell_y + r + r])

                adjacent_cell1.append([(X_coordinates[i], Y_coordinates[i]) for i in range(len(X_coordinates))
                                       if cell_x + r < X_coordinates[i] <= (
                                           col * r) + start_offset + r
                                       and cell_y < Y_coordinates[i] <= cell_y + r])

                adjacent_cell3.append([(X_coordinates[i], Y_coordinates[i]) for i in range(len(X_coordinates))
                                       if cell_x + r < X_coordinates[i] <= (
                                           col * r) + start_offset + r
                                       and cell_y + r < Y_coordinates[i] <= cell_y + r + r])
                
                if primary_cell[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in primary_cell[0]
                    ] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
        
                if adjacent_cell1[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in adjacent_cell1[0]
                    ] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
        
                if adjacent_cell2[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in
                    adjacent_cell2[0]] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
        
                if adjacent_cell3[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in
                    adjacent_cell3[0]] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])
        
                if adjacent_cell4 and adjacent_cell4[0] and [((y[0] - x[0]) ** 2) + ((y[1] - x[1]) ** 2) for x in primary_cell[0] for y in
                    adjacent_cell4[0]] < (r ** 2):
                    stroke(255, 255, 255)
                    line(x[0], x[1], y[0], y[1])

                # print('Middle column ' + str(col))
                # print(primary_cell)
                # print(adjacent_cell1)
                # print(adjacent_cell2)
                # print(adjacent_cell3)
                # print(adjacent_cell4)
                # print('-------------\n')

            cell_x += r