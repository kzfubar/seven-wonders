from networking.client.WondersClient import WondersClient

import sys

if __name__ == "__main__":
    print("Launching WondersClient...")
    client = WondersClient()
    if len(sys.argv) > 2:
        client.start(sys.argv[1], sys.argv[2])
    else:
        client.start()
