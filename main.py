import random
from datetime import datetime

from heuristics import BaseHeuristic, AdvanceHeuristic
from instances import InstanceGenerator
from priorities import f_priority
from search import search
from topspin import TopSpinState

# # instance_0 = [3, 2, 1]
# # instance_1 = [1, 7, 10, 3, 6, 9, 5, 8, 2, 4, 11]  # easy instance
# # instance_2 = [1, 5, 11, 2, 6, 3, 9, 4, 10, 7, 8]  # hard instance
# instance_3 = [1, 7, 3, 6, 5, 8, 2, 4]
#
# # start = TopSpinState(instance_0, 2)
# # heuristic = BaseHeuristic(3, 2)
# # heuristic = AdvanceHeuristic(3, 2)
# # start = TopSpinState(instance_1, 4)
# # heuristic = BaseHeuristic(11, 4)
# # heuristic = AdvanceHeuristic(11, 4)
# start = TopSpinState(instance_3, 4)
# # heuristic = BaseHeuristic(8, 4)
# heuristic = AdvanceHeuristic(8, 4)
#
# start_time = datetime.now()
# path, expansions = search(start, f_priority, heuristic.get_h_value)
# end_time = datetime.now()
# delta = end_time - start_time
#
# # print('instance_0')
# # print('instance_1')
# # print('instance_2')
# print('instance_3')
#
# # print('base heuristic')
# print('advanced heuristic')
# print(f'time to finish: {delta}')
#
# if path is not None:
#     print(expansions)
#     for vertex in path:
#         print(vertex.get_state_as_list())
# else:
#     print("unsolvable")

########################## pipeline ############################
n = 8
k = 4
m = 100
instance_generator = InstanceGenerator(n,k)
base_heuristic = BaseHeuristic(n, k)
adva_heuristic = AdvanceHeuristic(n, k)

heuristics = [('Base Heuristic', base_heuristic, []), ('Advanced Heuristic',adva_heuristic, [])]

instances_num = 50
for i in range(instances_num):
    random_instance = instance_generator.generate_instance(m)
    start = TopSpinState(random_instance, k)

    for heuristic in heuristics:
        start_time = datetime.now()
        path, expansions = search(start, f_priority, heuristic[1].get_h_value)
        end_time = datetime.now()
        delta = end_time - start_time

        print(heuristic[0])
        print(f'time to finish: {delta}')

        heuristic[2].append(delta.total_seconds())

        if path is not None:
            print(expansions)
            for vertex in path:
                print(vertex.get_state_as_list())
        else:
            print("unsolvable")

for heuristic in heuristics:
    print(f'heuristic: {heuristic[0]}')
    print(f'runtimes: {heuristic[2]}')
    print(f'average: {sum(heuristic[2]) / instances_num}')
