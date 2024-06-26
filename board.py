import pygame
import logging
from settings import CELL_SIZE, CELL_SIZE2, BLACK, BLUE, RED

class Board:
    def __init__(self, size, show_ships=True):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.show_ships = show_ships
        self.row_labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        self.column_labels = [str(i + 1) for i in range(size)]

    def add_ship(self, ship):
        self.ships.append(ship)
        self.update_grid_with_ship(ship)

    def update_grid_with_ship(self, ship):
        for position in ship.get_occupied_positions():
            x, y = position
            x_num = int(x) - 1
            y_num = ord(y.upper()) - 65
            if 0 <= x_num < self.size and 0 <= y_num < self.size:
                self.grid[y_num][x_num] = ship.name

    def all_ships_within_bounds(self):
        out_of_bounds_ships = []
        all_within_bounds = True
        for ship in self.ships:
            for x, y in ship.get_occupied_positions():
                x_num = int(x) - 1
                y_num = ord(y) - 65
                if x_num < 0 or x_num >= self.size or y_num < 0 or y_num >= self.size:
                    out_of_bounds_ships.append(ship.name)
                    all_within_bounds = False
                    break
        return all_within_bounds, out_of_bounds_ships

    def check_for_overlaps(self):
        position_count = {}
        overlapping_ships = []
        for ship in self.ships:
            for position in ship.get_occupied_positions():
                if position in position_count:
                    position_count[position].append(ship.name)
                else:
                    position_count[position] = [ship.name]

        for positions, ships in position_count.items():
            if len(ships) > 1:
                overlapping_ships.extend(ships)

        return list(set(overlapping_ships))

    def draw(self, screen, cell_size, offset=(0, 0), title="Player Board"):
        font = pygame.font.SysFont(None, 36)

        title_surface = font.render(title, True, BLACK)
        title_width, title_height = title_surface.get_size()
        grid_width = self.size * cell_size

        title_x = offset[0] + (grid_width - title_width) // 2
        title_y = offset[1] - title_height - 50

        screen.blit(title_surface, (title_x, title_y))

        for i, label in enumerate(self.row_labels):
            label_surface = font.render(label, True, BLACK)
            label_width, _ = label_surface.get_size()

            screen.blit(label_surface, (offset[0] - label_width - 10, offset[1] + i * cell_size + (cell_size // 2 - font.get_height() // 2)))

        for i, label in enumerate(self.column_labels):
            label_surface = font.render(label, True, BLACK)
            _, label_height = label_surface.get_size()

            screen.blit(label_surface, (offset[0] + i * cell_size + (cell_size // 2 - label_surface.get_width() // 2), offset[1] - label_height - 10))

        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(offset[0] + x * cell_size, offset[1] + y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, BLACK, rect, 1)

                if self.grid[y][x] == 'X':
                    pygame.draw.rect(screen, RED, rect)
                elif self.grid[y][x] == 'O':
                    pygame.draw.rect(screen, BLUE, rect)

        if self.show_ships:
            for ship in self.ships:
                ship.draw(screen)

    def check_game_over(self):
        for row in self.grid:
            for cell in row:
                if isinstance(cell, str) and cell not in ['X', 'O']:
                    return False
        return True
