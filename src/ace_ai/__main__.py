import sys

from .tools import Tools

def main() -> None:
    print(Tools.get_player_stats(sys.argv[2], sys.argv[1]))

if __name__ == "__main__":
    main()