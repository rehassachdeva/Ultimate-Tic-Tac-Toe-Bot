import sys
import random
import signal
import copy
import time

class Player23:
    
        def __init__(self):

            self.maxdepth = 5

            self.came = 0

            self.timed_out = False;

            self.inf = 1000000000000

            self.threshold = [2, 5.9, 3.9, 0]
            
            self.win_pos = [
                    (0, 1, 2),
                    (3, 4, 5),
                    (6, 7, 8),
                    (0, 3, 6),
                    (1, 4, 7),
                    (2, 5, 8),
                    (0, 4, 8),
                    (2, 4, 6)
                    ]

            self.twos = []

	    for each in self.win_pos:
                self.twos.append((each[0],each[1],each[2]))
                self.twos.append((each[1],each[2],each[0]))
                self.twos.append((each[0],each[2],each[1]))


            self.corners = [0, 2, 6, 8]

            self.rest = [1, 3, 5, 7]

            self.flag = " "

            self.opp_flag = " "

            self.local_score = {
                    "winpos" : 1,
                    "two" : 0.025,
                    "center" : 0.020,
                    "corner" : 0.007,
                    "rest" : 0.002,
                    "blockedtwo":0.010,
                    "blockpos":0.040,
                    }
            
            self.global_score = {
                    "winpos" : 100,
                    "two" : 95,
                    "center" : 90,
                    "corner" : 30,
                    "rest" : 5,
                    "blockedtwo":25,
                    "blockpos":60,
                    }
            
            self.llookup = {
                    'x' : {},
                    'o' : {}
                    }
            
            self.glookup = {
                    'x' : {},
                    'o' : {}
                    }

            self.memoization()

        def hsh(self, temp_node):
            return tuple(temp_node)

        def memoization(self):
            
            symbol = ['x', 'o', '-']
            
            for enum in xrange(0, 3**9):
                temp = enum
                node = []

                for i in xrange(0, 9):
                    node.append(symbol[temp % 3])
                    temp /= 3

                hshed = self.hsh(node)

                self.llookup['x'][hshed] = self.heuristic_local(node, 'x')
                self.llookup['o'][hshed] = -self.llookup['x'][hshed]
                self.glookup['x'][hshed] = self.heuristic_global(node, 'x')
                self.glookup['o'][hshed] = -self.glookup['x'][hshed]

        def blocks_allowed(self, old_move, block_stat):
            
            blocks = []
            
            if old_move[0]%3 == 0:
                if old_move[1]%3 == 0:
                    blocks = [1,3]
                if old_move[1]%3 == 1:
                    blocks = [0,2]
                if old_move[1]%3 == 2:
                    blocks = [1,5]

            if old_move[0]%3 == 1:
                if old_move[1]%3 == 0:
                    blocks = [0,6]
                if old_move[1]%3 == 1:
                    blocks = [4]
                if old_move[1]%3 == 2:
                    blocks = [2,8]

            if old_move[0]%3 == 2:
                if old_move[1]%3 == 0:
                    blocks = [3,7]
                if old_move[1]%3 == 1:
                    blocks = [6,8]
                if old_move[1]%3 == 2:
                    blocks = [5,7]

            final_blocks_allowed = []

            for block in blocks:
                if block_stat[block] == '-':
                    final_blocks_allowed.append(block)

            if old_move == (-1, -1):
                final_blocks_allowed = [4]
                
            return final_blocks_allowed

        def cells_allowed(self, temp_board, blocks_allowed, block_stat):

            cells = []

            for block in blocks_allowed:

                start_row = (block / 3) * 3
                start_col = ((block) % 3) * 3

                for i in xrange(start_row, start_row + 3):
                    for j in xrange(start_col, start_col + 3):
                        if temp_board[i][j] == '-':
                            cells.append((i,j))

            if not cells:
                for i in xrange(9):
                    if block_stat[i] != '-':
                        continue                    
                    start_row = (i / 3) * 3
                    start_col = ((i) % 3) * 3
                    for j in xrange(start_row, start_row + 3):
                        for k in xrange(start_col, start_col + 3):
                            if temp_board[j][k] == '-':
                                cells.append((j,k))

            return cells

        def heuristic(self, node, temp_block):

            utility = 0

            for i in xrange(9):
                start_row = (i / 3) * 3
                start_col = ((i) % 3) * 3
                i_stat = []

                for j in xrange(start_row, start_row + 3):
                    for k in xrange(start_col, start_col + 3):
                        i_stat.append(node[j][k])
                utility += self.llookup[self.flag][self.hsh(i_stat)]
            
            bl_stat = copy.deepcopy(temp_block)

            for i in xrange(9):
                if bl_stat[i] == 'D':
                    bl_stat[i] = '-'

            utility += self.glookup[self.flag][self.hsh(bl_stat)]
            
            return utility

	def heuristic_local(self, node, curr_flag):

                curr_opp_flag = " "
                if curr_flag == 'x':
                    curr_opp_flag = 'o'
                else:
                    curr_opp_flag = 'x'

            	utility = 0
                
                i_stat = node

                #Local win
                for each in self.win_pos:
                    if i_stat[each[0]] == curr_flag and i_stat[each[1]] == curr_flag and i_stat[each[2]] == curr_flag:
                        utility += self.local_score["winpos"]
                        break
                    if i_stat[each[0]] == curr_opp_flag and i_stat[each[1]] == curr_opp_flag and i_stat[each[2]] == curr_opp_flag:
                        utility -= self.local_score["winpos"]
                        break

                #Local twos
                for each in self.twos:
                    if i_stat[each[0]] == curr_flag and i_stat[each[1]] == curr_flag and i_stat[each[2]]=='-':
                        utility +=  self.local_score["two"]

                    if i_stat[each[0]] == curr_flag and i_stat[each[1]] == curr_flag and i_stat[each[2]]==curr_opp_flag:
                        utility +=  self.local_score["blockedtwo"]
                        utility -=  self.local_score["blockpos"]#opponent in blocking position,dec utility

                    if i_stat[each[0]] == curr_opp_flag and i_stat[each[1]] == curr_opp_flag and i_stat[each[2]]=='-':
                        utility -= self.local_score["two"]

                    if i_stat[each[0]] == curr_opp_flag and i_stat[each[1]] == curr_opp_flag and i_stat[each[2]]==curr_flag:
                        utility -= self.local_score["blockedtwo"]
                        utility += self.local_score["blockpos"]#self in blocking position,inc utility

                #Local corner
                for each in self.corners:
                    if i_stat[each] == curr_flag:
                        utility += self.local_score["corner"]
                    if i_stat[each] == curr_opp_flag:
                        utility -= self.local_score["corner"]

                #Local rest
                for each in self.rest:
                    if i_stat[each] == curr_flag:
                        utility += self.local_score["rest"]
                    if i_stat[each] == curr_opp_flag:
                        utility -= self.local_score["rest"]

                #Local center
                    if i_stat[4] == curr_flag:
                        utility += self.local_score["center"]
                    if i_stat[4] == curr_opp_flag:
                        utility -= self.local_score["center"]

		return utility

	def heuristic_global(self, node, curr_flag):

                curr_opp_flag = " "
                if curr_flag == 'x':
                    curr_opp_flag = 'o'
                else:
                    curr_opp_flag = 'x'

            	utility = 0
                
                i_stat = node

                #Global win
                for each in self.win_pos:
                    if i_stat[each[0]] == curr_flag and i_stat[each[1]] == curr_flag and i_stat[each[2]] == curr_flag:
                        utility += self.global_score["winpos"]
                        break
                    if i_stat[each[0]] == curr_opp_flag and i_stat[each[1]] == curr_opp_flag and i_stat[each[2]] == curr_opp_flag:
                        utility -= self.global_score["winpos"]
                        break

                #Global twos
                for each in self.twos:
                    if i_stat[each[0]] == curr_flag and i_stat[each[1]] == curr_flag and i_stat[each[2]]=='-':
                        utility +=  self.global_score["two"]

                    if i_stat[each[0]] == curr_flag and i_stat[each[1]] == curr_flag and i_stat[each[2]]==curr_opp_flag:
                        utility +=  self.global_score["blockedtwo"]
                        utility -=  self.global_score["blockpos"]#opponent in blocking position,dec utility

                    if i_stat[each[0]] == curr_opp_flag and i_stat[each[1]] == curr_opp_flag and i_stat[each[2]]=='-':
                        utility -= self.global_score["two"]

                    if i_stat[each[0]] == curr_opp_flag and i_stat[each[1]] == curr_opp_flag and i_stat[each[2]]==curr_flag:
                        utility -= self.global_score["blockedtwo"]
                        utility += self.global_score["blockpos"]#self in blocking position,inc utility


                #Global corner
                for each in self.corners:
                    if i_stat[each] == curr_flag:
                        utility += self.global_score["corner"]
                    if i_stat[each] == curr_opp_flag:
                        utility -= self.global_score["corner"]

                #Global rest
                for each in self.rest:
                    if i_stat[each] == curr_flag:
                        utility += self.global_score["rest"]
                    if i_stat[each] == curr_opp_flag:
                        utility -= self.global_score["rest"]

                #Global center
                    if i_stat[4] == curr_flag:
                        utility += self.global_score["center"]
                    if i_stat[4] == curr_opp_flag:
                        utility -= self.global_score["center"]

		return utility

        def genChild(self, node, temp_block, mov, current_flag):

            temp_node = copy.deepcopy(node)
            temp_node[mov[0]][mov[1]] = current_flag
            current_temp_block = copy.deepcopy(temp_block)

            block_num = (mov[0] / 3) * 3 + (mov[1] / 3)
            
            temp_stat = []
            start_row = (block_num / 3) * 3
            start_col = ((block_num) % 3) * 3
            for j in xrange(start_row, start_row + 3):
                for k in xrange(start_col, start_col + 3):
                    temp_stat.append(temp_node[j][k])

            for each in self.win_pos:
                if temp_stat[each[0]] == self.flag and temp_stat[each[1]] == self.flag and temp_stat[each[2]] == self.flag:
                    current_temp_block[block_num] = self.flag
                    break
                if temp_stat[each[0]] == self.opp_flag and temp_stat[each[1]] == self.opp_flag and temp_stat[each[2]] == self.opp_flag:
                    current_temp_block[block_num] = self.opp_flag
                    break

            return (temp_node, current_temp_block)


        def alphabeta(self, node, depth, alpha, beta, maximizingPlayer, old_move, temp_block):            

            if (depth == 0 and depth != self.maxdepth) or self.timed_out == True:
                    return self.heuristic(copy.deepcopy(node), copy.deepcopy(temp_block))
            
            if time.time() - self.came >= self.threshold[self.maxdepth-4]:
                self.timed_out = True
                return self.heuristic(copy.deepcopy(node), copy.deepcopy(temp_block))

            blocks = self.blocks_allowed(old_move, temp_block)
            
            cells_allowed = self.cells_allowed(node, blocks, temp_block)

            if not cells_allowed:
                return self.heuristic(copy.deepcopy(node), copy.deepcopy(temp_block))

            ret_mov = " "

            if maximizingPlayer:
                v = -self.inf
                
                for mov in cells_allowed:
                    tmp = self.genChild(node, temp_block, mov, self.flag)
                    child = tmp[0]
                    current_temp_block = tmp[1]

                    temp = self.alphabeta(copy.deepcopy(child), depth - 1, copy.deepcopy(alpha), copy.deepcopy(beta), False, copy.deepcopy(mov), copy.deepcopy(current_temp_block))

                    if v < temp:
                        v = temp
                        ret_mov = mov
                    alpha = max(alpha, v)
                    
                    if beta <= alpha:
                        break

                if depth == self.maxdepth:
                    return ret_mov
                else:
                    return v

            else:
                v = self.inf

                for mov in cells_allowed:
                    tmp = self.genChild(node, temp_block, mov, self.opp_flag)
                    child = tmp[0]
                    current_temp_block = tmp[1]

                    temp = self.alphabeta(copy.deepcopy(child), depth - 1, copy.deepcopy(alpha), copy.deepcopy(beta), True, copy.deepcopy(mov), copy.deepcopy(current_temp_block))
                    
                    if v > temp:
                        v = temp
                        ret_mov = mov
                    beta = min(beta, v)
                    
                    if beta <= alpha:
                        break
                
                if depth == self.maxdepth:
                    return ret_mov
                else:
                    return v

	def move(self, temp_board, temp_block, old_move, flag):
                if old_move == (-1, -1):
                    return (3, 3)
                ret2 = " "
                ret3 = " "
                ret4 = " "
                self.timed_out = False
                self.flag = flag
                if self.opp_flag == " ":
                    if self.flag == 'x':
                        self.opp_flag = 'o'
                    else:
                        self.opp_flag = 'x'
                self.maxdepth = 7
                self.came = time.time()
                ret = self.alphabeta(copy.deepcopy(temp_board), self.maxdepth,  -self.inf, self.inf, True, copy.deepcopy(old_move), copy.deepcopy(temp_block))
                if self.timed_out == True:
                    self.timed_out = False
                    self.maxdepth = 6
                    self.came = time.time()
                    ret2 = self.alphabeta(copy.deepcopy(temp_board), self.maxdepth, -self.inf, self.inf, True, copy.deepcopy(old_move), copy.deepcopy(temp_block))
                    if self.timed_out == True:
                        self.timed_out = False
                        self.maxdepth = 5
                        self.came = time.time()
                        ret3 = self.alphabeta(copy.deepcopy(temp_board), self.maxdepth, -self.inf, self.inf, True, copy.deepcopy(old_move), copy.deepcopy(temp_block))
                        if self.timed_out == True:
                            self.timed_out = False
                            self.maxdepth = 4
                            self.came = time.time()
                            ret4 = self.alphabeta(copy.deepcopy(temp_board), self.maxdepth, -self.inf, self.inf, True, copy.deepcopy(old_move), copy.deepcopy(temp_block))
                            return ret4                            
                        else:
                            return ret3
                    else:
                        return ret2
                else:
                    return ret

"""
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (3, 3) with x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  x - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (4, 0) with o
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  x - -  - - -
o - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (0, 2) with x
=========== Game Board ===========
- - x  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  x - -  - - -
o - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (2, 5) with o
=========== Game Board ===========
- - x  - - -  - - -
- - -  - - -  - - -
- - -  - - o  - - -

- - -  x - -  - - -
o - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (5, 8) with x
=========== Game Board ===========
- - x  - - -  - - -
- - -  - - -  - - -
- - -  - - o  - - -

- - -  x - -  - - -
o - -  - - -  - - -
- - -  - - -  - - x

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (7, 5) with o
=========== Game Board ===========
- - x  - - -  - - -
- - -  - - -  - - -
- - -  - - o  - - -

- - -  x - -  - - -
o - -  - - -  - - -
- - -  - - -  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (1, 7) with x
=========== Game Board ===========
- - x  - - -  - - -
- - -  - - -  - x -
- - -  - - o  - - -

- - -  x - -  - - -
o - -  - - -  - - -
- - -  - - -  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (3, 4) with o
=========== Game Board ===========
- - x  - - -  - - -
- - -  - - -  - x -
- - -  - - o  - - -

- - -  x o -  - - -
o - -  - - -  - - -
- - -  - - -  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (1, 1) with x
=========== Game Board ===========
- - x  - - -  - - -
- x -  - - -  - x -
- - -  - - o  - - -

- - -  x o -  - - -
o - -  - - -  - - -
- - -  - - -  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (4, 3) with o
=========== Game Board ===========
- - x  - - -  - - -
- x -  - - -  - x -
- - -  - - o  - - -

- - -  x o -  - - -
o - -  o - -  - - -
- - -  - - -  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (2, 0) with x
=========== Game Board ===========
- - x  - - -  - - -
- x -  - - -  - x -
x - -  - - o  - - -

- - -  x o -  - - -
o - -  o - -  - - -
- - -  - - -  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 2 made the move: (4, 1) with o
=========== Game Board ===========
- - x  - - -  - - -
- x -  - - -  - x -
x - -  - - o  - - -

- - -  x o -  - - -
o o -  o - -  - - -
- - -  - - -  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 1 made the move: (4, 4) with x
=========== Game Board ===========
- - x  - - -  - - -
- x -  - - -  - x -
x - -  - - o  - - -

- - -  x o -  - - -
o o -  o x -  - - -
- - -  - - -  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 2 made the move: (3, 5) with o
=========== Game Board ===========
- - x  - - -  - - -
- x -  - - -  - x -
x - -  - - o  - - -

- - -  x o o  - - -
o o -  o x -  - - -
- - -  - - -  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 1 made the move: (4, 7) with x
=========== Game Board ===========
- - x  - - -  - - -
- x -  - - -  - x -
x - -  - - o  - - -

- - -  x o o  - - -
o o -  o x -  - x -
- - -  - - -  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 2 made the move: (5, 5) with o
=========== Game Board ===========
- - x  - - -  - - -
- x -  - - -  - x -
x - -  - - o  - - -

- - -  x o o  - - -
o o -  o x -  - x -
- - -  - - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 1 made the move: (3, 6) with x
=========== Game Board ===========
- - x  - - -  - - -
- x -  - - -  - x -
x - -  - - o  - - -

- - -  x o o  x - -
o o -  o x -  - x -
- - -  - - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 2 made the move: (2, 3) with o
=========== Game Board ===========
- - x  - - -  - - -
- x -  - - -  - x -
x - -  o - o  - - -

- - -  x o o  x - -
o o -  o x -  - x -
- - -  - - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 1 made the move: (3, 1) with x
=========== Game Board ===========
- - x  - - -  - - -
- x -  - - -  - x -
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x -  - x -
- - -  - - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 2 made the move: (1, 8) with o
=========== Game Board ===========
- - x  - - -  - - -
- x -  - - -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x -  - x -
- - -  - - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 1 made the move: (0, 7) with x
=========== Game Board ===========
- - x  - - -  - x -
- x -  - - -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x -  - x -
- - -  - - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 2 made the move: (0, 8) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - - -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x -  - x -
- - -  - - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 1 made the move: (1, 4) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x -  - x -
- - -  - - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 2 made the move: (5, 3) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x -  - x -
- - -  o - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 1 made the move: (5, 1) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x -  - x -
- x -  o - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 2 made the move: (8, 0) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x -  - x -
- x -  o - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
o - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 1 made the move: (5, 0) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x -  - x -
x x -  o - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
o - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 2 made the move: (8, 4) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x -  - x -
x x -  o - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
o - -  - o -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 1 made the move: (8, 2) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x -  - x -
x x -  o - o  - - x

- - -  - - -  - - -
- - -  - - o  - - -
o - x  - o -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 2 made the move: (7, 4) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x -  - x -
x x -  o - o  - - x

- - -  - - -  - - -
- - -  - o o  - - -
o - x  - o -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 1 made the move: (4, 5) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x x  - x -
x x -  o - o  - - x

- - -  - - -  - - -
- - -  - o o  - - -
o - x  - o -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 2 made the move: (7, 6) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x x  - x -
x x -  o - o  - - x

- - -  - - -  - - -
- - -  - o o  o - -
o - x  - o -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 1 made the move: (8, 1) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x x  - x -
x x -  o - o  - - x

- - -  - - -  - - -
- - -  - o o  o - -
o x x  - o -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 2 made the move: (6, 1) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - - -

- x -  x o o  x - -
o o -  o x x  - x -
x x -  o - o  - - x

- o -  - - -  - - -
- - -  - o o  o - -
o x x  - o -  - - -
==================================
=========== Block Status =========
x - -
- - x
- - -
==================================

Player 1 made the move: (2, 7) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x -  o - o  - - x

- o -  - - -  - - -
- - -  - o o  o - -
o x x  - o -  - - -
==================================
=========== Block Status =========
x - x
- - x
- - -
==================================

Player 2 made the move: (8, 8) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x -  o - o  - - x

- o -  - - -  - - -
- - -  - o o  o - -
o x x  - o -  - - o
==================================
=========== Block Status =========
x - x
- - x
- - -
==================================

Player 1 made the move: (8, 5) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x -  o - o  - - x

- o -  - - -  - - -
- - -  - o o  o - -
o x x  - o x  - - o
==================================
=========== Block Status =========
x - x
- - x
- - -
==================================

Player 2 made the move: (8, 3) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x -  o - o  - - x

- o -  - - -  - - -
- - -  - o o  o - -
o x x  o o x  - - o
==================================
=========== Block Status =========
x - x
- - x
- - -
==================================

Player 1 made the move: (5, 2) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o - o  - - x

- o -  - - -  - - -
- - -  - o o  o - -
o x x  o o x  - - o
==================================
=========== Block Status =========
x - x
x - x
- - -
==================================

Player 2 made the move: (6, 3) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o - o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o - o  - - x

- o -  o - -  - - -
- - -  - o o  o - -
o x x  o o x  - - o
==================================
=========== Block Status =========
x - x
x - x
- - -
==================================

Player 1 made the move: (2, 4) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o x o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o - o  - - x

- o -  o - -  - - -
- - -  - o o  o - -
o x x  o o x  - - o
==================================
=========== Block Status =========
x - x
x - x
- - -
==================================

Player 2 made the move: (7, 1) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o x o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o - o  - - x

- o -  o - -  - - -
- o -  - o o  o - -
o x x  o o x  - - o
==================================
=========== Block Status =========
x - x
x - x
- - -
==================================

Player 1 made the move: (5, 4) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o x o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o x o  - - x

- o -  o - -  - - -
- o -  - o o  o - -
o x x  o o x  - - o
==================================
=========== Block Status =========
x - x
x D x
- - -
==================================

Player 2 made the move: (7, 8) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o x o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o x o  - - x

- o -  o - -  - - -
- o -  - o o  o - o
o x x  o o x  - - o
==================================
=========== Block Status =========
x - x
x D x
- - -
==================================

Player 1 made the move: (8, 6) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o x o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o x o  - - x

- o -  o - -  - - -
- o -  - o o  o - o
o x x  o o x  x - o
==================================
=========== Block Status =========
x - x
x D x
- - -
==================================

Player 2 made the move: (6, 4) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o x o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o x o  - - x

- o -  o o -  - - -
- o -  - o o  o - o
o x x  o o x  x - o
==================================
=========== Block Status =========
x - x
x D x
- o -
==================================

Player 1 made the move: (6, 2) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x -  - x o
x - -  o x o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o x o  - - x

- o x  o o -  - - -
- o -  - o o  o - o
o x x  o o x  x - o
==================================
=========== Block Status =========
x - x
x D x
- o -
==================================

Player 2 made the move: (1, 5) with o
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x o  - x o
x - -  o x o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o x o  - - x

- o x  o o -  - - -
- o -  - o o  o - o
o x x  o o x  x - o
==================================
=========== Block Status =========
x - x
x D x
- o -
==================================

Player 1 made the move: (6, 8) with x
=========== Game Board ===========
- - x  - - -  - x o
- x -  - x o  - x o
x - -  o x o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o x o  - - x

- o x  o o -  - - x
- o -  - o o  o - o
o x x  o o x  x - o
==================================
=========== Block Status =========
x - x
x D x
- o -
==================================

Player 2 made the move: (0, 3) with o
=========== Game Board ===========
- - x  o - -  - x o
- x -  - x o  - x o
x - -  o x o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o x o  - - x

- o x  o o -  - - x
- o -  - o o  o - o
o x x  o o x  x - o
==================================
=========== Block Status =========
x - x
x D x
- o -
==================================

Player 1 made the move: (0, 4) with x
=========== Game Board ===========
- - x  o x -  - x o
- x -  - x o  - x o
x - -  o x o  - x -

- x -  x o o  x - -
o o -  o x x  - x -
x x x  o x o  - - x

- o x  o o -  - - x
- o -  - o o  o - o
o x x  o o x  x - o
==================================
=========== Block Status =========
x x x
x D x
- o -
==================================

P1
COMPLETE
"""
