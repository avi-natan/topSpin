import heapq


def calculate_priority(priority_function, heuristic_function):
    """Calculates the priority of a node using the given priority and heuristic functions"""

    def priority(g, successor):
        return priority_function(g, heuristic_function(successor))

    return priority


def get_state_index(states, target_state):
    """Returns the index of the target_state in the priority_queue"""
    for index, state in enumerate(states):
        if state[5] == target_state:
            return index
    return -1  # Return -1 if not found


def search(start, priority_function, heuristic_function):
    # easy function to calculate the priority of a node
    get_priority = calculate_priority(priority_function, heuristic_function)

    close_list = []

    # put the start node in the queue
    priority_queue = []  # list of tuples (priority, g, Nan, path_to, state, state_as_list)
    heapq.heappush(priority_queue, (0, 0, 0, [start], start, start.get_state_as_list()))

    i = 0
    evaluation = 0
    # while Q is not empty
    while len(priority_queue) > 0:
        # debug prints - length of open list
        if len(priority_queue) % 100 == 0:
            print(len(priority_queue))
        # print('\n')

        # get the state with the highest priority
        pr, g, na, path_to, state, state_as_list = heapq.heappop(priority_queue)

        # if state is the goal node
        if state.is_goal():
            # return n
            return (path_to, evaluation)

        # generate state's successors
        successors = state.get_neighbors()

        # for each successor of state
        j = 0
        for successor in successors:
            successor_as_list = successor.get_state_as_list()
            if successor_as_list in close_list:
                continue

            index = get_state_index(priority_queue, successor_as_list)

            # if successor is not in priority_queue
            if index == -1:
                new_g = g + 1
                priority = get_priority(new_g, successor)
                heapq.heappush(
                    priority_queue,
                    (priority, new_g, i * 10 + j, path_to + [successor], successor, successor_as_list),
                )
            # else if successor is in priority_queue with a lower g
            else:
                new_g = g + 1
                if priority_queue[index][1] > new_g:
                    priority = get_priority(new_g, successor)
                    priority_queue.pop(index)
                    heapq.heappush(
                        priority_queue,
                        (priority, new_g, i * 10 + j, path_to + [successor], successor, successor_as_list),
                    )

            j += 1

        i += 1
        evaluation += 1
        close_list.append(state.get_state_as_list())

    return (None, 0)
