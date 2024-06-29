# algoritmos/dfs.py
from logic.estados import State

def dfs_solve(initial_state, goal_state_func):
    stack = [initial_state]
    visited = set()
    parent_map = {}

    while stack:
        current_state = stack.pop()
        if current_state in visited:
            continue
        
        visited.add(current_state)

        if goal_state_func(current_state):
            return reconstruir_camino(parent_map, current_state)
        
        for next_state in current_state.generar_nuevos_estados():
            if next_state not in visited:
                stack.append(next_state)
                parent_map[next_state] = current_state

    return None

def reconstruir_camino(parent_map, goal_state):
    path = []
    current_state = goal_state
    while current_state in parent_map:
        path.append(current_state)
        current_state = parent_map[current_state]
    path.reverse()
    return path