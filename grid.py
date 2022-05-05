import random
import math
from cell import Cell

class Grid():
    # properties:
    # cells: list

    def __init__(self, length):
        self.cells = []
        self.length = length
        #list of cells used to make the grid
        for y in range(self.length):
            for x in range(self.length):
                #create new instance of the cell class with every x and y value in the range
                cell = Cell(x, y)
                #add new cell to list of cells
                self.cells.append(cell)
        self.place_mines()
        self.populate_grid()

    def place_mines(self):
        distinct_num_of_mines_placed = 0
        max_number_of_mines = math.floor((self.length * self.length) * .1)
        while distinct_num_of_mines_placed < max_number_of_mines:
            random_cell = random.choice(self.cells)
            if random_cell.occupant == None:
                random_cell.occupant = "M"
                distinct_num_of_mines_placed = distinct_num_of_mines_placed + 1    

    # populates the grid based on the position of the mines
    def populate_grid(self):
        for cell in self.cells:
            if cell.occupant != "M":
                neighbors = self.get_neighbors(cell)
                num_of_mines = 0
                for neighbor in neighbors:
                    if neighbor.occupant == "M":
                        num_of_mines = num_of_mines + 1
                cell.occupant = str(num_of_mines)

    def get_neighbors(self, cell):
        neighbors = []
        for possible_neighbor_cell in self.cells:
            if possible_neighbor_cell.x == cell.x - 1 and possible_neighbor_cell.y == cell.y:
                #adding left neighbor
                neighbors.append(possible_neighbor_cell)
            elif possible_neighbor_cell.x == cell.x + 1 and possible_neighbor_cell.y == cell.y:
                #adding right neighbor
                neighbors.append(possible_neighbor_cell)
            elif possible_neighbor_cell.x == cell.x and possible_neighbor_cell.y == cell.y + 1:
                #adding neighbor above (y + 1)
                neighbors.append(possible_neighbor_cell)
            elif possible_neighbor_cell.x == cell.x and possible_neighbor_cell.y == cell.y - 1:
                #adding neighbor below (y - 1)
                neighbors.append(possible_neighbor_cell)
            elif possible_neighbor_cell.x == cell.x - 1 and possible_neighbor_cell.y == cell.y + 1:
                #adding upper left diagonal neighbor
                neighbors.append(possible_neighbor_cell)
            elif possible_neighbor_cell.x == cell.x - 1 and possible_neighbor_cell.y == cell.y - 1:
                #adding lower left diagonal neighbor
                neighbors.append(possible_neighbor_cell)
            elif possible_neighbor_cell.x == cell.x + 1 and possible_neighbor_cell.y == cell.y + 1:
                #adding upper right diagonal neighbor
                neighbors.append(possible_neighbor_cell)
            elif possible_neighbor_cell.x == cell.x + 1 and possible_neighbor_cell.y == cell.y - 1:
                #adding lower right diagonal neighbor
                neighbors.append(possible_neighbor_cell)
        return neighbors

#how many spaces/open lines between methods?

    def print_grid(self):
        for cell in self.cells:
            if cell.x == (self.length - 1):
                print(cell.occupant)
            else: 
                #when adding (end = "") as a parameter, it will print on the same line 
                print(cell.occupant + " ", end = "")
    
    def count_mines(self):
        number_of_mines = 0
        for cell in self.cells:
            if cell.occupant == "M":
                number_of_mines += 1
        return number_of_mines

    def find_cell_by_x_and_y_grid_coordinates(self, cell_x, cell_y):
        for cell in self.cells:
            if cell.x == cell_x and cell.y == cell_y:
                return cell

    def ripple_effect(self, clicked_cell):
        unchecked_cells = []
        checked_cells = []
        unchecked_cells.append(clicked_cell)

        while len(unchecked_cells) > 0:
            cell = unchecked_cells.pop()
            neighbor_cells = self.get_neighbors(cell)
            checked_cells.append(cell)
            for neighbor_cell in neighbor_cells:
                if neighbor_cell.occupant == "0":
                    neighbor_cell.hidden = False
                    if neighbor_cell not in checked_cells:
                        unchecked_cells.append(neighbor_cell)

    def ripple_effect_recursive(self, cell, checked_cells):
        checked_cells.append(cell)
        neighbor_cells = self.get_neighbors(cell)
        for neighbor_cell in neighbor_cells:
            if neighbor_cell.occupant == "0":
                neighbor_cell.hidden = False
                if neighbor_cell not in checked_cells:
                    self.ripple_effect_recursive(neighbor_cell, checked_cells)


    def did_player_win(self):
        for cell in self.cells:
            if cell.occupant == "0" and cell.hidden == True:
                return False
        return True