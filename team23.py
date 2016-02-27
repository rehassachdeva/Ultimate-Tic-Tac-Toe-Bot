import sys
import random
import signal
import copy

class Player23:

	def __init__(self):
	    	self.win_pos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
            	self.twos = []
		self.corners = [0, 2, 6, 8]
		self.rest = [1, 3, 5, 7]
		self.moves = " "
		self.flag = " "
		self.block_stat = " "
		self.opp_flag = " "
		self.gctr = 0

		for each in self.win_pos:
		        self.twos.append((each[0],each[1]))
		        self.twos.append((each[1],each[2]))
		        self.twos.append((each[0],each[1]))

	def move(self,board,block,move,flag):
                temp_board=copy.deepcopy(board)
                temp_block=copy.deepcopy(block)
                old_move=copy.deepcopy(move)

		blocks = self.blocks_allowed(old_move, temp_block)
                print "team23 blocks",blocks
		cells = self.cells_allowed(temp_board, blocks)
                print "cells",cells
		#return cells[random.randrange(len(cells))]
		best_move=self.pick(temp_board,temp_block,cells,flag)
		if best_move in cells:
		        print "my move", best_move
			return best_move
		else:
			print "illegal",best_move

	def pick(self,node,block_stat,movs,current_flag):
		best_score=-100000000000000000
		best_move=0
		for mov in movs:
			temp_node = copy.deepcopy(node)

			temp_node[mov[0]][mov[1]] = current_flag

			block_stat_temp = copy.deepcopy(block_stat)
			temp_score=self.heuristic(temp_node, block_stat_temp)
			if(temp_score>best_score):
				best_score=temp_score
				best_move=mov


		return best_move

        def blocks_allowed(self,old_move,block_stat):
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

            if not final_blocks_allowed:
                blocks = [x for x in range(9)]
                for block in blocks:
                    if block_stat[block] == '-':
                        final_blocks_allowed.append(block)

            return final_blocks_allowed

        def cells_allowed(self,temp_board, blocks_allowed):
            cells = []

            for block in blocks_allowed:

                start_row = (block / 3) * 3
                start_col = ((block) % 3) * 3

                for i in xrange(start_row, start_row + 3):
                    for j in xrange(start_col, start_col + 3):
                        if temp_board[i][j] == '-':
                            cells.append((i,j))

            return cells

	def heuristic(self, node, temp_block):

            utility = 0

            #=========================Local======================
            for i in xrange(9):

                start_row = (i / 3) * 3
                start_col = ((i) % 3) * 3

                i_stat = []

                for j in xrange(start_row, start_row + 3):
                    for k in xrange(start_col, start_col + 3):
                        i_stat.append(node[j][k])

                #Local win
                for each in self.win_pos:

                    if i_stat[each[0]] == self.flag and i_stat[each[1]] == self.flag and i_stat[each[2]] == self.flag:
                        temp_block_stat[i] = self.flag
                        utility += 5
                        break

                    if i_stat[each[0]] == self.opp_flag and i_stat[each[1]] == self.opp_flag and i_stat[each[2]] == self.opp_flag:
                        temp_block_stat[i] = self.opp_flag
                        utility -= 5
                        break
                #Local twos
                for each in self.twos:

                    if i_stat[each[0]] == self.flag and i_stat[each[1]] == self.flag:
                        utility += 4

                    if i_stat[each[0]] == self.opp_flag and i_stat[each[1]] == self.opp_flag:
                        utility -= 4

                #Local corner
                for each in self.corners:
                    if i_stat[each] == self.flag:
                        utility +=2
                    if i_stat[each] == self.opp_flag:
                        utility -=2

                #Local rest
                for each in self.rest:
                    if i_stat[each] == self.flag:
                        utility +=1
                    if i_stat[each] == self.opp_flag:
                        utility -=1

                #Local center
                    if i_stat[4] == self.flag:
                        utility +=3
                    if i_stat[4] == self.opp_flag:
                        utility -=3



            #================Global===============

            #Global win
            for each in self.win_pos:
            	if temp_block[each[0]] == self.flag and temp_block[each[1]] == self.flag and temp_block[each[2]] == self.flag:
                    utility += 10000
                    break

                if temp_block[each[0]] == self.opp_flag and temp_block[each[1]] == self.opp_flag and temp_block[each[2]] == self.opp_flag:
                    utility -= 10000
                    break

            #Global twos
            for each in self.twos:

                    if temp_block[each[0]] == self.flag and temp_block[each[1]] == self.flag:
                        utility += 5

                    if temp_block[each[0]] == self.opp_flag and temp_block[each[1]] == self.opp_flag:
                        utility -= 5

            #Global corner
            for each in self.corners:
                    if temp_block[each] == self.flag:
                        utility +=3
                    if temp_block[each] == self.opp_flag:
                        utility -=3

            #Global rest
            for each in self.rest:
                    if temp_block[each] == self.flag:
                        utility +=2
                    if temp_block[each] == self.opp_flag:
                        utility -=2

            #Global center
                    if temp_block[4] == self.flag:
                        utility +=10
                    if temp_block[4] == self.opp_flag:
                        utility -=10



            return utility




