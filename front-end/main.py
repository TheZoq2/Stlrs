import sfml as sf
import random
from tile import *
from road import *
from enum import *
import time
import os
import math
import constants as const

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
            
            result.append(sf.Vector2(float(coords[0]), float(coords[1])))
    return result

def calibrate():
    global game_state
    global camera_offset

    CONST_CAMERA_OFFSET = sf.Vector2(100, 100)

    if time.time() > img_cal_start + 2: #Find the offset of the pieces
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

        game_state = GameState.START_GAME
    elif time.time() > img_cal_start + 1: #Let the tracker do some matrix magick
        #Do calibration stuff
        TrackTalker.tell_calibrate();
        #game_state = GameState.START_GAME

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

    return [x for (x, _) in result]
    #return []

#def get_closest_tiles(target, num):
#    closest_tile = tiles[0];
#    lowest_distance = 10000000000000000
#
#    for y in tiles:
#        for tile in y:
#            if tile:
#                distance = math.sqrt((target.x - tile.get_world_pos()[0])**2 + (target.y - tile.get_world_pos()[1])**2)
#
#                if distance < lowest_distance:
#                    lowest_distance = distance
#                    closest_tile = tile
#    
#    return closest_tile

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

r = road((tiles[2][1], tiles[1][1]))

std_texture = sf.Texture.from_file("media/1x1.png")

calibrationTexture = sf.Texture.from_file("media/Calibration.png")
calibrationSprite = sf.Sprite(calibrationTexture);
calibrationSprite.scale((const.SCREEN_CORRECTION, const.SCREEN_CORRECTION))

game_state = GameState.WAIT_CALIBRATE

calibratePressed = False;

img_cal_start = 0

TrackTalker.tell_restart();

coords=[]

# start the game loop
while window.is_open:
    # process events
    for event in window.events:
        # close window: exit
        if type(event) is sf.CloseEvent:
            window.close()

        #if type(event) is sf.ResizeEvent:
        #   window.size = (const.SCREEN_SIZE)

    window.clear() # clear screen
    for y in tiles:
        for x in y:
            if x:
                x.draw(window);
    r.draw(window)

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
    
        #print(coord - camera_offset, end="")

    print("")

    if game_state == GameState.WAIT_CALIBRATE:
        window.draw(calibrationSprite);

        if sf.Keyboard.is_key_pressed(sf.Keyboard.RETURN):
            img_cal_start = time.time();
            game_state = GameState.CALIBRATE

    elif game_state == GameState.CALIBRATE:
        calibrate()
    elif game_state == GameState.START_GAME:
        if sf.Keyboard.is_key_pressed(sf.Keyboard.RETURN) and window.has_focus():
            white_sprite = sf.Sprite(std_texture);
            white_sprite.scale(const.SCREEN_SIZE_CORRECTED)
            window.draw(white_sprite)

            if len(corrected_coords) != 0:
                closest_tiles = get_closest_tiles(corrected_coords[0], 3)

                for tile in closest_tiles:
                    tile.set_color(255,0,0)

                #print("Updating tile: ", tile.coordinates)

        
    for sprite in pawn_sprites:
        window.draw(sprite)

    window.display() # update the window

