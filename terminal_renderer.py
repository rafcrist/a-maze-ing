"""Terminal renderer for bitmask-based maze grids using Unicode box-drawing."""


class TerminalRenderer:
    """Render a bitmask-based maze grid in the terminal."""

    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8

    # Vertex bitmask: UP=1, RIGHT=2, DOWN=4, LEFT=8
    CORNERS: dict[int, str] = {
        0: " ",
        1: "╵",
        2: "╶",
        3: "└",
        4: "╷",
        5: "│",
        6: "┌",
        7: "├",
        8: "╴",
        9: "┘",
        10: "─",
        11: "┴",
        12: "┐",
        13: "┤",
        14: "┬",
        15: "┼",
    }

    def __init__(self, maze: list[list[int]]) -> None:
        """Initialize the renderer with a 2D matrix of wall bitmasks.

        Args:
            maze: 2D list of integers where each cell encodes its walls
                using bits: NORTH=1, EAST=2, SOUTH=4, WEST=8.

        Raises:
            ValueError: If maze rows do not all have the same width.
        """
        if maze:
            expected_width = len(maze[0])
            for row in maze:
                if len(row) != expected_width:
                    raise ValueError("All maze rows must have the same width.")
            self.width = expected_width
        else:
            self.width = 0

        self.maze = maze
        self.height = len(maze)

    def _has_wall(self, x: int, y: int, wall: int) -> bool:
        """Return whether the cell at (x, y) has the specified wall."""
        return bool(self.maze[y][x] & wall)

    def _has_horizontal_wall(self, x: int, vy: int) -> bool:
        """Check if a horizontal wall exists at column x and vertex row vy."""
        if vy == 0:
            return self._has_wall(x, 0, self.NORTH)
        if vy == self.height:
            return self._has_wall(x, self.height - 1, self.SOUTH)
        return (
            self._has_wall(x, vy, self.NORTH)
            or self._has_wall(x, vy - 1, self.SOUTH)
        )

    def _has_vertical_wall(self, vx: int, y: int) -> bool:
        """Check if a vertical wall exists at vertex column vx and row y."""
        if vx == 0:
            return self._has_wall(0, y, self.WEST)
        if vx == self.width:
            return self._has_wall(self.width - 1, y, self.EAST)
        return (
            self._has_wall(vx, y, self.WEST)
            or self._has_wall(vx - 1, y, self.EAST)
        )

    def _get_corner(self, vx: int, vy: int) -> str:
        """Return the Unicode box-drawing character for vertex (vx, vy)."""
        mask = 0
        if vy > 0 and self._has_vertical_wall(vx, vy - 1):
            mask |= 1  # UP
        if vx < self.width and self._has_horizontal_wall(vx, vy):
            mask |= 2  # RIGHT
        if vy < self.height and self._has_vertical_wall(vx, vy):
            mask |= 4  # DOWN
        if vx > 0 and self._has_horizontal_wall(vx - 1, vy):
            mask |= 8  # LEFT
        return self.CORNERS[mask]

    def _cell_content(self, x: int, y: int) -> str:
        """Return the 3-character interior content of the cell at (x, y)."""
        return "   "

    def _render_horizontal_border(self, vy: int) -> str:
        """Build a horizontal border line for vertex row vy."""
        parts: list[str] = []
        for x in range(self.width):
            parts.append(self._get_corner(x, vy))
            parts.append(
                "───" if self._has_horizontal_wall(x, vy) else "   "
            )
        parts.append(self._get_corner(self.width, vy))
        return "".join(parts)

    def _render_cell_row(self, y: int) -> str:
        """Build a cell interior row with vertical walls for row y."""
        parts: list[str] = []
        for x in range(self.width):
            parts.append("│" if self._has_vertical_wall(x, y) else " ")
            parts.append(self._cell_content(x, y))
        parts.append("│" if self._has_vertical_wall(self.width, y) else " ")
        return "".join(parts)

    def render(self) -> str:
        """Build and return the full Unicode representation of the maze."""
        if self.height == 0 or self.width == 0:
            return ""

        lines: list[str] = []
        for y in range(self.height):
            lines.append(self._render_horizontal_border(y))
            lines.append(self._render_cell_row(y))
        lines.append(self._render_horizontal_border(self.height))
        return "\n".join(lines)

    def display(self) -> None:
        """Print the rendered maze to the terminal."""
        print(self.render())


if __name__ == "__main__":
    # Fake 3x3 maze for standalone testing (independent of MazeGenerator):
    # NORTH=1, EAST=2, SOUTH=4, WEST=8
    fake_maze: list[list[int]] = [
        [13, 1, 3],
        [9, 6, 10],
        [12, 5, 6],
    ]
    renderer = TerminalRenderer(fake_maze)
    renderer.display()
