# Copyright © 2023 Kaj Habegger, Fabio Lenherr
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import torch
import numpy as np
from collections import deque
from game import PySnake

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNINGRATE = 0.001


class Agent:

    def __init__(self) -> None:
        self.game_amount = 0
        self.epsilon = 0 # controls randomness
        self.gamma = 0 #discount
        self.memory = deque(maxlen=MAX_MEMORY)
        # if memory exceeded automatically removes it on the left

    def get_state(self, game):
        pass

    def remember(self,state,action,reward,next_state,done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self,state,action,reward,next_state,done):
        pass

    def get_action(self, state):
        pass

def train():
    scores = []
    mean_scores = []
    current_score = 0
    best_score = 0
    agent = Agent()
    game = PySnake() 
    while(True):
        #get old state
        old_state = agent.get_state(game)
        # evaluate next action
        move = agent.get_action(old_state)
        # perform new state 
        reward, done, score = game.ai_input(move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory()




if __name__ == '__main__':
    train()
