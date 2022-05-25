import math
from typing import Iterable

import pygame


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


def gameLoop(convex_hull_points, points):
    game_over = False
    game_close = False

    while not game_over:
        dis.fill(black)
        while game_close == True:
            dis.fill(white)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        mult = 25
        add = 200
        for p in points:
            pygame.draw.circle(dis, blue, (p[0] * mult + 200, p[1] * mult + 200), 2)
        for p in convex_hull_points:
            pygame.draw.circle(dis, red, (p.x * mult + 200, p.y * mult + 200), 2)

        ### Unfinished part is here
        n=len(convex_hull_points)
        for i in range(0, n):
            min_dis = 99999
            next_point: Point = None
            for j in range(0, len(convex_hull_points)):
                if not i == j:
                    distance = math.dist((convex_hull_points[i].x,convex_hull_points[i].y),
                                         (convex_hull_points[j].x,convex_hull_points[j].y))
                    if (min_dis > distance):
                        min_dis=distance
                        next_point = convex_hull_points[j]

            pygame.draw.line(dis, green,
                             (convex_hull_points[i].x * mult + 200, convex_hull_points[i].y * mult + 200), (
                                 convex_hull_points[j].x * mult + 200, convex_hull_points[j].y * mult + 200),
                             1)
            convex_hull_points.remove(next_point)
            n=len(convex_hull_points)


        """
        pygame.draw.line(dis, green,
                                    (convex_hull_points[i].x * mult + 200, convex_hull_points[i].y * mult + 200), (
                                    convex_hull_points[j].x * mult + 200, convex_hull_points[j].y * mult + 200),
                                    1)
        """
        pygame.display.update()
        clock.tick(5)
    pygame.quit()
    quit()


def main():
    points = [
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

    result = find_convex_hull(points)
    print(result)
    gameLoop(result, points)


if __name__ == "__main__":
    main()
