import heapq
import hashlib
import json


def generate_unique_hash(data):
    # Convert the list to bytes
    data_bytes = json.dumps(data).encode("utf-8")

    # Create a new SHA-256 hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the data bytes
    hash_object.update(data_bytes)

    # Get the hexadecimal representation of the hash
    unique_hash = hash_object.hexdigest()

    return unique_hash


def calculate_priority(priority_function, heuristic_function):
    """Calculates the priority of a node using the given priority and heuristic functions"""

    def priority(g, successor):
        return priority_function(g, heuristic_function(successor))

    return priority


def search(start, priority_function, heuristic_function):
    # Easy function to calculate the priority of a node
    get_priority = calculate_priority(priority_function, heuristic_function)

    close_list = set()
    priority_queue = []  # Dictionary to store states and their priorities

    # Put the start node in the queue
    start_state_list = start.get_state_as_list()
    start_state_hash = generate_unique_hash(start_state_list)
    heapq.heappush(
        priority_queue,
        (
            0,
            0,
            0,
            (None, start),
            start,
            start_state_hash,
        ),
    )

    i = 0
    evaluation = 0
    # While the priority queue is not empty
    while priority_queue:
        # Get the state with the highest priority
        pr, g, na, path_to, state, state_as_list = heapq.heappop(priority_queue)

        # If state is the goal node
        if state.is_goal():
            # Return the path and evaluation
            path = []
            while path_to is not None:
                path.insert(0, path_to[1])
                path_to = path_to[0]
            return (path, evaluation)

        # Generate state's successors
        successors = state.get_neighbors()

        # Check if the state has been visited before
        if state_as_list in close_list:
            continue

        # Add the state to the close list
        close_list.add(state_as_list)

        # For each successor of state
        j = 0
        for successor_tuple in successors:
            successor = successor_tuple[0]
            successor_cost = successor_tuple[1]
            successor_as_list = generate_unique_hash(successor.get_state_as_list())

            # Check if successor is in the priority queue
            if successor_as_list not in priority_queue:
                new_g = g + successor_cost
                priority = get_priority(new_g, successor)
                heapq.heappush(
                    priority_queue,
                    (
                        priority,
                        new_g,
                        i * 10 + j,
                        (path_to, successor),
                        successor,
                        successor_as_list,
                    ),
                )
            # If successor is in priority_queue with a lower g
            elif priority_queue[successor_as_list][1] > g + successor_cost:
                new_g = g + successor_cost
                priority = get_priority(new_g, successor)
                priority_queue[successor_as_list] = (
                    priority,
                    new_g,
                    i * 10 + j,
                    (path_to, successor),
                    successor,
                    successor_as_list,
                )

            j += 1

        i += 1
        evaluation += 1

    return (None, 0)
