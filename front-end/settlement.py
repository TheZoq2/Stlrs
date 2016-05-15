import sfml as sf

village_texture = sf.Texture.from_file("media/village.png")


class Settlement:
    def __init__(self, tiles):
        self.tiles = tiles

        sum_x = 0
        sum_y = 0
        for tile in tiles:
            sum_x += tile.get_world_pos()[0]
            sum_y += tile.get_world_pos()[1]

        self.pos = sf.Vector2(sum_x / 3, sum_y / 3)

        s = sf.Sprite(village_texture)
        s.origin = sf.Vector2(50,90)
        s.scale((0.4, 0.4))
        s.position = self.pos
        self.sprite = s;

    def draw(self, window):
        window.draw(self.sprite)
