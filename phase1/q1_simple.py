import math

# Definition of the polygon to be analyzed
points = [
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 3),
    (2, 4),
    (3, 4),
    (3, 3),
    (3, 2),
    (2, 2),
    (2, 1),
    (1, 1),
]


def is_polygon_valid(polygon_points):
    """Evaluates if the list of points follows the rules for defining a Polygon.
    - First and last point are the same.

    Args:
        polygon_points (A list of 2D coordinates): points of the polygon.
    Returns:
        boolean: whether the points of the polygon follow the rules defined.
    """
    return polygon_points[0] == polygon_points[len(polygon_points) - 1]


def is_point_between(point_a, between_point, point_b):
    """Evaluates if a point is contained in the same line segment defined by point a and point b.

    Args:
        point_a (2D coordinate): Given point a
        between_point (2D coordinate): point to be analyzed if it is between point a and point b
        point_b (2D coordinate): Given point b
    Returns:
        boolean: whether the point is in the same line segment defined by point a and point b
    """
    test_distance = math.dist(point_a, between_point) + math.dist(
        between_point, point_b
    )
    return math.dist(point_a, point_b) == test_distance


def remove_in_between_points(points):
    """Removes points that do not define line segments from a list of points that define a polygon.
    In other words, points that are "in between" two other points.

    Args:
        points (A list of 2D coordinates): points of the polygon.
    Returns:
        clean_points (A list of 2D coordinates): points of the polygon without redundant points.
    """
    # Creates a copy of the list to not alter original list.
    aux_points = points.copy()
    # This elongates the array in a circular manner. Adds second last point to the beginning of the list,
    # and second point to the end of the list, simplifying loop operations.
    aux_points.insert(0, points[len(aux_points) - 2])
    aux_points.append(points[1])

    # Array that will be filled with valid points
    clean_points = []
    for i in range(1, len(aux_points) - 1):
        # If the point is not contained in a line segment between the previous and
        # next point, add it to the list of valid points.
        if not is_point_between(aux_points[i - 1], aux_points[i], aux_points[i + 1]):
            clean_points.append(aux_points[i])

    # If the start point is a redundant point, it was removed. Adding the new starting point at
    # the end of the list will ensure it is a closed polygon.
    if not is_polygon_valid(clean_points):
        clean_points.append(clean_points[0])

    return clean_points


def clean_polygon(points):
    """Removes redundant points from a list of points that define a polygon.

    Args:
        points (A list of 2D coordinates): points of the polygon.
    Returns:
        clean_points (A list of 2D coordinates): points of the polygon without redundant points.
    """
    # If the input polygon is invalid according to format, cease analysis.
    if not is_polygon_valid(points):
        print("Input Polygon is invalid.")
        return []

    # Now, apply all the functions for removing redundant points.
    aux_points = remove_in_between_points(points)

    # Tests if the newly generated polygon is valid according to format.
    if not is_polygon_valid(aux_points):
        print(aux_points)
        print("Output Polygon is invalid.")
        return []
    return aux_points


# Test scenario.
print("Before list reduction: ", points)
print("After list reduction: ", clean_polygon(points))
