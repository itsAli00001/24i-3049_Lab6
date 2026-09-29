import math
import heapq

# Hospital graph for Task 3 / Streamlit GUI
locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6),
}

hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1,
    },
    "Main_Corridor": {
        "Nursing_Station": 2.2,
    },
    "Patient_Wing": {
        "Laboratory": 5.0,
    },
    "Nursing_Station": {
        "Laboratory": 3.2,
        "Emergency_Ward": 6.0,
    },
    "Laboratory": {
        "Emergency_Ward": 3.2,
    },
    "Emergency_Ward": {},
}


def heuristic(current, goal):
    """Euclidean distance between two locations."""
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def _reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path


def _path_cost(path):
    total = 0.0
    for u, v in zip(path, path[1:]):
        total += hospital_graph[u][v]
    return total


def gbfs(start, goal):
    """Greedy Best-First Search. Returns (path, total_cost)."""
    if start not in hospital_graph or goal not in hospital_graph:
        return None, None

    frontier = []
    counter = 0
    heapq.heappush(frontier, (heuristic(start, goal), counter, start))

    came_from = {start: None}
    explored = set()

    while frontier:
        _, _, current = heapq.heappop(frontier)

        if current in explored:
            continue

        explored.add(current)

        if current == goal:
            path = _reconstruct_path(came_from, current)
            return path, _path_cost(path)

        for neighbor in hospital_graph[current]:
            if neighbor not in explored and neighbor not in came_from:
                came_from[neighbor] = current
                counter += 1
                heapq.heappush(
                    frontier,
                    (heuristic(neighbor, goal), counter, neighbor)
                )

    return None, None


def a_star(start, goal):
    """A* Search using f(n)=g(n)+h(n). Returns (path, total_cost)."""
    if start not in hospital_graph or goal not in hospital_graph:
        return None, None

    frontier = []
    counter = 0
    g_cost = {start: 0.0}
    came_from = {start: None}

    heapq.heappush(
        frontier,
        (heuristic(start, goal), counter, start)
    )

    closed = set()

    while frontier:
        _, _, current = heapq.heappop(frontier)

        if current in closed:
            continue

        closed.add(current)

        if current == goal:
            path = _reconstruct_path(came_from, current)
            return path, g_cost[current]

        for neighbor, edge_cost in hospital_graph[current].items():
            tentative_g = g_cost[current] + edge_cost

            if tentative_g < g_cost.get(neighbor, float("inf")):
                g_cost[neighbor] = tentative_g
                came_from[neighbor] = current
                counter += 1
                f_cost = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (f_cost, counter, neighbor))

    return None, None
