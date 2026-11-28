"""Terminal renderer for bitmask-based maze grids using Unicode box-drawing."""
from maze_config import MazeConfig


class TerminalRenderer:
    """Render a bitmask-based maze grid in the terminal."""

    NORTH: int = 1
    EAST: int = 2
    SOUTH: int = 4
    WEST: int = 8

    EMPTY_CELL: str = "   "
    ENTRY_SYMBOL: str = " E "
    EXIT_SYMBOL: str = " X "

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

    def __init__(self, maze: list[list[int]], maze_config: MazeConfig) -> None:
        """Initialize the renderer with a maze grid and its configuration.

        Args:
            maze: 2D list of integers where each cell encodes its walls
                using bits: NORTH=1, EAST=2, SOUTH=4, WEST=8.
            maze_config: Validated maze configuration containing dimensions,
                entry, and exit coordinates.

        Raises:
            ValueError: If maze dimensions do not match maze_config.
        """
        if len(maze) != maze_config.height or any(
            len(row) != maze_config.width for row in maze
        ):
            raise ValueError(
                "Maze grid dimensions do not match maze_config."
            )

        self.maze = maze
        self.height = maze_config.height
        self.width = maze_config.width
        self.entry: tuple[int, int] = maze_config.entry
        self.exit: tuple[int, int] = maze_config.exit

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
        if (x, y) == self.entry:
            return self.ENTRY_SYMBOL
        if (x, y) == self.exit:
            return self.EXIT_SYMBOL
        return self.EMPTY_CELL

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
    from maze_generator import MazeGenerator

    maze_config = MazeConfig(10, 10, (0, 0), (4, 4), "output.txt", True)
    generator = MazeGenerator(
        maze_config.width, maze_config.height, seed=maze_config.seed
    )
    generator.generate()
    renderer = TerminalRenderer(generator.grid, maze_config)
    renderer.display()
