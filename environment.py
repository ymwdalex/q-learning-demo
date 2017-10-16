import random
from Tkinter import Canvas


class Env():
    def __init__(self,
                 master,
                 random_start_pos=False,
                 nr_cols=5,
                 nr_rows=5,
                 walls=[(1, 1), (1, 2), (2, 1), (2, 2)],
                 red_block_pos_l=[(4, 1)],
                 green_block_pos_l=[(4, 0)],
                 cell_width=100):
        self.master = master

        ############################
        # Game setting
        self.nr_cols, self.nr_rows = (nr_cols, nr_rows)
        self.actions = ["up", "down", "left", "right"]
        self.walk_reward = -0.04

        # Walls
        self.walls = walls

        # Red Grid
        self.red_block_pos_l = red_block_pos_l
        # Green Grid
        self.green_block_pos_l = green_block_pos_l
        self.special_grids = [(red[0], red[1], "red", -1) for red in self.red_block_pos_l] + \
                             [(green[0], green[1], "green", 1) for green in self.green_block_pos_l]

        ########################
        # player setting
        self.player_pos = (0, self.nr_rows-1)

        # random start position or not
        self.random_start_pos = random_start_pos

        # Score
        self.score = 1

        # Terminal flag
        self.terminal = False

        #############################################
        # Game UI configuration
        self.triangle_size = 0.1
        self.cell_width = cell_width
        self.board = Canvas(self.master,
                            width=self.nr_cols*self.cell_width,
                            height=self.nr_rows*self.cell_width)
        self.board.grid(row=0, column=0)
        # cell_score_min = -0.2
        # cell_score_max = 0.2

        # Special grid setting
        self.cell_scores = {}

        # key bind setting
        self.master.bind("<Up>", self.call_up)
        self.master.bind("<Down>", self.call_down)
        self.master.bind("<Right>", self.call_right)
        self.master.bind("<Left>", self.call_left)
        self.master.bind('<Escape>', lambda e: self.master.destroy())
        self.master.bind('<space>', self.restart_game)

        return

    def call_up(self, event):
        return self.try_move(0, -1)

    def call_down(self, event):
        return self.try_move(0, 1)

    def call_left(self, event):
        return self.try_move(-1, 0)

    def call_right(self, event):
        return self.try_move(1, 0)

    def response_action(self, action):
        # self.actions = ["up", "down", "left", "right"]
        # print "Action: {}".format(self.actions[action])
        if action == 0:
            return self.call_up(None)
        if action == 1:
            return self.call_down(None)
        if action == 2:
            return self.call_left(None)
        if action == 3:
            return self.call_right(None)

    def restart_game(self, _):
        self.init_player_pos()
        self.score = 1
        self.terminal = False
        self.board.coords(self.me,
                          self.player_pos[0]*self.cell_width+self.cell_width*2/10,
                          self.player_pos[1]*self.cell_width+self.cell_width*2/10,
                          self.player_pos[0]*self.cell_width+self.cell_width*8/10,
                          self.player_pos[1]*self.cell_width+self.cell_width*8/10)

    def init_player_pos(self):
        if self.random_start_pos:
            while True:
                new_x = random.randint(0, self.nr_cols-1)
                new_y = random.randint(0, self.nr_rows-1)
                if not((new_x, new_y) in self.walls or
                        (new_x, new_y) == self.red_block_pos_l or
                        (new_x, new_y) == self.green_block_pos_l):
                    self.player_pos = (new_x, new_y)
                    break
            print self.player_pos
        else:
            self.player_pos = (0, self.nr_rows-1)

    def get_player_position(self):
        return self.player_pos

    def render_grid(self):
        for i in range(self.nr_cols):
            for j in range(self.nr_rows):
                self.board.create_rectangle(i*self.cell_width,
                                            j*self.cell_width,
                                            (i+1)*self.cell_width,
                                            (j+1)*self.cell_width,
                                            fill="white",
                                            width=1)
                # temp = {}
                # for action in self.actions:
                #     temp[action] = create_triangle(i, j, action)
                # self.cell_scores[(i,j)] = temp

        for (i, j, c, w) in self.special_grids:
            self.board.create_rectangle(i*self.cell_width,
                                        j*self.cell_width,
                                        (i+1)*self.cell_width,
                                        (j+1)*self.cell_width,
                                        fill=c,
                                        width=1)

        for (i, j) in self.walls:
            self.board.create_rectangle(i*self.cell_width, j*self.cell_width, (i+1)*self.cell_width, (j+1)*self.cell_width, fill="black", width=1)

        self.me = self.board.create_rectangle(self.player_pos[0]*self.cell_width+self.cell_width*2/10,
                                              self.player_pos[1]*self.cell_width+self.cell_width*2/10,
                                              self.player_pos[0]*self.cell_width+self.cell_width*8/10,
                                              self.player_pos[1]*self.cell_width+self.cell_width*8/10,
                                              fill="orange",
                                              width=1,
                                              tag="me")

    def try_move(self, dx, dy):
        reward = self.walk_reward

        # always update reward
        self.score += self.walk_reward

        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        # see if a valid move
        if new_x >= 0 and new_x < self.nr_cols and \
           new_y >= 0 and new_y < self.nr_rows and \
           not ((new_x, new_y) in self.walls):
            self.board.coords(self.me,
                              new_x*self.cell_width+self.cell_width*2/10,
                              new_y*self.cell_width+self.cell_width*2/10,
                              new_x*self.cell_width+self.cell_width*8/10,
                              new_y*self.cell_width+self.cell_width*8/10)
            self.player_pos = (new_x, new_y)

            for (i, j, c, w) in self.special_grids:
                if self.player_pos[0] == i and self.player_pos[1] == j:
                    self.score -= self.walk_reward
                    self.score += w
                    reward = w
                    if self.score > 0:
                        print "Success! self.score: ", self.score
                    else:
                        print "Fail! self.score: ", self.score
                    self.terminal = True
                    break

        print "Reward: {}\tPosition: {}\tTerminal: {}\tScore: {}".format(reward, self.player_pos, self.terminal, self.score)
        return reward, self.player_pos, self.terminal, self.score

    # def create_triangle(self, i, j, action):
    #     if action == self.actions[0]:
    #         return self.board.create_polygon((i+0.5-self.triangle_size)*self.cell_width,
    #                                          (j+self.triangle_size)*self.cell_width,
    #                                          (i+0.5+self.triangle_size)*self.cell_width,
    #                                          (j+self.triangle_size)*self.cell_width,
    #                                          (i+0.5)*self.cell_width, j*self.cell_width,
    #                                          fill="white", width=1)
    #     elif action == self.actions[1]:
    #         return self.board.create_polygon((i+0.5-self.triangle_size)*self.cell_width,
    #                                          (j+1-self.triangle_size)*self.cell_width,
    #                                          (i+0.5+self.triangle_size)*self.cell_width,
    #                                          (j+1-self.triangle_size)*self.cell_width,
    #                                          (i+0.5)*self.cell_width,
    #                                          (j+1)*self.cell_width,
    #                                          fill="white",
    #                                          width=1)
    #     elif action == self.actions[2]:
    #         return self.board.create_polygon((i+self.triangle_size)*self.cell_width,
    #                                          (j+0.5-self.triangle_size)*self.cell_width,
    #                                          (i+self.triangle_size)*self.cell_width,
    #                                          (j+0.5+self.triangle_size)*self.cell_width,
    #                                          i*self.cell_width,
    #                                          (j+0.5)*self.cell_width,
    #                                          fill="white",
    #                                          width=1)
    #     elif action == self.actions[3]:
    #         return self.board.create_polygon((i+1-self.triangle_size)*self.cell_width,
    #                                          (j+0.5-self.triangle_size)*self.cell_width,
    #                                          (i+1-self.triangle_size)*self.cell_width,
    #                                          (j+0.5+self.triangle_size)*self.cell_width,
    #                                          (i+1)*self.cell_width, (j+0.5)*self.cell_width,
    #                                          fill="white",
    #                                          width=1)

    # def set_cell_score(self, state, action, val):
    #     global cell_score_min, cell_score_max
    #     triangle = self.cell_scores[state][action]
    #     green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    #     green = hex(green_dec)[2:]
    #     red = hex(255-green_dec)[2:]
    #     if len(red) == 1:
    #         red += "0"
    #     if len(green) == 1:
    #         green += "0"
    #     color = "#" + red + green + "00"
    #     self.board.itemconfigure(triangle, fill=color)
