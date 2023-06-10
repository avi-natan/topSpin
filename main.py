import random
from datetime import datetime

from heuristics import BaseHeuristic, AdvanceHeuristic
from priorities import f_priority
from search import search
from topspin import TopSpinState

# instance_0 = [3, 2, 1]
instance_1 = [1, 7, 10, 3, 6, 9, 5, 8, 2, 4, 11]  # easy instance
# instance_2 = [1, 5, 11, 2, 6, 3, 9, 4, 10, 7, 8]  # hard instance
# instance_3 = [1, 7, 3, 6, 5, 8, 2, 4]

# start = TopSpinState(instance_0, 2)
# heuristic = BaseHeuristic(3, 2)
# heuristic = AdvanceHeuristic(3, 2)
start = TopSpinState(instance_1, 4)
# heuristic = BaseHeuristic(11, 4)
heuristic = AdvanceHeuristic(11, 4)
# start = TopSpinState(instance_3, 4)
# heuristic = BaseHeuristic(8, 4)
# heuristic = AdvanceHeuristic(8, 4)

start_time = datetime.now()
path, expansions = search(start, f_priority, heuristic.get_h_value)
end_time = datetime.now()
delta = end_time - start_time

print(f'time to finish: {delta}')

if path is not None:
    print(expansions)
    for vertex in path:
        print(vertex.get_state_as_list())
else:
    print("unsolvable")
