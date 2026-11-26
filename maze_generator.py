import random
import sys
from collections import deque


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

        self.pattern_cells = self.create_42_pattern()

    def create_42_pattern(self) -> set[tuple[int, int]]:
        """Return the centered coordinates of the closed 42 cells."""
        mask = (
            "#.#.###",
            "#.#...#",
            "###.###",
            "..#.#..",
            "..#.###",
        )
        pattern_width = len(mask[0])
        pattern_height = len(mask)
        if (self.width < pattern_width + 2
                or self.height < pattern_height + 2):
            return (set())

        start_x = self.width // 2 - pattern_width // 2
        start_y = self.height // 2 - pattern_height // 2
        cells: set[tuple[int, int]] = set()
        for y, row in enumerate(mask):
            for x, char in enumerate(row):
                if (char == "#"):
                    cells.add((start_x + x, start_y + y))
        return (cells)

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
        offsets = {
            self.NORTH: (0, -1),
            self.EAST: (1, 0),
            self.SOUTH: (0, 1),
            self.WEST: (-1, 0),
        }
        if (wall not in offsets):
            return
        dx, dy = offsets[wall]
        if ((x, y) in self.pattern_cells
                or (x + dx, y + dy) in self.pattern_cells):
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
        if (not self.pattern_cells):
            print("Error: maze too small for the 42 pattern.",
                  file=sys.stderr)

        visited = {(0, 0)}
        visited.update(self.pattern_cells)
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

    def write_output_file(
        self,
        filename: str,
        entry: tuple[int, int],
        exit: tuple[int, int],
        path: list[str],
    ) -> None:
        """Write maze data using the required output format."""
        with open(filename, "w", encoding="utf-8") as output:
            for row in self.encode_hex_grid():
                output.write(row + "\n")
            output.write("\n")
            output.write(f"{entry[0]},{entry[1]}\n")
            output.write(f"{exit[0]},{exit[1]}\n")
            output.write(" ".join(path) + "\n")

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

    def solve(self, entry: tuple[int, int],
              exit: tuple[int, int]) -> list[str]:
        directions = [
            (0, -1, self.NORTH),
            (1, 0, self.EAST),
            (0, 1, self.SOUTH),
            (-1, 0, self.WEST)
        ]
        queue = deque([entry])
        visited = {entry}
        parents: dict[tuple[int, int], tuple[int, int]] = {}
        while (queue):
            x, y = queue.popleft()
            if ((x, y) == exit):
                break
            for dx, dy, wall in directions:
                nx = x + dx
                ny = y + dy
                if (self.is_valid_position(nx, ny)
                        and not self.has_wall(x, y, wall)
                        and (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                    parents[(nx, ny)] = x, y
        if not (exit in visited):
            return ([])

        path: list[str] = []
        current = exit
        while (current != entry):
            previous = parents[current]

            cx, cy = current
            px, py = previous

            dx = cx - px
            dy = cy - py
            if (dy == -1):
                path.append("N")
            elif (dy == 1):
                path.append("S")
            elif (dx == -1):
                path.append("W")
            elif (dx == 1):
                path.append("E")
            current = previous
        path.reverse()
        return (path)


if __name__ == "__main__":
    maze = MazeGenerator(5, 5, seed=100)
    maze.generate()
    maze.display()

    path = maze.solve((0, 0), (4, 4))

    print("Shortest path:", path)
    print("Total moves:", len(path))

    print(maze.solve((0, 0), (0, 0)))
    print(maze.solve((0, 0), (1, 0)))
    print(maze.solve((4, 4), (0, 0)))

    closed_maze = MazeGenerator(5, 5)
    print(closed_maze.solve((0, 0), (4, 4)))
