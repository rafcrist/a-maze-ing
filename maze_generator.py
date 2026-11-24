import random


class MazeGenerator:
    """Creates the base structure for a maze and validates cell access."""

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL_WALLS = NORTH | EAST | SOUTH | WEST

    def __init__(self, width: int, height: int,
                 seed: int | None = None) -> None:
        """Initialize the maze with width, height, and all walls closed."""
        self.width = width
        self.height = height
        self.rng = random.Random(seed)

        self.grid: list[list[int]] = []
        for _ in range(self.height):
            line = [self.ALL_WALLS] * self.width
            self.grid.append(line)

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if the given position is inside the maze."""
        if (x >= 0 and x < self.width and y >= 0 and y < self.height):
            return (True)
        return (False)

    def get_cell(self, x: int, y: int) -> int:
        """Return the cell if the position is valid,
        or raise an error otherwise."""
        if (self.is_valid_position(x, y)):
            cell = self.grid[y][x]
            return (cell)
        raise ValueError("Invalid cell.")

    def has_wall(self, x: int, y: int, wall: int) -> bool:
        """Verify whether a specific wall exists in the cell."""
        cell = self.get_cell(x, y)
        result = cell & wall
        if (result):
            return (True)
        return (False)

    def remove_wall(self, x: int, y: int, wall: int) -> None:
        if not (self.is_valid_position(x, y)):
            return
        if wall == self.NORTH and y == 0:
            return
        if wall == self.SOUTH and y == self.height - 1:
            return
        if wall == self.WEST and x == 0:
            return
        if wall == self.EAST and x == self.width - 1:
            return
        cell = self.get_cell(x, y)
        cell = cell & ~wall
        self.grid[y][x] = cell

        if (wall == self.EAST):
            nx = x + 1
            ny = y
            if (self.is_valid_position(nx, ny)):
                self.grid[ny][nx] = self.grid[ny][nx] & ~self.WEST

        elif (wall == self.WEST):
            nx = x - 1
            ny = y
            if (self.is_valid_position(nx, ny)):
                self.grid[ny][nx] = self.grid[ny][nx] & ~self.EAST

        elif (wall == self.NORTH):
            nx = x
            ny = y - 1
            if (self.is_valid_position(nx, ny)):
                self.grid[ny][nx] = self.grid[ny][nx] & ~self.SOUTH

        elif (wall == self.SOUTH):
            nx = x
            ny = y + 1
            if (self.is_valid_position(nx, ny)):
                self.grid[ny][nx] = self.grid[ny][nx] & ~self.NORTH

    def generate(self) -> None:
        visited = {(0, 0)}
        stack = [(0, 0)]

        while (stack):
            x, y = stack[-1]
            neighbors = []

            # East
            nx = x + 1
            ny = y
            if (self.is_valid_position(nx, ny)
               and (nx, ny) not in visited):
                neighbors.append((nx, ny))

            # West
            nx = x - 1
            ny = y
            if (self.is_valid_position(nx, ny)
               and (nx, ny) not in visited):
                neighbors.append((nx, ny))

            # North
            nx = x
            ny = y - 1
            if (self.is_valid_position(nx, ny)
               and (nx, ny) not in visited):
                neighbors.append((nx, ny))

            # South
            nx = x
            ny = y + 1
            if (self.is_valid_position(nx, ny)
               and (nx, ny) not in visited):
                neighbors.append((nx, ny))

            if (neighbors):
                next_cell = self.rng.choice(neighbors)
                nx, ny = next_cell
                visited.add(next_cell)
                stack.append(next_cell)
                if (nx == x + 1):
                    self.remove_wall(x, y, self.EAST)
                elif (nx == x - 1):
                    self.remove_wall(x, y, self.WEST)
                elif (ny == y + 1):
                    self.remove_wall(x, y, self.SOUTH)
                elif (ny == y - 1):
                    self.remove_wall(x, y, self.NORTH)
            else:
                stack.pop()

    def encode_cell(self, x: int, y: int) -> str:
        """Encode a cell's wall bitmask as one hexadecimal digit."""
        return (format(self.get_cell(x, y), "X"))

    def encode_hex_grid(self) -> list[str]:
        """Encode the full maze grid as hexadecimal rows."""
        rows: list[str] = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                row += self.encode_cell(x, y)
            rows.append(row)
        return (rows)

    def display(self) -> None:
        """Display the maze using ASCII characters."""
        for y in range(self.height):
            top = ""
            for x in range(self.width):
                if self.has_wall(x, y, self.NORTH):
                    top += "+---"
                else:
                    top += "+   "
            print(top + "+")

            side = ""
            for x in range(self.width):
                if self.has_wall(x, y, self.WEST):
                    side += "|   "
                else:
                    side += "    "

            print(side + "|")
        print("+" + "---+" * self.width)


if __name__ == "__main__":
    maze = MazeGenerator(10, 10, seed=100)
    maze.generate()
    maze.display()
