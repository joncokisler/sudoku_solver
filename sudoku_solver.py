import pygame
import time

__author__ = "Jon Cokisler"
__copyright__ = "Copyright 2020, SudokuSolver by Jon Cokisler"
__credits__ = ["Jon Cokisler"]
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "can.cokisler@gmail.com"
__status__ = "Production"

pygame.init()

WINDOW_SIZE = [325, 325]
WIDTH = 30
HEIGHT = 30
MARGIN = 5
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("SUDOKU SOLVER(PRESS SPACEBAR TO START)")

grid = [[0, 0, 0, 0, 0, 2, 3, 1, 0],
        [2, 0, 0, 4, 0, 0, 0, 0, 0],
        [5, 9, 0, 6, 8, 0, 0, 7, 4],
        [6, 5, 8, 9, 0, 7, 0, 2, 0],
        [0, 7, 0, 0, 0, 0, 0, 6, 0],
        [0, 2, 0, 3, 0, 6, 7, 8, 1],
        [9, 6, 0, 0, 7, 3, 0, 5, 2],
        [0, 0, 0, 0, 0, 9, 0, 0, 8],
        [0, 8, 2, 5, 0, 0, 0, 0, 0]]

grid_copy = grid.copy()

clicked_grid = []
for row in range(9):
    clicked_grid.append([])
    for column in range(9):
        clicked_grid[row].append(0)


def reset_grid():
    """"""
    grid = [[0, 0, 0, 0, 0, 2, 3, 1, 0],
            [2, 0, 0, 4, 0, 0, 0, 0, 0],
            [5, 9, 0, 6, 8, 0, 0, 7, 4],
            [6, 5, 8, 9, 0, 7, 0, 2, 0],
            [0, 7, 0, 0, 0, 0, 0, 6, 0],
            [0, 2, 0, 3, 0, 6, 7, 8, 1],
            [9, 6, 0, 0, 7, 3, 0, 5, 2],
            [0, 0, 0, 0, 0, 9, 0, 0, 8],
            [0, 8, 2, 5, 0, 0, 0, 0, 0]]


def solve(grid: []) -> bool:
    """Solves the sudoku puzzle"""
    next_box = find_next_box(grid)

    if next_box is None:
        return True
    draw_manual()

    for i in range(1, 10):
        # grid_copy[next_box[0]][next_box[1]] = i
        draw_manual()

        if is_valid(grid, next_box, i):
            # grid_copy[next_box[0]][next_box[1]] = i
            grid[next_box[0]][next_box[1]] = i
            clicked_grid[next_box[0]][next_box[1]] = 1

            if solve(grid):
                return True
            else:
                grid[next_box[0]][next_box[1]] = 0
                # grid_copy[next_box[0]][next_box[1]] = 0
        else:
            clicked_grid[next_box[0]][next_box[1]] = 2

    return False


def find_next_box(grid: []) -> any:
    """Finds the next empty box in the puzzle"""
    for row in range(9):
        for column in range(9):
            if grid[row][column] == 0:
                return (row, column)
    return None


def is_valid(grid: [], position: tuple, num: int) -> bool:
    """Checks to see if the current solution is correct"""
    # check vertically
    for row in range(9):
        if grid[row][position[1]] == num:
            return False
    # check horizontally
    for column in range(9):
        if grid[position[0]][column] == num:
            return False

    # check inside the box
    row_box = (position[0] // 3)
    col_box = (position[1] // 3)

    for row in range(row_box * 3, (row_box * 3) + 3):
        for column in range(col_box * 3, (col_box * 3) + 3):
            if grid[row][column] == num:
                return False
    return True


def draw():
    """Main method. Draws the board and takes the input"""
    done = False
    my_font = pygame.font.SysFont("monospace", 25)
    while not done:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:

                position = pygame.mouse.get_pos()
                column = position[0] // (WIDTH + MARGIN)
                row = position[1] // (HEIGHT + MARGIN)
                if grid[row][column] != 0:
                    pass
                else:
                    clicked_grid[row][column] = 1
            # un-highlights the box
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:

                position = pygame.mouse.get_pos()
                column = position[0] // (WIDTH + MARGIN)
                row = position[1] // (HEIGHT + MARGIN)

                clicked_grid[row][column] = 0

            # automatically solves the puzzle
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_grid()
                done = True

                solve(grid)
                draw()


            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                # reset clicked_grid
                for row in range(9):
                    for column in range(9):
                        clicked_grid[row][column] = 0
        screen.fill((0, 0, 0))
        color = (177, 205, 205)
        for row in range(9):
            for column in range(9):
                if clicked_grid[row][column] == 1:
                    color = (0, 255, 0)
                elif clicked_grid[row][column] == 2:
                    color = (255, 0, 0)

                pygame.draw.rect(
                    screen, color,
                    [(MARGIN + WIDTH) * column + MARGIN,
                     (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
                color = (177, 205, 205)

                # render text
                if grid[row][column] == 0:
                    txt = ""
                else:
                    txt = str(grid[row][column])

                label = my_font.render("{}".format(txt), 1, (0, 0, 0))
                screen.blit(label, ((MARGIN + WIDTH) * column + MARGIN + 10,
                                    (MARGIN + HEIGHT) * row + MARGIN + 10))
        offset = 0
        for i in range(3):
            pygame.draw.rect(screen, (51, 153, 102),
                             pygame.Rect((0, (i + 1) * 108.3 - offset, 325, 5)))
            offset += 5

        offset = 0
        for i in range(3):
            pygame.draw.rect(screen, (51, 153, 102),
                             pygame.Rect(((i + 1) * 108.3 - offset, 0, 5, 325)))
            offset += 5
        pygame.display.flip()


def draw_manual():
    """Main method for when the board needs to be refreshed manually."""
    my_font = pygame.font.SysFont("monospace", 25)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:

            position = pygame.mouse.get_pos()
            column = position[0] // (WIDTH + MARGIN)
            row = position[1] // (HEIGHT + MARGIN)
            if grid_copy[row][column] != 0:
                pass
            else:
                clicked_grid[row][column] = 1
        # un-highlights the box
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:

            position = pygame.mouse.get_pos()
            column = position[0] // (WIDTH + MARGIN)
            row = position[1] // (HEIGHT + MARGIN)

            clicked_grid[row][column] = 0

        # automatically solves the puzzle
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_grid()
            draw()
            solve(grid)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            # reset clicked_grid
            for row in range(9):
                for column in range(9):
                    clicked_grid[row][column] = 0
    screen.fill((0, 0, 0))
    color = (177, 205, 205)
    for row in range(9):
        for column in range(9):
            if clicked_grid[row][column] == 1:
                color = (0, 255, 0)

            elif clicked_grid[row][column] == 2:
                color = (255, 0, 0)
            pygame.draw.rect(
                screen, color,
                [(MARGIN + WIDTH) * column + MARGIN,
                 (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
            color = (177, 205, 205)

            # render text
            if grid[row][column] == 0:
                txt = ""
            else:
                txt = str(grid_copy[row][column])

            label = my_font.render("{}".format(txt), 1, (0, 0, 0))
            screen.blit(label, ((MARGIN + WIDTH) * column + MARGIN + 10,
                                (MARGIN + HEIGHT) * row + MARGIN + 10))
    offset = 0
    for i in range(3):
        pygame.draw.rect(screen, (51, 153, 102),
                         pygame.Rect((0, (i + 1) * 108.3 - offset, 325, 5)))
        offset += 5

    offset = 0
    for i in range(3):
        pygame.draw.rect(screen, (51, 153, 102),
                         pygame.Rect(((i + 1) * 108.3 - offset, 0, 5, 325)))
        offset += 5
    pygame.display.flip()


draw()
clock.tick(60)  # Limit the frame rate to 60 FPS.

pygame.quit()
