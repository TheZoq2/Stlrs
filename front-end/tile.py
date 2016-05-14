import sfml as sf

SCALE = 0.5

class tile:
    
    def __init__(self, value, img_resource, coordinates):
        self.value = value
        self.coordinates = coordinates

        texture = sf.Texture.from_file(img_resource)
        s = sf.Sprite(texture)
        s.scale((SCALE, SCALE))
        
        pos = tile._calc_pos(coordinates)
        s.position = sf.Vector2(pos[0], pos[1])
        self.sprite = s

    def draw(self, canvas):
        canvas.draw(self.sprite)

    def _calc_pos(coordinates):
        if coordinates[1] % 2 == 0:
            y = coordinates[1] * (300 * SCALE)
            x = coordinates[0] * (346 * SCALE)
            return (x, y)
        else:
            y = coordinates[1] * (300 * SCALE)
            x = coordinates[0] * (346 * SCALE) + (173 * SCALE)
            return (x, y)
        
