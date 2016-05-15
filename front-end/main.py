import sfml as sf
import random
from tile import *
from enum import *
import time
import os
import math
import constants as const
from settlement import *

from track_talker import TrackTalker

class GameState(Enum):
    WAIT_CALIBRATE = 0
    CALIBRATE = 1
    RUN_GAME = 2
    DO_TURN = 3
    

def read_camera_result():
    result = []

    with open("/tmp/stlrs_coords") as f:
        lines = f.readlines();

        for line in lines:
            line=line.replace("[", "");
            line=line.replace("]", "");
            line=line.replace(" ", "");

            coords = line.split(",");
            
            result.append(sf.Vector2(float(coords[0]), float(coords[1])))
    return result

def calibrate():
    global game_state
    global camera_offset

    CONST_CAMERA_OFFSET = sf.Vector2(100, 100)

    if time.time() > camera_wait_start + 2: #Find the offset of the pieces
        if len(coords) != 0:
            smallest_distance = 1000000000000
            smallest_coord = coords[0]
            #Find the top left corner
            for coord in coords:
                distance = math.sqrt(coord.x**2 + coord.y**2)
                if distance < smallest_distance:
                    smallest_distance = distance
                    smallest_coord = coord

            camera_offset = smallest_coord -CONST_CAMERA_OFFSET

        game_state = GameState.RUN_GAME
    elif time.time() > camera_wait_start + 1: #Let the tracker do some matrix magick
        #Do calibration stuff
        TrackTalker.tell_calibrate();
        #game_state = GameState.RUN_GAME

    white_sprite = sf.Sprite(std_texture);
    white_sprite.scale(const.SCREEN_SIZE_CORRECTED)
    window.draw(white_sprite)

def get_closest_tiles(target, num):
    global tile

    sorted = []
    for y in tiles:
        for tile in y:
            if tile:
                distance = math.sqrt((target.x - tile.get_world_pos()[0])**2 + (target.y - tile.get_world_pos()[1])**2)
                sorted.append((tile, distance))

    sorted.sort(key=lambda tup: tup[1])

    result = []
    if len(sorted) < num:
        result = sorted
    result = sorted[0:num]

    #print(result)
    return ([x for (x, _) in result], [x for (_, x) in result])


camera_offset = sf.Vector2(0,0)

# create the main window
window = sf.RenderWindow(sf.VideoMode(const.SCREEN_SIZE[0], const.SCREEN_SIZE[1]), "PySFML")

tiles = []
shuf_tiles = list(const.TILE_RATIO)
random.shuffle(shuf_tiles)
for y in range(0,7):
    tiles.append([])
    for x in range(0,6):
        tiles[y].append(None)

for c in const.VALID_COORDINATES:
    tile_texture = const.TYPES[shuf_tiles.pop()]
    tiles[c[0]][c[1]] = tile(1, tile_texture, c)

std_texture = sf.Texture.from_file("media/1x1.png")

calibrationTexture = sf.Texture.from_file("media/Calibration.png")
calibrationSprite = sf.Sprite(calibrationTexture);
calibrationSprite.scale((const.SCREEN_CORRECTION, const.SCREEN_CORRECTION))

game_state = GameState.WAIT_CALIBRATE

calibratePressed = False;

camera_wait_start = 0

TrackTalker.tell_restart();

coords=[]

settlements = []

# start the game loop
while window.is_open:
    # process events
    for event in window.events:
        # close window: exit
        if type(event) is sf.CloseEvent:
            window.close()

        if type(event) is sf.ResizeEvent:
            window.size = (const.SCREEN_SIZE)

    window.clear() # clear screen
    for y in tiles:
        for x in y:
            if x:
                x.draw(window);

    coords = read_camera_result()[1:];
    corrected_coords = []

    pawn_sprites = []

    
    for coord in coords:
        x = (coord.x ) * const.SCREEN_CORRECTION
        y = (coord.y ) * const.SCREEN_CORRECTION

        new_vec = sf.Vector2(x,y) - camera_offset
        corrected_coords.append(new_vec)

        test_sprite = sf.Sprite(std_texture)
        test_sprite.scale((20, 20))
        test_sprite.position =  new_vec
        test_sprite.color = sf.Color(150,150,150)

        pawn_sprites.append(test_sprite)
    


    if game_state == GameState.WAIT_CALIBRATE:
        window.draw(calibrationSprite);

        if sf.Keyboard.is_key_pressed(sf.Keyboard.RETURN):
            camera_wait_start = time.time();
            game_state = GameState.CALIBRATE

    elif game_state == GameState.CALIBRATE:
        calibrate()
    elif game_state == GameState.RUN_GAME:
        if sf.Keyboard.is_key_pressed(sf.Keyboard.RETURN) and window.has_focus():
            game_state = GameState.DO_TURN
            camera_wait_start = time.time()

    elif game_state == GameState.DO_TURN:
        if time.time() > camera_wait_start + 1:
            if len(corrected_coords) != 0:
                (closest_tiles, distances) = get_closest_tiles(corrected_coords[0], 3)
                
                is_corner = True
                is_road = False

                for d in distances:
                    if abs(d - const.RADIUS) > const.RADIUS * 0.1:
                        is_corner = False

                if not is_corner:
                    is_road = True
                    for d in distances[0:2]:
                        ROAD_DISTANCE = const.RADIUS * math.cos(math.pi/6)
                        if abs(d - ROAD_DISTANCE) > ROAD_DISTANCE * 0.1:
                            is_road = False

                if is_road:
                    print("Piece is road")
                elif is_corner:
                    print("Piece is settlement")

                    settlements.append(Settlement(closest_tiles))

                game_state = GameState.RUN_GAME


        else:
            white_sprite = sf.Sprite(std_texture);
            white_sprite.scale(const.SCREEN_SIZE_CORRECTED)
            window.draw(white_sprite)



        
    for sprite in pawn_sprites:
        window.draw(sprite)

    for settlement in settlements:
        settlement.draw(window)

    window.display() # update the window

