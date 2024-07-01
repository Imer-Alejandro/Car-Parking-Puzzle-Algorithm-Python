import time
import psutil
import heapq

def heuristic_1(state):
    # Heurística: distancia de Manhattan del vehículo 'A' a la posición del '0'
    vehicle_a_pos = state.vehicles['A'].positions[0]
    vehicle_0_pos = state.vehicles['0'].positions[0]
    return abs(vehicle_a_pos[0] - vehicle_0_pos[0]) + abs(vehicle_a_pos[1] - vehicle_0_pos[1])

def heuristic_2(state):
    # Heurística: número de vehículos en el camino del vehículo 'A' a la salida
    vehicle_a_pos = state.vehicles['A'].positions
    row_a = vehicle_a_pos[0][1]
    return sum(1 for (id, vehicle) in state.vehicles.items() if id != 'A' and id != '0' and any(y == row_a for x, y in vehicle.positions))

def heuristic_3(state):
    # Heurística: distancia en celdas desde el vehículo 'A' hasta el borde derecho del tablero
    vehicle_a_pos = state.vehicles['A'].positions[0]
    return len(state.board[0]) - vehicle_a_pos[0] - 1

def a_star_solve(initial_state, goal_state_func):
    start_time = time.time()
    process = psutil.Process()
    
    # Inicializar el heap de prioridades y otros datos
    heap = []
    heapq.heappush(heap, (0, initial_state))
    visited = set()
    parent_map = {}
    action_map = {}
    cost_map = {initial_state: 0}
    nodes_expanded = 0
    max_search_depth = 0
    
    while heap:
        _, current_state = heapq.heappop(heap)
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
            new_cost = cost_map[current_state] + 1  # Asumiendo costo de 1 por cada movimiento
            if next_state not in cost_map or new_cost < cost_map[next_state]:
                cost_map[next_state] = new_cost
                heur = (heuristic_1(next_state) + heuristic_2(next_state) + heuristic_3(next_state)) / 3
                priority = new_cost + heur
                heapq.heappush(heap, (priority, next_state))
                parent_map[next_state] = current_state
                action_map[next_state] = action
                next_state.depth = current_depth + 1
                max_search_depth = max(max_search_depth, next_state.depth)
    
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
