SCALE = 0.5

SCREEN_CORRECTION = 1.82
SCREEN_SIZE = (550, 550)
SCREEN_SIZE_CORRECTED = ((SCREEN_SIZE[0] * SCREEN_CORRECTION, SCREEN_SIZE[1] * SCREEN_CORRECTION))

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


