# Anti Scam Bot

This is a bot that will post "Scam" on new posts for a given user. It's intended to be used to help warn people of scams.

# Setup

Before you can run this bot you need to supply 3 things. `PUBLIC_KEY`, `DERIVED_PUBLIC_KEY`, and `PUBLIC_SEED_HEX`.
```
PUBLIC_KEY = "public key here"
DERIVED_PUBLIC_KEY = "derived public key"
DERIVED_SEED_HEX = "derived seed hex"
```

You can get the derived key and seed from `diamondapp.com`.

You will also need to add users to the database. The following shows the syntax used.

```
[
    {
        "public key of target": "last post hex hash"
    }
]
```

# Running

To run this bot you can type the following into a terminal
```
python3 bot.py
```
