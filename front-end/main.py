import sfml as sf
import random
from tile import *
from enum import *
import time
import os

from track_talker import TrackTalker

class GameState(Enum):
    WAIT_CALIBRATE = 0
    CALIBRATE = 1
    START_GAME = 2
    

def read_camera_result():
    result = []

    with open("/tmp/stlrs_coords") as f:
        lines = f.readlines();

        for line in lines:
            line=line.replace("[", "");
            line=line.replace("]", "");
            line=line.replace(" ", "");

            coords = line.split(",");
            
            result.append((float(coords[0]), float(coords[1])))
    return result


SCREEN_SIZE = (550,550)
SCREEN_SIZE_CORRECTED = ((SCREEN_SIZE[0] * 1.82, SCREEN_SIZE[1] * 1.82))

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
window = sf.RenderWindow(sf.VideoMode(SCREEN_SIZE[0], SCREEN_SIZE[1]), "PySFML")

tiles = []
shuf_tiles = list(TILE_RATIO)
random.shuffle(shuf_tiles)
for y in range(0,7):
    tiles.append([])
    for x in range(0,6):
        tiles[y].append(None)

for c in VALID_COORDINATES:
    tile_texture = TYPES[shuf_tiles.pop()]
    tiles[c[0]][c[1]] = tile(1, tile_texture, c)

std_texture = sf.Texture.from_file("media/1x1.png")

calibrationTexture = sf.Texture.from_file("media/Calibration.png")
calibrationSprite = sf.Sprite(calibrationTexture);
calibrationSprite.scale((1.82,1.82))

state = GameState.WAIT_CALIBRATE

calibratePressed = False;

img_cal_start = 0

TrackTalker.tell_restart();

# start the game loop
while window.is_open:
    # process events
    for event in window.events:
        # close window: exit
        if type(event) is sf.CloseEvent:
            window.close()

        if type(event) is sf.ResizeEvent:
            window.size = SCREEN_SIZE

    window.clear() # clear screen
    for y in tiles:
        for x in y:
            if x:
                x.draw(window);

    coords = read_camera_result()[1:];


    if state == GameState.WAIT_CALIBRATE:
        window.draw(calibrationSprite);

        if sf.Keyboard.is_key_pressed(sf.Keyboard.RETURN) and window.has_focus():
            img_cal_start = time.time();
            state = GameState.CALIBRATE

    elif state == GameState.CALIBRATE:
        if time.time() > img_cal_start + 1:
            #Do calibration stuff
            TrackTalker.tell_calibrate();
            state = GameState.START_GAME
        else:
            white_sprite = sf.Sprite(std_texture);
            white_sprite.scale(SCREEN_SIZE_CORRECTED)
            window.draw(white_sprite)
    elif state == GameState.START_GAME:
        if sf.Keyboard.is_key_pressed(sf.Keyboard.RETURN) and window.has_focus():
            white_sprite = sf.Sprite(std_texture);
            white_sprite.scale(SCREEN_SIZE_CORRECTED)
            window.draw(white_sprite)


        
        

    window.display() # update the window
