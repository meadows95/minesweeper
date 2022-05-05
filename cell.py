import math
import pygame

BLACK = (0, 0, 0)
#light grey
CELL_COLOR_HIDDEN = (200, 201, 201)
#dark grey
CELL_COLOR_NOT_HIDDEN = (169, 169, 169)
HIDDEN_BORDER_COLOR_LIGHT = (249, 248, 246)
HIDDEN_BORDER_COLOR_DARK = (108, 108, 108)
 
# This sets the margin between each cell
DISTANCE_BETWEEN_CELLS = 8

class Cell():
    # properties: data type
    # hidden: boolean
    # x value: int
    # y value: int
    # occupant value: string (0, 1, 2, '3', or 'M')

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hidden = True
        self.occupant = None
        #should other properties be parameters of __init__?

    def draw(self, screen, screen_width, screen_height, font, grid_length):
        if self.hidden == True:
            color = CELL_COLOR_HIDDEN
        else:
            color = CELL_COLOR_NOT_HIDDEN

        cell_side_length = (screen_height // grid_length) - DISTANCE_BETWEEN_CELLS
        width_of_grid = cell_side_length * grid_length + ((grid_length - 1) * DISTANCE_BETWEEN_CELLS)
        margin = math.floor((screen_width - width_of_grid) / 2)
        rect_obj = self.draw_rectangle(
            screen,
            color,
            (DISTANCE_BETWEEN_CELLS + cell_side_length) * self.x + DISTANCE_BETWEEN_CELLS + margin,
            (DISTANCE_BETWEEN_CELLS + cell_side_length) * self.y + DISTANCE_BETWEEN_CELLS,
            cell_side_length)

        if self.hidden == False:
            if self.occupant != "0":
                text_surface_object = font.render(self.occupant, True, BLACK)
                text_rect = text_surface_object.get_rect(center=rect_obj.center)
                screen.blit(text_surface_object, text_rect)
    
    def draw_rectangle(self, screen, color, x_position, y_position, cell_side_length):
        rect = pygame.draw.rect(
            screen,
            color,
            [
                x_position,
                y_position,
                cell_side_length,
                cell_side_length
            ])
        if self.hidden:
            #setting the color for each side of the hidden cell to appear raised
            pygame.draw.rect(
                screen,
                HIDDEN_BORDER_COLOR_DARK, 
                [x_position - 0, y_position - 0, cell_side_length, cell_side_length],
                2)

            pygame.draw.rect(
                screen,
                HIDDEN_BORDER_COLOR_DARK, 
                [x_position - 1, y_position - 1, cell_side_length, cell_side_length],
                2)
                
            pygame.draw.rect(
                screen,
                HIDDEN_BORDER_COLOR_LIGHT, 
                [x_position - 2, y_position - 2, cell_side_length, cell_side_length],
                2)

            pygame.draw.rect(
                screen,
                HIDDEN_BORDER_COLOR_LIGHT, 
                [x_position - 3, y_position - 3, cell_side_length, cell_side_length],
                2)
        
        return rect

