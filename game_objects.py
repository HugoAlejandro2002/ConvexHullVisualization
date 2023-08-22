import arcade

class Point(arcade.Sprite):
    def __init__(self, x: float, y: float, color=arcade.color.WHITE):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.color = color
        self.tint = False

    def draw(self):
        color = arcade.color.BLACK if self.tint else self.color
        arcade.draw_circle_filled(self.center_x, self.center_y, 5, color)

