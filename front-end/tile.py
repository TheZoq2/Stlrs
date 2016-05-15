import sfml as sf
import constants as const

class tile:
    
    def __init__(self, value, img_resource, coordinates):
        self.value = value
        self.coordinates = coordinates

        texture = sf.Texture.from_file(img_resource)
        s = sf.Sprite(texture)
        s.scale((const.SCALE, const.SCALE))
        
        pos = tile._calc_pos(coordinates)
        s.position = sf.Vector2(pos[0], pos[1])
        self.sprite = s


    def get_neighbours(self):
        result = [
                    (self.coordinates[0] - 1, self.coordinates[1])
                    (self.coordinates[0] + 1, self.coordinates[1])
                ]
        if coordinates[0] % 2 == 1:
            result.append((self.coordinates[0]    , self.coordinates[1] - 1))
            result.append((self.coordinates[0] + 1, self.coordinates[1] - 1))
            result.append((self.coordinates[0]    , self.coordinates[1] + 1))
            result.append((self.coordinates[0] + 1, self.coordinates[1] + 1))
        else:
            result.append((self.coordinates[0]    , self.coordinates[1] - 1))
            result.append((self.coordinates[0] - 1, self.coordinates[1] - 1))
            result.append((self.coordinates[0]    , self.coordinates[1] + 1))
            result.append((self.coordinates[0] - 1, self.coordinates[1] + 1))
        
        return result


    def draw(self, canvas):
        canvas.draw(self.sprite)

    def get_world_pos(self):
        pos = tile._calc_pos(self.coordinates)
        return (pos[0] + 200*const.SCALE, pos[1] + 200 * const.SCALE)

    def get_coordinates(self):
        return self.coordinates

    def set_color(self, r,g,b):
        self.sprite.color = sf.graphics.Color(r,g,b)
        

    def _calc_pos(coordinates):
        if coordinates[1] % 2 == 0:
            y = coordinates[1] * (300 * const.SCALE)
            x = coordinates[0] * (346 * const.SCALE)
            return (x, y)
        else:
            y = coordinates[1] * (300 * const.SCALE)
            x = coordinates[0] * (346 * const.SCALE) + (173 * const.SCALE)
            return (x, y)
        
