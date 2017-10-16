import argparse
from Tkinter import Tk
from environment import Env
from setting import load_game_setting

# input parameter
parser = argparse.ArgumentParser(description="Awesome Game")
parser.add_argument('--random')
parser.add_argument('--difficulty', type=int, help='difficult of the environment', default=0)
args = parser.parse_args()

# load game difficulty setting
nr_cols, nr_rows, walls, red_block_pos_l, green_block_pos_l, cell_width = load_game_setting(args.difficulty)

# start environment
master = Tk()
env = Env(master, args.random is not None, nr_cols, nr_rows, walls, red_block_pos_l, green_block_pos_l, cell_width)
env.render_grid()
master.mainloop()
