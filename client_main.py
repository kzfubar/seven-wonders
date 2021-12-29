from client.WondersClient import WondersClient

import sys

if __name__ == "__main__":
    print("Launching WondersClient...")
    WondersClient().start(sys.argv[1], sys.argv[2])
