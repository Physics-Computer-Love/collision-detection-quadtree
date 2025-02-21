import random
import time

from pympler import asizeof

from src.quadtree import Quadtree, Rectangle, Point


def benchmark_quadtree_size():
    qtree = Quadtree(Rectangle(0, 0, 100, 100), 4)

    print(f"Size: {asizeof.asizeof(qtree) / 1024:.2f} KB")

def benchmark_insert_time():
    qtree = Quadtree(Rectangle(0, 0, 100, 100), 4)

    points = [
        Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(10000)
    ]


    start = time.time()

    qtree.batch_insert(points)

    end = time.time()

    print(f"\nInsert: {(end - start) * 1000:.2f} ms")
    print(f"Points size: {asizeof.asizeof(points) / 1024:.2f} KB")
    print(f"Quadtree size: {asizeof.asizeof(qtree) / 1024:.2f} KB")

def benchmark_query_time():
    qtree = Quadtree(Rectangle(0, 0, 100, 100), 4)

    points = [
        Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(10000)
    ]

    for p in points:
        qtree.insert(p)

    query_rect = Rectangle(20, 20, 30, 30)

    start = time.time()
    qtree.query(query_rect)
    end = time.time()

    print(f"\nQuery: {(end - start) * 1000:.2f} ms")
    print(f"Points size: {asizeof.asizeof(points) / 1024:.2f} KB")
    print(f"Quadtree size: {asizeof.asizeof(qtree) / 1024:.2f} KB")

if __name__ == '__main__':
    benchmark_quadtree_size()
    benchmark_insert_time()
    benchmark_query_time()