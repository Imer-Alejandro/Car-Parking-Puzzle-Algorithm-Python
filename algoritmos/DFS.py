import time
import psutil

def dfs_solve(initial_state, goal_state_func):
    start_time = time.time()
    process = psutil.Process()
    stack = [(initial_state, None)]
    visited = set()
    parent_map = {}
    action_map = {}
    nodes_expanded = 0
    max_search_depth = 0

    while stack:
        current_state, action = stack.pop()
        current_depth = current_state.depth if hasattr(current_state, 'depth') else 0

        if current_state in visited:
            continue
        
        visited.add(current_state)
        nodes_expanded += 1

        if action:
            action_map[current_state] = action

        if goal_state_func(current_state):
            end_time = time.time()
            running_time = end_time - start_time
            path, actions = reconstruir_camino(parent_map, action_map, current_state)
            write_metrics(path, actions, nodes_expanded, current_depth, max_search_depth, running_time, process)
            return path
        
        for next_state, action in current_state.generar_nuevos_estados():
            if next_state not in visited:
                next_state.depth = current_depth + 1
                stack.append((next_state, action))
                parent_map[next_state] = current_state
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

    with open('output/DFS_output_metric.txt', 'w') as f:
        f.write(f"path_to_goal: {path_to_goal}\n")
        f.write(f"cost_of_path: {cost_of_path}\n")
        f.write(f"nodes_expanded: {nodes_expanded}\n")
        f.write(f"search_depth: {search_depth}\n")
        f.write(f"max_search_depth: {max_search_depth}\n")
        f.write(f"running_time: {running_time:.8f}\n")
        f.write(f"max_ram_usage: {max_ram_usage:.8f}\n")