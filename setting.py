def load_game_setting(difficulty):
    if difficulty == 0:
        nr_cols = 5
        nr_rows = 5
        walls = [(1, 1), (1, 2), (2, 1), (2, 2)]
        red_block_pos_l = [(4, 1)]
        green_block_pos_l = [(4, 0)]
        cell_width = 100
    elif difficulty == 1:
        nr_cols = 8
        nr_rows = 8
        walls = [(2, 2), (2, 3), (3, 2), (3, 3), (6, 4), (6, 5)]
        red_block_pos_l = [(7, 2), (6, 2)]
        green_block_pos_l = [(7, 0)]
        cell_width = 100
    else:
        nr_cols = 15
        nr_rows = 15
        walls = [(2, 2), (2, 3), (3, 2), (3, 3), (6, 4), (6, 5), (8, 8), (8, 9), (9, 8), (9, 9)]
        red_block_pos_l = [(14, 1), (13, 1)]
        green_block_pos_l = [(14, 0)]
        cell_width = 50

    return nr_cols, nr_rows, walls, red_block_pos_l, green_block_pos_l, cell_width
