import math
from typing import Iterable

import pygame

################################## All global variables #########################################################################################################################
points_inputs = [
    (0, 3),
    (2, 2),
    (1, 1),
    (2, 1),
    (3, 0),
    (0, 0),
    (3, 3),
    (2, -1),
    (2, -4),
    (1, -3),
]

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

pygame.init()
dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Convex Hull')
clock = pygame.time.Clock()

simulate=False

#########################################################################################################################

class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if self.x > other.x:
            return True
        elif self.x == other.x:
            return self.y > other.y
        return False

    def __lt__(self, other):
        return not self > other

    def __ge__(self, other):
        if self.x > other.x:
            return True
        elif self.x == other.x:
            return self.y >= other.y
        return False

    def __le__(self, other):
        if self.x < other.x:
            return True
        elif self.x == other.x:
            return self.y <= other.y
        return False

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash(self.x)


def construct_points(myList: list[Point] | list[list[float]] | Iterable[list[float]], ) -> list[Point]:
    points: list[Point] = []
    if myList:
        for p in myList:
            if isinstance(p, Point):
                points.append(p)
            else:
                try:
                    points.append(Point(p[0], p[1]))
                except (IndexError, TypeError):
                    print(f"Point {p}, has been ignored. All points must have at 2 coordinates.")

    return points


def validate_input(points: list[Point] | list[list[float]], ) -> list[Point]:
    if not hasattr(points, "__iter__"):
        raise ValueError(f"An interable object is expected but got an non-iterable type {points}")
    if not points:
        raise ValueError(f"A list of points was expected but got {points}")

    points_list = construct_points(points)
    return points_list


def upper_or_lower(a: Point, b: Point, c: Point) -> float:
    distance = (a.x * b.y + b.x * c.y + c.x * a.y) - (a.y * b.x + b.y * c.x + c.y * a.x)
    return distance


def construct_hull(points: list[Point], left_most_point: Point, right_most_point: Point,
                   convex_hull_points: set[Point]):
    simulatetion_loop(convex_hull_points, points_inputs, left_most_point, right_most_point,None)
    if points:
        extreme_point = None
        extreme_point_distance = float("-inf")
        candidate_points = []

        for p in points:
            distance = upper_or_lower(left_most_point, right_most_point, p)

            if distance > 0:
                candidate_points.append(p)

                if distance > extreme_point_distance:
                    extreme_point = p
                    extreme_point_distance = distance

        if extreme_point:
            simulatetion_loop(convex_hull_points, points_inputs, left_most_point,right_most_point,extreme_point)
            construct_hull(candidate_points, left_most_point, extreme_point, convex_hull_points)
            convex_hull_points.add(extreme_point)
            construct_hull(candidate_points, extreme_point, right_most_point, convex_hull_points)


def find_convex_hull(points: list[Point]) -> list[Point]:
    points = validate_input(points)
    points = sorted(points)
    n = len(points)

    left_most_point = points[0]
    right_most_point = points[n - 1]

    convex_hull_points = {left_most_point, right_most_point}
    upper_hull = []
    lower_hull = []

    for i in range(1, n - 1):
        distance = upper_or_lower(left_most_point, right_most_point, points[i])

        if distance > 0:
            upper_hull.append(points[i])
        elif distance < 0:
            lower_hull.append(points[i])

    construct_hull(upper_hull, left_most_point, right_most_point, convex_hull_points)
    construct_hull(lower_hull, right_most_point, left_most_point, convex_hull_points)

    return sorted(convex_hull_points)


def simulatetion_loop(convex_hull_points, points, left_most_point: Point, right_most_point: Point, extreme_point:Point):
    game_over = False
    if simulate==False:
        game_over=True

    while not game_over:
        dis.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        mult = 25
        add = 200
        if points:
            for p in points:
                pygame.draw.circle(dis, blue, (p[0] * mult + add, p[1] * mult + add), 2)
        for p in convex_hull_points:
            pygame.draw.circle(dis, red, (p.x * mult + add, p.y * mult + add), 2)

        if extreme_point:
            pygame.draw.circle(dis, yellow, (extreme_point.x * mult + add, extreme_point.y * mult + add), 2)
        pygame.draw.line(dis, green,
                         (left_most_point.x * mult + add, left_most_point.y * mult + add), (
                             right_most_point.x * mult + add, right_most_point.y * mult + add),
                         1)
        pygame.display.update()
        clock.tick(1)
        break

def distance_of_two_points(a:Point,b:Point):
    return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)


def gameLoop(convex_hull_points, points):
    game_over = False
    game_close = False

    while not game_over:
        dis.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        mult = 25
        add = 200
        if points:
            for p in points:
                pygame.draw.circle(dis, blue, (p[0] * mult + add, p[1] * mult + add), 2)
        for p in convex_hull_points:
            pygame.draw.circle(dis, red, (p.x * mult + add, p.y * mult + add), 2)


        ### Unfinished part is here

        for i in range(1, len(convex_hull_points)-1):
            pygame.draw.line(dis, green,
                             (convex_hull_points[i].x * mult + add, convex_hull_points[i].y * mult + add), (
                                 convex_hull_points[i+1].x * mult + add, convex_hull_points[i+1].y * mult + add),
                             1)


        """
        pygame.draw.line(dis, green,
                                    (convex_hull_points[i].x * mult + add, convex_hull_points[i].y * mult + add), (
                                    convex_hull_points[j].x * mult + add, convex_hull_points[j].y * mult + add),
                                    1)
        """
        pygame.display.update()
        clock.tick(5)

    pygame.quit()
    quit()


def main():
    result = find_convex_hull(points_inputs)
    print(result)
    gameLoop(result, points_inputs)


if __name__ == "__main__":
    main()
