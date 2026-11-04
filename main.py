import sys
import config-parser

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("enter a filename to your program fits well")
        sys.exit(1)
    filename:str = sys.argv[1]
    config = parse_config(filename)
