#! /usr/local/bin/python3

from datetime import datetime
import requests
import os
import signal
import sys
import time
import json
import deso

NODE_URL = "https://node.deso.org/api/v0/"
PUBLIC_KEY = ""
DERIVED_SEED_HEX = ""
DERIVED_PUBLIC_KEY = ""
BODY = "Scam"

# load our json database
os.system("cls")
print("Loading json database\033[K")
with open('database.json', 'r') as file:
    scammers = json.load(file)

# Handle any cleanup here
def handler(signal_received, frame):
    with open('database.json', 'w') as file:
        json.dump(scammers, file, indent=4)
    print("Saving json database\033[K")
    sys.exit(0)

# Register the handler for SIGINT
if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

def getFollowers(numToFetch = 999):
    global FOLLOWERS
    api = f"{NODE_URL}get-follows-stateless"
    data = {
        "PublicKeyBase58Check": PUBLIC_KEY,
        "NumToFetch": numToFetch # how do we do all ?
    }
    return requests.post(api, json=data).json()["PublicKeyToProfileEntry"]

try:
    print(f"Searching \033[32m{len(scammers)}\033[0m users for scam posts.")
    desoPosts = deso.Posts(nodeURL=NODE_URL)
    while True:
        for scammer in scammers:
            for key, value in scammer.items():
                if value != "" and 1 == 1: # ignore if post is hidden
                    try:
                        POST_HASH_HEX = desoPosts.getPostsForPublicKey(publicKey=key, numToFetch=1).json()["Posts"][0]["PostHashHex"]
                        LAST_POST_HASH_HEX = value
                        if POST_HASH_HEX != LAST_POST_HASH_HEX:
                            try:
                                desoSocial = deso.Social(publicKey=PUBLIC_KEY, derivedPublicKey=DERIVED_PUBLIC_KEY, derivedSeedHex=DERIVED_SEED_HEX)
                                res = desoSocial.submitPost(parentStakeID=POST_HASH_HEX, body=BODY, isHidden=False)
                                print(f"\033[94m[{datetime.now().strftime('%H:%M:%S %p')}]\033[0m {POST_HASH_HEX}\033[K")
                                scammer[key] = POST_HASH_HEX
                            except Exception as e:
                                print(f"\033[37;41m{e}\033[0m\033[K")
                    except Exception as e:
                        print(f"\033[37;41m{e}\033[0m\033[K")
                        continue
        print("\033[?25lRunning. Press Ctrl+C to exit.\033[K", end="\r")
        time.sleep(2)
except KeyboardInterrupt:
    print('KeyboardInterrupt caught. Exiting...')
