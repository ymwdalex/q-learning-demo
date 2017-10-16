import time
import numpy as np


class Agent():
    def __init__(self, env, max_iteration=20, time_interval=50):
        self.env = env
        self.time_interval = time_interval  # ms

        self.Q = self.init_Q()
        self.discount = 0.8
        self.alpha = 1
        self.nr_iter = 1
        self.max_iteration = max_iteration

        self.total_reward = []

    def init_Q(self):
        nr_rows = self.env.nr_rows
        nr_cols = self.env.nr_cols
        nr_actions = len(self.env.actions)

        return np.zeros((nr_actions, nr_rows, nr_cols))

    def get_current_state(self):
        """
        Get current state: (col, row)
        N.B. first column, then row
        """
        return self.env.get_player_position()

    def get_action_by_Q(self, state):
        """
        Get best action in current state
        """
        col, row = state
        winner = np.where(self.Q[:, row, col] == self.Q[:, row, col].max())[0]
        return np.random.choice(winner, 1)[0]

    def move(self, action):
        """
        Given state and action, get reward and next state
        Input:
            action: [0, 4)
        Output:
            reward:
            next_state:
        """
        return self.env.response_action(action)

    def update_Q(self, state, action, reward, next_state):
        # print state, action, reward, next_state, alpha
        # get maximum Q value of next state
        next_col, next_row = next_state
        max_val = self.Q[:, next_row, next_col].max()

        col, row = state
        self.Q[action, row, col] = ((1 - self.alpha) * self.Q[action, row, col] +
                                    self.alpha * (reward + self.discount * max_val))

    def update_alpha(self):
        self.alpha = pow(self.nr_iter, -0.1)

    def learn(self):
        # get current state
        state = self.get_current_state()

        # Pick the right action
        best_action = self.get_action_by_Q(state)

        # Make the movement
        reward, next_state, terminal, total_score = self.move(best_action)

        # Update Q
        self.update_Q(state, best_action, reward, next_state)
        # print self.Q

        # Check if the game has restarted
        if terminal:
            self.total_reward.append(total_score)
            self.env.restart_game(None)
            self.nr_iter += 1.0
            print "iteration {}".format(self.nr_iter)
            time.sleep(1)

        # Update the learning rate
        self.update_alpha()

        # register agent learning function
        if self.nr_iter <= self.max_iteration:
            self.env.master.after(self.time_interval, self.learn)
        else:
            self.env.master.destroy()
