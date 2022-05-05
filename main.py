from inspect import currentframe
import math
import time
from re import X
from tracemalloc import reset_peak
import pygame
from cell import Cell
from grid import Grid

# Define possible colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGREEN = (34, 69, 36)

current_time = None
start_time = None
 
# This sets the margin between each cell
DISTANCE_BETWEEN_CELLS = 8

# Initialize pygame
pygame.init()

BIG_FONT = pygame.font.Font(None, 80)
SMALL_FONT = pygame.font.Font(None, 45)
CELL_FONT = pygame.font.SysFont('Arial', 24)
END_OF_GAME_FONT = pygame.font.SysFont('Arial', 80, bold=True)

# Set the HEIGHT and WIDTH of the screen
video_infos = pygame.display.Info()
width, height = video_infos.current_w, video_infos.current_h
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
# w, h = pygame.display.get_surface().get_size()

# Set title of screen
pygame.display.set_caption("Minesweeper")

done = False
mine_clicked = False
has_started_stopwatch = False
win_lose_time = None

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

game_grid = Grid(10)

def display_end_game_text(screen, screen_width, screen_height, did_player_win):
    end_of_game_text_options = "You won!" if did_player_win else "You lose!"
    end_of_game_text = BIG_FONT.render(end_of_game_text_options, 13, BLACK)
    restart_prompt = SMALL_FONT.render('Press R to restart', False, BLACK)

    text_width = end_of_game_text.get_width()
    text_height = end_of_game_text.get_height()
    text_restart_prompt_height = restart_prompt.get_height()

    restart_prompt_x_position = screen_width / 2 - text_width / 2
    restart_prompt_y_position =  screen_height / 2 - text_height / 2 + text_height

    textx_position = screen_width / 2 - text_width / 2
    texty_position = screen_height / 2 - text_height / 2

    background_margin = 20

    background_x = textx_position - background_margin
    background_y = texty_position - background_margin
    background_width = text_width + (background_margin * 2)
    background_height = text_height + (background_margin * 2) + text_restart_prompt_height
    restart_prompt_width = restart_prompt.get_width()

    # Draw white background
    pygame.draw.rect(screen, WHITE, ((background_x, background_y), (background_width, background_height)))
    
    # Draw play again text
    screen.blit(end_of_game_text, (textx_position, texty_position))

    restart_prompt_x_position = (screen_width / 2) - (restart_prompt_width / 2)
    restart_prompt_y_position = texty_position + text_height

    # Draw restart text
    screen.blit(restart_prompt, (restart_prompt_x_position, restart_prompt_y_position))

def reset_game():
    # marks the variables as being in the global scope instead of local to the function
    global game_grid
    global mine_clicked
    global has_started_stopwatch
    global win_lose_time
    game_grid = Grid(10)
    mine_clicked = False
    has_started_stopwatch = False
    win_lose_time = None

def display_stopwatch():
    time_elapsed = None
    if mine_clicked or game_grid.did_player_win():
        time_elapsed = round(win_lose_time - start_time, 1)
    else:
        time_elapsed = round(current_time - start_time, 1)
    
    stopwatch_title = SMALL_FONT.render('Time: ' + str(time_elapsed), False, WHITE)
     # Draw stopwatch text
    stopwatch_position = (10, 10)
    screen.blit(stopwatch_title, stopwatch_position)

# -------- Main Program Loop -----------
while not done:
    current_time = time.time()
    screen_width, screen_height = pygame.display.get_surface().get_size()
    cell_side_length = (screen_height // game_grid.length) - DISTANCE_BETWEEN_CELLS
    width_of_grid = cell_side_length * game_grid.length + ((game_grid.length - 1) * DISTANCE_BETWEEN_CELLS)
    margin = math.floor((screen_width - width_of_grid) / 2)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            x_pixels = pos[0]
            y_pixels = pos[1]
            # Change the x/y screen coordinates to grid coordinates
            cell_x =  (x_pixels - margin) // (cell_side_length + DISTANCE_BETWEEN_CELLS)
            cell_y = y_pixels // (cell_side_length + DISTANCE_BETWEEN_CELLS)
            clicked_cell = game_grid.find_cell_by_x_and_y_grid_coordinates(cell_x, cell_y)

            # Set clicked_cell hidden value to false
            if clicked_cell != None and not mine_clicked and not game_grid.did_player_win():
                if not has_started_stopwatch:
                    has_started_stopwatch = True
                    start_time = time.time()
                    # do whatever to start the stopwatch
                clicked_cell.hidden = False

                if clicked_cell.occupant == "0":
                    game_grid.ripple_effect_recursive(clicked_cell, [])
                elif clicked_cell.occupant == "M":
                    mine_clicked = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if mine_clicked or game_grid.did_player_win():
                    reset_game()
 
    # Set the screen background
    screen.fill(DARKGREEN)

    for cell in game_grid.cells:
        cell.draw(screen, screen_width, screen_height, CELL_FONT, game_grid.length)

    if mine_clicked:
        display_end_game_text(screen, screen_width, screen_height, False)
        if not win_lose_time:
            win_lose_time = time.time()

    if game_grid.did_player_win():
        display_end_game_text(screen, screen_width, screen_height, True)
        if not win_lose_time:
            win_lose_time = time.time()

    if has_started_stopwatch:
        display_stopwatch()

    # Limit to 60 frames per second
    clock.tick(30)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()


pygame.quit()
