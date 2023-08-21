import math
import arcade
from game_objects import Point

WIDTH = 1800
HEIGHT = 800
TITLE = "Graham Convex Hull"


class App(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        self.sprites = arcade.SpriteList()
        self.hull_points = []

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            point = Point(x, y)
            self.sprites.append(point)

    def implement_graham(self):
        points = [(sprite.center_x, sprite.center_y) for sprite in self.sprites]
        if len(points) < 3:
            return

        # Encuentra el punto más bajo y más a la izquierda
        pivot = min(points, key=lambda p: (p[1], p[0]))

        # Ordena los puntos según el ángulo polar respecto al punto pivote
        sorted_points = sorted(points, key=lambda p: math.atan2(p[1] - pivot[1], p[0] - pivot[0]))

        # Inicializa la envoltura convexa con los primeros tres puntos
        hull = [pivot, sorted_points[0], sorted_points[1]]

        for point in sorted_points[2:]:
            while len(hull) > 1 and self.cross_product(hull[-2], hull[-1], point) < 0:
                hull.pop()
            hull.append(point)

        self.hull_points = hull

    def cross_product(self, o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.implement_graham()

    def on_draw(self):
        arcade.start_render()
        self.sprites.draw()

        if len(self.hull_points) > 1:
            arcade.draw_line_strip(self.hull_points, arcade.color.BLUE, 3)
            arcade.draw_line(self.hull_points[-1][0], self.hull_points[-1][1],
                             self.hull_points[0][0], self.hull_points[0][1], arcade.color.BLUE, 3)


if __name__ == "__main__":
    app = App()
    arcade.run()
