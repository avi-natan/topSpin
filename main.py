import random
from datetime import datetime

from heuristics import BaseHeuristic, AdvanceHeuristic
from instances import InstanceGenerator
from priorities import f_priority, fw_priority, h_priority
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

algs_and_heuristics = [
    ('A* basic', f_priority, base_heuristic, [], [], []),
    ('A* advanced', f_priority, adva_heuristic, [], [], []),
    ('WA* basic', fw_priority(5), base_heuristic, [], [], []),
    ('WA* advanced', fw_priority(5), adva_heuristic, [], [], []),
    ('GBFS basic', h_priority, base_heuristic, [], [], []),
    ('GBFS advanced', h_priority, adva_heuristic, [], [], [])
]

instances_num = 50
for i in range(instances_num):
    random_instance = instance_generator.generate_instance(m)
    start = TopSpinState(random_instance, k)

    for a_and_h in algs_and_heuristics:
        start_time = datetime.now()
        path, expansions = search(start, a_and_h[1], a_and_h[2].get_h_value)
        end_time = datetime.now()
        delta = end_time - start_time

        print(a_and_h[0])
        print(f'time to finish: {delta}')

        a_and_h[3].append(delta.total_seconds())
        a_and_h[4].append(len(path)) if path is not None else a_and_h[4].append(-1)
        a_and_h[5].append(expansions)

        if path is not None:
            print(expansions)
            for vertex in path:
                print(vertex.get_state_as_list())
        else:
            print("unsolvable")

for a_and_h in algs_and_heuristics:
    print(f'heuristic: {a_and_h[0]}')
    print(f'runtimes: {a_and_h[3]}')
    print(f'average runtime: {sum(a_and_h[3]) / instances_num}')
    print(f'path lengths: {a_and_h[4]}')
    print(f'average path lengths: {sum(a_and_h[4]) / instances_num}')
    print(f'expansions: {a_and_h[5]}')
    print(f'average expansions: {sum(a_and_h[5]) / instances_num}')
    print(f'number of cases solved: {len(list(filter(lambda a: a != -1, a_and_h[4])))}/{instances_num}')
