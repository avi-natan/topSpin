import random

from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy as np

from instances import InstanceGenerator
from topspin import TopSpinState


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
        state_as_list = state.get_state_as_list()
        gap = 0

        if state_as_list[0] != 1:
            gap = 1

        for i in range(len(state_as_list) - 1):
            if abs(state_as_list[i] - state_as_list[i + 1]) != 1:
                gap += self._k

        if abs(state_as_list[0] - state_as_list[-1]) != self._n-1 or abs(state_as_list[0] - state_as_list[-1]) != 1:
            gap += 2

        if abs(state_as_list[0] - state_as_list[self._k]) != self._k or abs(state_as_list[0] - state_as_list[self._k]) != 1:
            gap += 1

        return gap


class LearnedHeuristic:
    def __init__(self, n=11, k=4):
        self._n = n
        self._k = k
        input_shape = (n,)

        self._model = Sequential()
        self._model.add(Dense(64, activation="relu", input_shape=input_shape))
        self._model.add(Dropout(0.05))
        self._model.add(Dense(32, activation="relu"))
        self._model.add(Dropout(0.05))
        self._model.add(Dense(16, activation="relu"))
        self._model.add(Dense(1, activation="linear"))

        self._model.compile(loss="mse", optimizer="adam")

        # don't forget to load the model after you trained it
        try:
            self.load_model()
        except Exception as e:
            pass

        adva_heuristic = AdvanceHeuristic(n, k)
        instance_generator = InstanceGenerator(n,k)
        input_data_as_list = [instance_generator.generate_instance(random.randint(1, K + 1)) for K in range(100000)]
        input_data = list(map(lambda state_as_list: TopSpinState(state_as_list, k), input_data_as_list))
        output_labels = []
        for i, state in enumerate(input_data):
            output_labels.append(adva_heuristic.get_h_value(state))
            print(f'========================================== {i}')

        self.train_model(input_data, output_labels, 100)
        self.save_model()


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
