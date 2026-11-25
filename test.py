import sys

from maze_config import ConfigError, MazeConfig

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("enter a filename to your program fits well")
        sys.exit(1)
    filename: str = sys.argv[1]
    try:
        config = MazeConfig.from_file(filename)
        print(f"Config loaded successfully: {config}")
    except ConfigError as e:
        print(f"Error: {e}")
        sys.exit(1)
