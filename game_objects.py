import arcade

class Point(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__("assets/black_point.png", 0.2)
        self.center_x = x
        self.center_y = y
