# -*- coding: utf-8 -*-
import numpy as np
from collections import defaultdict


def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
    the coordinate of the upper left corner of pi in the board (lowest row and column index 
    that the tile covers).
    
    -Use np.flip and np.rot90 to manipulate pentominos.
    
    -You can assume there will always be a solution.
    """
    # make a copy of the parameter board
    board = np.array(board)

    # change the board a litte to be compatible with the pents
    board[board == 0] = -1
    board[board == 1] = 0

    # one pent has 8 mutations in most, get all of them in a dict
    # also change the representation of a pent, to a list of tuples(coordinates), making the search faster
    pents_map = {}
    for p in pents:
        pents_map[get_pent_label(p)] = get_all_mutations(p)

    # get the result board first
    _, res_board = dfs(board, board.shape, dict(pents_map))
    print(res_board)

    # use the board to determine the final layout to return
    pents_coords = defaultdict(list)
    for x, y in np.ndindex(res_board.shape):
        if res_board[x][y] in pents_map:
            pents_coords[res_board[x][y]].append((x, y))

    sol = []

    for plabel, coords in pents_coords.items():
        min_x, max_x, min_y, max_y = coords[0][0], coords[0][0], coords[0][1], coords[0][1]

        for coord in coords:
            min_x, max_x = min(min_x, coord[0]), max(max_x, coord[0])
            min_y, max_y = min(min_y, coord[1]), max(max_y, coord[1])

        piece = np.zeros((max_x - min_x + 1, max_y - min_y + 1))

        for coord in coords:
            piece[coord[0] - min_x][coord[1] - min_y] = plabel

        sol.append((piece.astype(int), (min_x, min_y)))

    return sol


def in_bound(board_shape, x, y):
    return 0 <= x < board_shape[0] and 0 <= y < board_shape[1]


def dfs(board, board_shape, pents_map):
    if not pents_map:
        return True, board

    for x, y in ((x, y) for y in range(board_shape[1]) for x in range(board_shape[0])):
        # find the the first unfilled position to add a pent
        if board[x][y] == 0:
            # try all the rest pents one by one
            for p, mutations in pents_map.items():
                # try all the mutations of a pent
                for mutation in mutations:
                    to_continue = False

                    # check if it's possible to add the pent on the board
                    for x_move, y_move in mutation:
                        if not in_bound(board_shape, x + x_move, y + y_move) or board[x + x_move][y + y_move] != 0:
                            to_continue = True
                            break

                    # continue to the next loop if we cannot add a new pent
                    if to_continue:
                        continue

                    # make copies of board and the rest pents to make backtracking easier
                    new_board = np.array(board)

                    new_pents_map = dict(pents_map)
                    new_pents_map.pop(p)

                    # add the pent to the board
                    for x_move, y_move in mutation:
                        new_board[x + x_move][y + y_move] = p

                    found, res_board = dfs(new_board, board_shape, new_pents_map)

                    if found:
                        return True, res_board

            return False, board


def get_all_mutations(pent):
    # use a set to remove duplicates
    mutations = set()
    for flipnum in range(3):
        p = np.copy(pent)

        if flipnum > 0:
            p = np.flip(pent, flipnum - 1)
        for rot_num in range(4):
            p = np.rot90(p)
            mutations.add(get_one_mutation(p))

    return list(mutations)


def get_one_mutation(mutation):
    """
    get the relative representation of one mutation, store in a list of coordinates
    """
    coords = tuple()
    for x, y in np.ndindex(mutation.shape):
        if mutation[x][y] != 0:
            coords += ((x, y),)

    origin = coords[0]

    for coord in coords:
        if coord[1] < origin[1]:
            origin = coord
        elif coord[1] == origin[1] and coord[0] < origin[0]:
            origin = coord

    mutation = tuple()
    for coord in coords:
        mutation += ((coord[0] - origin[0], coord[1] - origin[1]), )

    return tuple(sorted(mutation))

def get_pent_label(pent):
    """
    Returns the label of a pentomino.
    """
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if pent[i][j] != 0:
                plabel = pent[i][j]
                break
        if plabel != 0:
            break
    return plabel
