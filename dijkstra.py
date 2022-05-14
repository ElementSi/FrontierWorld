import cmath
import heapq


def make_grid(region_map, list_solid_object):
    """
    Making cell velocity multiplier matrix
    :param region_map: Map object - map of the game region
    :param list_solid_object: list[MapObject object,...] - list of all objects that can block a path
    :return: grid: list[list[float]] - velocity multiplier matrix
    """
    grid = []
    width = region_map.width
    height = region_map.height

    for i in range(0, height):
        grid.append([])
        for j in range(0, width):
            grid[-1].append(1 / region_map.field[i][j].speed_mod)

    for solid_object in list_solid_object:
        grid[int(solid_object.coord[1] + 0.5)][int(solid_object.coord[0] + 0.5)] = 10000

    return grid


def make_graph(region_map, list_solid_object):
    """
    Making a dict. The Key: velocity coefficient values at the given coordinate
                  Value: velocity coefficient values around the given coordinate
    :param region_map: Map object - map of the game region
    :param list_solid_object: list[MapObject object,...] - list of all objects that can block a path
    :return: {float: list[float]}: The Key - velocity coefficient values around the given tile
    """
    graph = {}
    grid = make_grid(region_map, list_solid_object)
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y, region_map, list_solid_object)
    return graph


def check_next_node(x_element, y_element, cols, rows):
    """
    Checking for the entry of the next tal into the game map
    :param x_element:
    :param y_element:
    :param cols:
    :param rows:
    :return:
    """
    return 0 <= x_element < cols and 0 <= y_element < rows


def get_next_nodes(x, y, region_map, list_solid_object):
    """
    Finding cell coordinates around the current in a certain direction
    :param x: float - x location coordinate
    :param y: float - y location coordinate
    :param region_map: Map object - map of the game region
    :param list_solid_object: list[SolidObject object,...] - list of all objects that can block a path
    :return: [float, float] - coordinate around the current in a certain direction
    """
    grid = make_grid(region_map, list_solid_object)
    cols = region_map.width
    rows = region_map.height
    ways = [-1, 0], [0, -1], [1, 0], [0, 1], [1, 1], [1, -1], [-1, 1], [-1, -1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy, cols, rows)]


def dijkstra_logic(creature_coord, goal_coord, region_map, list_solid_object):
    """
    Implementation of Dijkstra 's algorithm
    :param creature_coord: [float, float] - coordinates of creature for whom we are looking for a way
    :param goal_coord: [int, int] - finish coordinate
    :param region_map: Map object - map of the game region
    :param list_solid_object: list[MapObject object,...] - list of all objects that can block a path
    :return: list[list[int, int],...] - list of tiles to go through
    """
    graph = make_graph(region_map, list_solid_object)
    start = (int(creature_coord[0] + 0.5), int(creature_coord[1] + 0.5))
    goal = (goal_coord[0], goal_coord[1])
    queue_coords = []
    heapq.heappush(queue_coords, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue_coords:
        cur_cost, cur_node = heapq.heappop(queue_coords)
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            neigh_cost, neigh_node = next_node
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                heapq.heappush(queue_coords, (new_cost, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node

    cur_node = goal
    path = list()
    coordinates = list()
    coordinates.append(goal[0])
    coordinates.append(goal[1])
    path.append(coordinates)
    while cur_node != start:
        cur_node = visited[cur_node]
        coordinates = [cur_node[1], cur_node[0]]
        path.append(coordinates)

    path.reverse()
    path.pop(0)
    return path


def time_counter(path_to_finish, region_map):
    """
    Counting time which is necessary to overcome the path
    :param path_to_finish: list[list[float]]
    :param region_map: Map object - map of the game region
    :return: float - time
    """
    time = 0.0
    number_element = 1
    while number_element != path_to_finish.size():
        x0 = path_to_finish[number_element - 1][0]
        y0 = path_to_finish[number_element - 1][1]
        x1 = path_to_finish[number_element][0]
        y1 = path_to_finish[number_element][1]
        facet = cmath.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
        time += facet / region_map.field[y0][x0].speed_mod
    return time