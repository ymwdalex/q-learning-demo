import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from Tkinter import Tk
from environment import Env
from agent import Agent
from setting import load_game_setting

# input parameter
parser = argparse.ArgumentParser(description="Awesome Game")
parser.add_argument('--random')
parser.add_argument('--difficulty', type=int, help='difficult of the environment', default=0)
parser.add_argument('--max-iteration', dest='max_iteration', type=int, help='maximun iteration', default=20)
args = parser.parse_args()

# load game difficulty setting
nr_cols, nr_rows, walls, red_block_pos_l, green_block_pos_l, cell_width = load_game_setting(args.difficulty)

# start a Tkinter
master = Tk()

# register tkinter instance in the environment
env = Env(master, args.random is not None, nr_cols, nr_rows, walls, red_block_pos_l, green_block_pos_l, cell_width)

# Draw the game board
env.render_grid()

# Initial an agent
agent = Agent(env, args.max_iteration)

# start learning
agent.learn()

# start the UI loop
master.mainloop()

sns.set_style("darkgrid")
plt.plot(np.array(agent.total_reward))
plt.show()