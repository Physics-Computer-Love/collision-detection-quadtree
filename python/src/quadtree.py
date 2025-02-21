from dataclasses import dataclass
import numpy as np
from matplotlib import pyplot as plt


def compute_bounding_box(points):
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)
    return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)


@dataclass(slots=True)
class Point:
    x: int
    y: int
    metadata: dict = None

    def __repr__(self):
        return f'Point({self.x}, {self.y})'


@dataclass(slots=True)
class Rectangle:
    x: int
    y: int
    width: int
    height: int

    def contains(self, point):
        return (self.x <= point.x < self.x + self.width and
                self.y <= point.y < self.y + self.height)

    def intersects(self, other) -> bool:
        return not (other.x > self.x + self.width or
                other.x + other.width < self.x or
                other.y > self.y + self.height or
                other.y + other.height < self.y)

    def __repr__(self):
        return f'Rectangle({self.x}, {self.y}, {self.width}, {self.height})'


class Quadtree:
    def __init__(self, boundary: Rectangle, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = np.empty((capacity, 2), dtype=np.int32)
        self.metadata = np.empty(capacity, dtype=object)
        self.point_count = 0
        self.divided = False

        self.north_east = None
        self.north_west = None
        self.south_east = None
        self.south_west = None

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width
        h = self.boundary.height

        half_width = w // 2
        half_height = h // 2

        # Create four children that divide the current region
        ne = Rectangle(x + half_width, y - half_height, half_width, half_height)
        self.north_east = Quadtree(ne, self.capacity)

        nw = Rectangle(x, y, half_width, half_height)
        self.north_west = Quadtree(nw, self.capacity)

        se = Rectangle(x + half_width, y + half_height, half_width, half_height)
        self.south_east = Quadtree(se, self.capacity)

        sw = Rectangle(x, y + half_height, half_width, half_height)
        self.south_west = Quadtree(sw, self.capacity)

        self.divided = True

    def insert(self, point: Point):
        stack = [self]

        while stack:
            current = stack.pop()
            if not current.boundary.contains(point):
                continue


            if current.point_count < current.capacity:
                current.points[current.point_count] = (point.x, point.y)
                current.metadata[current.point_count] = point.metadata
                current.point_count += 1
                return True

            if not current.divided:
                current.subdivide()

            stack.extend([current.north_east, current.north_west, current.south_east, current.south_west])

        return False

    def query(self, range_rect: Rectangle, found=None):
        if found is None:
            found = []

        stack = [self]

        while stack:
            current = stack.pop()
            if not current.boundary.intersects(range_rect):
                continue

            for i in range(current.point_count):
                point = Point(*current.points[i], current.metadata[i])
                if range_rect.contains(point):
                    found.append(point)

            if current.divided:
                stack.extend([current.north_east, current.north_west, current.south_east, current.south_west])

        return found

    def plot(self, ax):
        rect = plt.Rectangle((self.boundary.x, self.boundary.y),
                             self.boundary.width,
                             self.boundary.height,
                             fill=False, color="black", lw=0.8)

        ax.add_patch(rect)

        if self.divided:
            for quadrant in [self.north_east, self.north_west, self.south_east, self.south_west]:
                quadrant.plot(ax)

    def batch_insert(self, points):
        for point in points:
            self.insert(point)
