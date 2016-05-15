import sfml as sf
import constants as const
import math
class road:

    def __init__(self, neighbours):
        self.neighbours = neighbours
        t  = sf.Texture.from_file('media/road.png')
        s = sf.Sprite(t)
        s.scale((const.SCALE, const.SCALE))
        s.origin = sf.Vector2(50, 12.5)
        pos = self._calc_pos()
        ang = self._calc_angle()
        print(ang)
        s.rotate(ang)
        s.position = sf.Vector2(pos[0], pos[1])
        
        
        self.sprite = s


    def draw(self, canvas):
        canvas.draw(self.sprite)

    def _calc_angle(self):
        print(self.neighbours[0].get_coordinates()[1])
        #if self.neighbours[0].get_coordinates()[1] == self.neighbours[1].get_coordinates()[1]:
        #    return 90
        #return 0
        
        n1_world_pos = self.neighbours[0].get_world_pos()
        n2_world_pos = self.neighbours[1].get_world_pos()
        diff = (n1_world_pos[0] - n2_world_pos[0], n1_world_pos[1] - n2_world_pos[1])

        return math.atan(diff[1]/diff[0]) / math.pi * 180 + 90

    def _calc_pos(self):
        n1_world_pos = self.neighbours[0].get_world_pos()
        n2_world_pos = self.neighbours[1].get_world_pos()

        return (((n1_world_pos[0] - n2_world_pos[0]) / 2 + n2_world_pos[0]),
                ((n1_world_pos[1] - n2_world_pos[1]) / 2 + n2_world_pos[1]))
