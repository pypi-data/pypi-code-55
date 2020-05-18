#!/usr/bin/env python3

import os
import random

around = os.listdir()
if 'gameofcard' in around:
    import gameofcard.gameobject
    go = gameofcard.gameobject
elif 'gameobject' in around:
    import gameobject
    go = gameobject
else:
    import gameobject
    go = gameobject

if __name__ == '__main__':
    # random.seed(1)
    game = go.BriscolaGame(
        [go.BriscolaPlayer("East"),
         go.BriscolaPlayer("North"),
         go.BriscolaPlayer("West"),
         go.BriscolaPlayer("Me", False)
         ])
