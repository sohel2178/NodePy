import sys
import json
import numpy as np

def main():
    y = json.loads(sys.argv[1])
    print(y)


if __name__ == '__main__':
    main()