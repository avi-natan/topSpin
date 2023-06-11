from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy as np


class BaseHeuristic:
    def __init__(self, n=11, k=4):
        self._n = n
        self._k = k

    def get_h_value(self, state):
        state_as_list = state.get_state_as_list()
        gap = 0

        if state_as_list[0] != 1:
            gap = 1

        for i in range(len(state_as_list) - 1):
            if abs(state_as_list[i] - state_as_list[i + 1]) != 1:
                gap += 1

        return gap


class AdvanceHeuristic:
    def __init__(self, n=11, k=4):
        self._n = n
        self._k = k

    def get_h_value(self, state):
        # # this heuristics counts the combined distance of the tiles to their goal position
        # state_as_list = state.get_state_as_list()
        # h = 0
        #
        # for i, tile in enumerate(state_as_list[:self._k]):
        #     h += abs(tile - i + 1)
        #
        # return h

        # state_as_list = state.get_state_as_list()
        # h = abs(sum(state_as_list[:self._k]) - sum(range(1, self._k + 1)))
        # for i, tile in enumerate(state_as_list[:self._k]):
        #     h += abs(tile - i + 1)
        # h += abs(state_as_list[0] - state_as_list[-1])
        # # h = abs(sum(state_as_list[self._k:]) - sum(range(self._k, self._n+1)))
        # # h = abs(abs(sum(state_as_list[self._k:]) - sum(range(self._k, self._n+1))) - abs(sum(state_as_list[:self._k]) - sum(range(1, self._k + 1))))

        state_as_list = state.get_state_as_list()
        gap = 0

        if state_as_list[0] != 1:
            gap = 1

        for i in range(len(state_as_list) - 1):
            if abs(state_as_list[i] - state_as_list[i + 1]) != 1:
                gap += 2

        if abs(state_as_list[0] - state_as_list[-1]) != self._n-1 or abs(state_as_list[0] - state_as_list[-1]) != 1:
            gap += 1

        return gap


class LearnedHeuristic:
    def __init__(self, n=11, k=4):
        self._n = n
        self._k = k
        input_shape = (n,)

        self._model = Sequential()
        self._model.add(Dense(64, activation="relu", input_shape=input_shape))
        self._model.add(Dropout(0.25))
        self._model.add(Dense(32, activation="relu"))
        self._model.add(Dropout(0.25))
        self._model.add(Dense(16, activation="relu"))
        self._model.add(Dense(1, activation="linear"))

        self._model.compile(loss="mse", optimizer="adam")

        # don't forget to load the model after you trained it

    def get_h_value(self, state):
        state = np.array(state.get_state_as_list())
        state = state.reshape(1, self._n)
        return self._model.predict(state, verbose=0)[0][0]

    def train_model(self, input_data, output_labels, epochs=100):
        input_as_list = [state.get_state_as_list() for state in input_data]
        self._model.fit(input_as_list, output_labels, epochs=epochs)

    def save_model(self):
        self._model.save_weights("models/learned_heuristic.h5")

    def load_model(self):
        self._model.load_weights("models/learned_heuristic.h5")
