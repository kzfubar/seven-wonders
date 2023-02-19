from networking.client.WondersClient import WondersClient

import sys

if __name__ == "__main__":
    print("Launching WondersClient...")
    client = WondersClient()
    if len(sys.argv) > 1:
        client.start(sys.argv[1], None)  # fixme remove none
    else:
        client.start()
