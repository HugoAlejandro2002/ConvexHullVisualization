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
        self.current_step = 0
        self.current_hull_index = 0
        self.time_counter = 0
        self.time_interval = 0.5

    def on_update(self, delta_time: float):
        self.update_tint()
        self.update_hull_index(delta_time)

    def update_tint(self):
        for point in self.sprites:
            point.tint = not point.tint

    def update_hull_index(self, delta_time):
        self.time_counter += delta_time
        if self.time_counter >= self.time_interval:
            if self.current_hull_index < len(self.hull_points) - 1:
                self.current_hull_index += 1
            self.time_counter = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.add_point(x, y)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.remove_point(x, y)

    def add_point(self, x, y):
        point = Point(x, y)
        self.sprites.append(point)
        self.current_step = 0
        self.hull_points = []

    def remove_point(self, x, y):
        for point in self.sprites:
            if abs(point.center_x - x) < 10 and abs(point.center_y - y) < 10:
                point.remove_from_sprite_lists()
                self.current_step = 0
                self.hull_points = []
                break

    def implement_graham(self):
        points = [(sprite.center_x, sprite.center_y) for sprite in self.sprites]
        if len(points) < 3:
            return

        if self.current_step == 0:
            self.pivot = min(points, key=lambda p: (p[1], p[0]))
            self.current_step += 1
        elif self.current_step == 1:
            self.sorted_points = Point.sort_by_angle_and_distance(points, self.pivot)
            self.current_step += 1
        elif self.current_step == 2:
            self.hull_points = Point.graham_algorithm(points, self.pivot)
            self.current_hull_index = 0
            self.current_step = 4

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.implement_graham()
        elif key == arcade.key.R:
            self.reset()

    def reset(self):
        self.sprites = arcade.SpriteList()
        self.hull_points = []
        self.current_step = 0

    def on_draw(self):
        arcade.start_render()
        self.draw_points()
        self.draw_status_and_instructions()
        self.draw_hull()
        
        if self.current_step >= 1:
            arcade.draw_circle_outline(self.pivot[0], self.pivot[1], 10, arcade.color.WHITE_SMOKE, 3)

        if self.current_step >= 2:
            for i, point in enumerate(self.sorted_points):
                arcade.draw_text(str(i), point[0] + 10, point[1] + 10, arcade.color.WHITE, 12)


    def draw_points(self):
        for point in self.sprites:
            point.draw()

    def draw_status_and_instructions(self):
        status_text = ["Añadir Puntos", "Seleccionamiento de Pivote", "Ordenamiento de Puntos", "Dibujando...", "Convex Hull"]
        arcade.draw_text(status_text[self.current_step], 10, HEIGHT - 30, arcade.color.WHITE, 20)
        
        instructions = [
            "Instrucciones:",
            "Clic izquierdo: Añadir punto",
            "Clic derecho: Eliminar punto",
            "Espacio: Siguiente Paso",
            "R: Reiniciar"
        ]
        y_position = HEIGHT - 60
        for instruction in instructions:
            arcade.draw_text(instruction, 10, y_position, arcade.color.WHITE, 16)
            y_position -= 20

    def draw_hull(self):
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
