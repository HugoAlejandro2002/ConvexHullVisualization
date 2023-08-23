import arcade
import math

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

    @staticmethod
    def cross_product(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    @staticmethod
    def sort_by_angle_and_distance(points, pivot):
        return sorted(points, key=lambda p: (
            math.atan2(p[1] - pivot[1], p[0] - pivot[0]),
            (p[0] - pivot[0]) ** 2 + (p[1] - pivot[1]) ** 2
        ))

    @staticmethod
    def graham_algorithm(points, pivot):
        sorted_points = Point.sort_by_angle_and_distance(points, pivot)
        hull = [pivot, sorted_points[0], sorted_points[1]]
        for point in sorted_points[2:]:
            while len(hull) > 1 and Point.cross_product(hull[-2], hull[-1], point) <= 0:
                hull.pop()
            hull.append(point)
        return hull
