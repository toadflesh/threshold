import threshold
import sys

def main():
    val = threshold.init(sys.argv)
    if val == "error":
        print("ERROR: not enough args\nUSAGE: uv run main.py <txid>")
        sys.exit(1)
    elif val == "tx len error":
        print("ERROR: invalid txid\nUSAGE: uv run main.py <txid>")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
