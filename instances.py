import random

class InstanceGenerator:
    def __init__(self, n=11, k=4):
        self._n = n
        self._k = k

    def generate_instance(self, m):
        state_as_list = [i for i in range(1, self._n+1)]

        for i in range(m):
            action = random.randint(1, 3)
            if action == 1:
                # left rotate
                state_as_list = state_as_list[1:] + [state_as_list[0]]
            elif action == 2:
                # right rotate
                state_as_list = [state_as_list[-1]] + state_as_list[:-1]
            elif action == 3:
                # k flip
                state_as_list = state_as_list[: self._k][::-1] + state_as_list[self._k:]
            else:
                raise Exception("Invalid action number")

        return state_as_list
