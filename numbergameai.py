import heapq
from collections import deque

def sliding_puzzle_solver(array):
    # Goal state
    goal = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    if tuple(array) == goal:
        return []

    # Directions for moving the empty space
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
    moves = ["UP", "DOWN", "LEFT", "RIGHT"]
    
    # Helper to find the position of the empty tile (0)
    def find_empty_pos(state):
        for i in range(3):
            for j in range(3):
                if state[i * 3 + j] == 0:
                    return i, j
    
    # A* search algorithm
    def heuristic(state):
        # Count the number of misplaced tiles
        return sum(cur != goal[i] for i, cur in enumerate(state))
    
    def generate_next_states(state):
        empty_x, empty_y = find_empty_pos(state)
        for i, (dx, dy) in enumerate(directions):
            new_x, new_y = empty_x + dx, empty_y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = list(state)
                # Swap the empty tile with the adjacent tile
                new_state[empty_x * 3 + empty_y], new_state[new_x * 3 + new_y] = \
                new_state[new_x * 3 + new_y], new_state[empty_x * 3 + empty_y]
                yield new_state, moves[i]
    
    # Priority queue for A* search
    pq = []
    start_state = tuple(array)
    heapq.heappush(pq, (0 + heuristic(start_state), 0, start_state, []))
    visited = set()
    
    while pq:
        est_total_cost, step_cost, current, path = heapq.heappop(pq)

        if current == goal:
            return path
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for next_state, move in generate_next_states(current):
            new_path = path + [move]
            heapq.heappush(pq, (step_cost + 1 + heuristic(next_state), step_cost + 1, tuple(next_state), new_path))
    
    return []

# Read input data
k = int(input().strip())
tiles = [int(input().strip()) for _ in range(k * k)]

# Solve the puzzle
solution = sliding_puzzle_solver(tiles)

# Output result
print(len(solution))
for move in solution:
    print(move)
