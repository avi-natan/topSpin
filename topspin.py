
class TopSpinState:

    def __init__(self, state, k=4):
        self.k = k
        self.state = state

    def is_goal(self):
        return sorted(self.state) == self.state

    def get_state_as_list(self):
        return self.state

    def get_neighbors(self):
        # 3 neighbours: left rotate, right rotate, and k flip
        l_rotate = self.state[1:] + [self.state[0]]
        r_rotate = [self.state[-1]] + self.state[:-1]
        k_flip = self.state[:self.k][::-1] + self.state[self.k:]

        return [TopSpinState(l_rotate,self.k), TopSpinState(r_rotate,self.k), TopSpinState(k_flip,self.k)]
