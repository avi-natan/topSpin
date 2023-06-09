import heapq


def calculate_priority(priority_function, heuristic_function):
    """Calculates the priority of a node using the given priority and heuristic functions"""

    def priority(g, successor):
        return priority_function(g, heuristic_function(successor))

    return priority


def get_state_index(states, target_state):
    """Returns the index of the target_state in the priority_queue"""
    for index, state in enumerate(states):
        if state[0] == target_state:
            return index
    return -1  # Return -1 if not found


def search(start, priority_function, heuristic_function):
    # easy function to calculate the priority of a node
    get_priority = calculate_priority(priority_function, heuristic_function)

    close_list = set()

    # put the start node in the queue
    priority_queue = []  # list of tuples (priority, g, Nan, path_to, state)
    heapq.heappush(priority_queue, (0, 0, 0, [start], start))

    i = 0
    evaluation = 0
    # while Q is not empty
    while len(priority_queue) > 0:
        # get the state with the highest priority
        _, g, _, path_to, state = heapq.heappop(priority_queue)

        # if state is the goal node
        if state.is_goal():
            # return n
            return (path_to, evaluation)

        # generate state's successors
        successors = state.get_neighbors()

        # for each successor of state
        j = 0
        for successor in successors:
            new_g = g + successor[1]
            successor = successor[0]

            if successor in close_list:
                continue

            index = get_state_index(priority_queue, successor)
            priority = get_priority(g, successor)

            # if successor is not in priority_queue
            if index == -1:
                heapq.heappush(
                    priority_queue,
                    (priority, new_g, i * 10 + j, path_to + [successor], successor),
                )
            # else if successor is in priority_queue with a lower g
            elif priority_queue[index][1] > new_g:
                priority_queue.pop(index)
                heapq.heappush(
                    priority_queue,
                    (priority, new_g, i * 10 + j, path_to + [successor], successor),
                )

            j += 1

        i += 1
        evaluation += 1
        close_list.add(state)

    return (None, 0)
