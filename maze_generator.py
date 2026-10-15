class MazeGenerator:
    """Creates the base structure for a maze and validates cell access."""

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL_WALLS = NORTH | EAST | SOUTH | WEST

    def __init__(self, width: int, height: int) -> None:
        """Initialize the maze with width, height, and all walls closed."""
        self.width = width
        self.height = height

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