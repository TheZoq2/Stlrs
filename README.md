# Stlrs
Inovative board game engine for the 21th century :)

A quick video of the project in action can be seen [here](https://www.youtube.com/watch?v=aMyHLjdJJoI)

This project is the result of the LIU Spring Game Jam 2016. The goal was to create a semi physical 
version of the settlers of catan board game. Players still interract with the game using regular physical
game pieces but the computer keeps track of resources and placed settlements. 

Unfortunley we did not have time to implement the actual game but the object recognition and placement of the 
game pieces works as expected.

#Technical details

The project consts of two parts, one image recognition part written in C++ using openCV for image recognition and the 
game part written in python using python-sfml for rendering. The two parts communicate by reading and writing to two files,
`/tmp/stlrs_cmd` and `/tmp/stlrs_coords`. The cmd file is used for the python script to send commands to the tracking part
while the coords file contains the coordinates found during the last search run by the tracker.

##Object recognition
The image recognition code was written before the game jam but had a few bug fixes during the jam itself. Object recognition
is done in three steps.

First, an image is captured from the camera which is then converted from an RGB color space to a HSV space. This is done
because it is much easier to filter out a specific color or brightness of an image in HSV than RGB.

The HSV image is then searched through for pixels that fall within a specific threshold and a new image is created that contains
only black or white pixels. This data is also stored in a separte structure that is used in the next step.

A flood fill is performed on the 'binary image' which finds all separate 'islands' in the image. All islands with a sufficient
size are written to the communication file and sent to the python script.

In order to remove any fish-eye effect from the camera, the cv::unidistort function is run using previously calibrated parameters.

The C++ backend of the project has one additional function which is to project the coordinates seen by the camera to coordinates
on the game window. When the game has started, the user is told to place 4 game pieces on specific points on the board. These
points are known by both the python and C++ component and by comparing the points as they appear on the camera to how they are
on the screen, the camera coordinates can be translated to screen coordinates. This is done using the opencv function 
`cv::getPerspectiveTransform` and `warpPerspective`.

Once the callibration is done, the converted coordinates are sent to the python program.

##Game part
The python program that handles the game receives raw coordinates from the tracking program and uses them to calculate
what pieces are placed where. If we had had time to implement it, it would have handled the game logic aswell but for now,
it only keeps track of what pieces have been placed.

During each players turn, they would place any new pieces they want to add to the board where they should be added. Then they
would hit something on the computer which would run the image processing to figgure out where the pieces have been placed and
store that data. The physical pieces would then be removed and the next player would make their turn.

Because the pieces are relativley small compared to the board itself, the type of piece can't be distinguished based on
the camera image. But luckily, in the base version of settlers, a piece placed on the board can only mean on thing at a time.
If a piece is placed on the edge of two tiles, it has to be a road, while a piece placed on an empty corner of three tiles 
has to be a new village. If the piece is placed in a corner where a village already exists, it has to be a town. This allows
the python script to figgure out what pieces are placed. 
