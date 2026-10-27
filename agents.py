from collections import deque
import heapq
from itertools import count


class SearchResult:
    def __init__(self, path, expanded):
        self.path = path
        self.expanded = expanded


def reconstruct_path(parents, goal):
    path = []
    state = goal
    while state is not None:
        path.append(state)
        state = parents[state]
    path.reverse()
    return path


def bfs(campus, start, goal):
    frontier = deque([start])
    parents = {start: None}
    expanded = 0
    while frontier:
        state = frontier.popleft()
        if state == goal:
            return SearchResult(reconstruct_path(parents, goal), expanded)
        expanded += 1
        for action, successor in campus.neighbors(state):
            if successor not in parents:
                parents[successor] = state
                frontier.append(successor)
    return SearchResult(None, expanded)


def manhattan(state, goal):
    """TODO 1: Return Manhattan distance between two (row, column) tuples."""
    # Add the absolute row difference and the absolute column difference.
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])


def astar(campus, start, goal):
    """TODO 2: Return SearchResult(path, expanded) for A* graph search."""
    # Use heapq as a priority queue and manhattan() as the heuristic.
    # Track best known g-costs and parent states in dictionaries.
    if start == goal:
        return SearchResult([start], 0)
    order = count()  # insertion number, used to break equal-f ties
    frontier = [(manhattan(start, goal), next(order), 0, start)]
    g_costs = {start: 0}
    parents = {start: None}
    expanded = 0
    while frontier:
        f, number, g, state = heapq.heappop(frontier)
        if g != g_costs[state]:
            continue  # stale entry, a cheaper route was found later
        if state == goal:
            return SearchResult(reconstruct_path(parents, goal), expanded)
        expanded += 1
        for action, successor in campus.neighbors(state):
            new_g = g + 1
            if successor not in g_costs or new_g < g_costs[successor]:
                g_costs[successor] = new_g
                parents[successor] = state
                new_f = new_g + manhattan(successor, goal)
                heapq.heappush(frontier, (new_f, next(order), new_g, successor))
    return SearchResult(None, expanded)


def epsilon_greedy(q_values, state, actions, epsilon, rng):
    """TODO 3: Choose an action with epsilon-greedy exploration."""
    # q_values is a dictionary. Its keys are (state, action) pairs.
    # Example key: ((1, 1), "RIGHT"). Unseen entries have value 0.0.
    if rng.random() < epsilon:
        return rng.choice(actions)
    best_value = max(q_values.get((state, action), 0.0) for action in actions)
    best_actions = [action for action in actions
                    if q_values.get((state, action), 0.0) == best_value]
    return rng.choice(best_actions)


def q_learning_update(q_values, state, action, reward, next_state,
                      actions, alpha, gamma, terminal):
    """TODO 4: Update exactly one Q-table entry in place; return nothing."""
    # Get Q(state, action), defaulting to 0.0.
    # If terminal is True, the target is reward with no continuation term.
    # Otherwise target = reward + gamma * max Q(next_state, next_action).
    # Consider every action, including unseen entries with value 0.0.
    # Apply Q <- Q + alpha * (target - Q).
    old_value = q_values.get((state, action), 0.0)
    if terminal:
        target = reward
    else:
        next_best = max(q_values.get((next_state, next_action), 0.0)
                        for next_action in actions)
        target = reward + gamma * next_best
    q_values[(state, action)] = old_value + alpha * (target - old_value)
