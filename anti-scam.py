import os
import signal
import sys
import time
import jsonc
import deso
from datetime import datetime

PUBLIC_KEY = 'PUBLIC_KEY_HERE'
DERIVED_SEED_HEX = 'DERIVED_SEED_HEX'
DERIVED_PUBLIC_KEY = 'DERIVED_PUBLIC_KEY'

desoPosts = deso.Posts()
desoUser = deso.User(nodeURL="https://node.deso.com/api/v0/", readerPublicKey=PUBLIC_KEY)

BODY = "Scam"

# load our json database
with open('database.json', 'r') as file:
    scammers = jsonc.load(file)

# Handle any cleanup here
def handler(signal_received, frame):
    with open('database.json', 'w') as file:
        jsonc.dump(scammers, file, indent=4)
    print("Saving json database")
    sys.exit(0)

# Register the handler for SIGINT
if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    os.system("cls")
    print('Running. Press Ctrl+C to exit.')
    print("Searching for scam posts ...")

try:
    while True:
        for scammer in scammers:
            for key, value in scammer.items():
                if value != "" and 1 == 1: # ignore if post is hidden
                    POST_HASH_HEX = desoPosts.getPostsForPublicKey(publicKey=key, numToFetch=1).json()["Posts"][0]["PostHashHex"]
                    LAST_POST_HASH_HEX = value

                    if POST_HASH_HEX != LAST_POST_HASH_HEX:
                        desoSocial = deso.Social(publicKey=PUBLIC_KEY, derivedPublicKey=DERIVED_PUBLIC_KEY, derivedSeedHex=DERIVED_SEED_HEX)
                        res = desoSocial.submitPost(parentStakeID=POST_HASH_HEX, body=BODY, isHidden=False)
                        print(f"{datetime.now().strftime('%H:%M:%S %p')} Scam found @ PostHexHash: {POST_HASH_HEX}")
                        scammer[key] = POST_HASH_HEX
        time.sleep(5)
        pass # not sure
# not sure
except KeyboardInterrupt:
    print('KeyboardInterrupt caught. Exiting...')

