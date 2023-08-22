import math
import arcade
from game_objects import Point

WIDTH = 1800
HEIGHT = 800
TITLE = "Graham Convex Hull"

class App(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.sprites = arcade.SpriteList()
        self.hull_points = []
        self.current_step = 0  # Para controlar qué paso del algoritmo se muestra
        self.sorted_points = []
        self.current_hull_index = 0
        self.current_hull_index = 0
        self.time_counter = 0  # Contador de tiempo para controlar la velocidad de dibujo
        self.time_interval = 0.5 

    def on_update(self, delta_time: float):
        for point in self.sprites:
            point.tint = not point.tint  # Para el tintineo de los puntos

        self.time_counter += delta_time  # Incrementar el contador de tiempo

        # Incrementar el índice del casco convexo para dibujar la siguiente línea
        if self.time_counter >= self.time_interval:
            if self.current_hull_index < len(self.hull_points) - 1:
                self.current_hull_index += 1
            self.time_counter = 0 
            
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            point = Point(x, y)
            self.sprites.append(point)

    def implement_graham(self):
        if self.current_step == 0:
            # Paso 1: Encuentra el punto más bajo y más a la izquierda
            points = [(sprite.center_x, sprite.center_y) for sprite in self.sprites]
            if len(points) < 3:
                return
            self.pivot = min(points, key=lambda p: (p[1], p[0]))
            self.current_step += 1

        elif self.current_step == 1:
            # Paso 2: Ordena los puntos según el ángulo polar respecto al punto pivote
            points = [(sprite.center_x, sprite.center_y) for sprite in self.sprites]
            self.sorted_points = sorted(points, key=lambda p: math.atan2(p[1] - self.pivot[1], p[0] - self.pivot[0]))
            self.current_step += 1

        elif self.current_step == 2:
            # Paso 3: Implementar el algoritmo de Graham para encontrar la envoltura convexa
            hull = [self.pivot, self.sorted_points[0], self.sorted_points[1]]
            for point in self.sorted_points[2:]:
                while len(hull) > 1 and self.cross_product(hull[-2], hull[-1], point) < 0:
                    hull.pop()
                hull.append(point)
            self.hull_points = hull
            self.current_step = 0  
            self.current_hull_index = 0

    def cross_product(self, o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.implement_graham()

    def on_draw(self):
        arcade.start_render()
        for point in self.sprites:
            point.draw()

        # Resaltar el punto pivote
        if self.current_step >= 1:
            arcade.draw_circle_outline(self.pivot[0], self.pivot[1], 10, arcade.color.WHITE_SMOKE, 3)

        # Mostrar los puntos ordenados
        if self.current_step >= 2:
            for i, point in enumerate(self.sorted_points):
                arcade.draw_text(str(i), point[0] + 10, point[1] + 10, arcade.color.WHITE, 12)

            
        if len(self.hull_points) > 1:
            for i in range(min(self.current_hull_index, len(self.hull_points) - 1)):
                arcade.draw_line(self.hull_points[i][0], self.hull_points[i][1],
                                 self.hull_points[i + 1][0], self.hull_points[i + 1][1], arcade.color.WHITE, 3)
            
            if self.current_hull_index == len(self.hull_points) - 1:
                arcade.draw_line(self.hull_points[-1][0], self.hull_points[-1][1],
                                 self.hull_points[0][0], self.hull_points[0][1], arcade.color.WHITE, 3)



if __name__ == "__main__":
    app = App()
    arcade.run()
