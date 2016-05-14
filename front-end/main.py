import sfml as sf
import random
from tile import *


STONE, CLAY, WHEAT, WOOL, WOOD, DESERT = range(0,6)
TYPES = {STONE: 'media/stone.png', 
    CLAY: 'media/clay.png', 
    WHEAT: 'media/wheat.png', 
    WOOL: 'media/wool.png',
    WOOD: 'media/wood.png',
    DESERT: 'media/desert.png'}

TILE_RATIO = [STONE, STONE, STONE,
        CLAY, CLAY, CLAY,
        WHEAT, WHEAT, WHEAT, WHEAT,
        WOOL, WOOL, WOOL, WOOL,
        WOOD, WOOD, WOOD, WOOD,
        DESERT]

VALID_COORDINATES = [(1, 0), (2, 0), (3, 0),
        (0, 1), (1, 1), (2, 1), (3, 1),
        (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
        (0, 3), (1, 3), (2, 3), (3, 3),
        (1, 4), (2, 4), (3, 4)]
        

# create the main window
window = sf.RenderWindow(sf.VideoMode(640, 480), "pySFML Window")

tiles = []
shuf_tiles = list(TILE_RATIO)
random.shuffle(shuf_tiles)
for y in range(0,7):
    tiles.append([])
    for x in range(0,6):
        tiles[y].append(None)

for c in VALID_COORDINATES:
    tile_texture = TYPES[shuf_tiles.pop()]
    print(shuf_tiles)
    print(tiles)
    print(c)
    tiles[c[0]][c[1]] = tile(1, tile_texture, c)


# start the game loop
while window.is_open:
    # process events
    for event in window.events:
        # close window: exit
        if type(event) is sf.CloseEvent:
            window.close()
           
    window.clear() # clear screen
    for y in tiles:
        for x in y:
            if x:
                print(x)
                x.draw(window);
    window.display() # update the window
