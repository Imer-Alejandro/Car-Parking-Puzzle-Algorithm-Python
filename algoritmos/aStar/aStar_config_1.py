import heapq
import time
import psutil
import math

def manhattan_distance(vehicle, goal_position):
    return sum(abs(x - goal_position[0]) + abs(y - goal_position[1]) for x, y in vehicle.positions)

def blocking_vehicles(state):
    blocking_count = 0
    vehicle_A = state.vehicles['A']
    goal_x = len(state.board[0]) - 1

    for x, y in vehicle_A.positions:
        if x < goal_x:
            for xx in range(x + 1, goal_x + 1):
                if state.board[y][xx] not in ('.', 'A'):
                    blocking_count += 1
    return blocking_count

def euclidean_distance(vehicle, goal_position):
    return math.sqrt(sum((x - goal_position[0]) ** 2 + (y - goal_position[1]) ** 2 for x, y in vehicle.positions))

def heuristic(state, goal_position):
    vehicle_A = state.vehicles['A']
    h1 = manhattan_distance(vehicle_A, goal_position)
    h2 = blocking_vehicles(state)
    h3 = euclidean_distance(vehicle_A, goal_position)
    return (h1 + h2 + h3) / 3  # Pesos iguales a las heurísticas

def a_star_solve(initial_state, goal_state_func):
    start_time = time.time()
    process = psutil.Process()
    goal_position = (len(initial_state.board[0]) - 1, 0)  # Suponiendo que la salida está en la última columna de la fila 0
    heap = []
    heapq.heappush(heap, (0, initial_state))
    visited = set()
    parent_map = {}
    action_map = {}
    nodes_expanded = 0
    max_search_depth = 0

    while heap:
        current_priority, current_state = heapq.heappop(heap)
        current_depth = current_state.depth if hasattr(current_state, 'depth') else 0

        if current_state in visited:
            continue

        visited.add(current_state)
        nodes_expanded += 1

        if goal_state_func(current_state):
            end_time = time.time()
            running_time = end_time - start_time
            path, actions = reconstruir_camino(parent_map, action_map, current_state)
            write_metrics(path, actions, nodes_expanded, current_depth, max_search_depth, running_time, process)
            return path

        for next_state, action in current_state.generar_nuevos_estados():
            if next_state not in visited:
                next_state.depth = current_depth + 1
                cost = current_priority + 1  # Suponiendo costo uniforme de 1 por movimiento
                heuristic_cost = heuristic(next_state, goal_position)
                priority = cost + heuristic_cost
                next_state.cost = priority  # Guardar el costo en el estado
                heapq.heappush(heap, (priority, next_state))
                parent_map[next_state] = current_state
                action_map[next_state] = action
                max_search_depth = max(max_search_depth, current_depth + 1)

    return None

def reconstruir_camino(parent_map, action_map, goal_state):
    path = []
    actions = []
    current_state = goal_state
    while current_state in parent_map:
        path.append(current_state)
        actions.append(action_map[current_state])
        current_state = parent_map[current_state]
    path.reverse()
    actions.reverse()
    return path, actions

def write_metrics(path, actions, nodes_expanded, search_depth, max_search_depth, running_time, process):
    path_to_goal = actions
    cost_of_path = len(path)
    max_ram_usage = process.memory_info().rss / 1024.0

    with open('output/AST_output_metric.txt', 'w') as f:
        f.write(f"path_to_goal: {path_to_goal}\n")
        f.write(f"cost_of_path: {cost_of_path}\n")
        f.write(f"nodes_expanded: {nodes_expanded}\n")
        f.write(f"search_depth: {search_depth}\n")
        f.write(f"max_search_depth: {max_search_depth}\n")
        f.write(f"running_time: {running_time:.8f}\n")
        f.write(f"max_ram_usage: {max_ram_usage:.8f}\n")
