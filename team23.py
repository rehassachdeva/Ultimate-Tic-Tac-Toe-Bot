import sys
import random
import signal

class Player23:

	def __init__(self):
		pass

	def move(self,temp_board,temp_block,old_move,flag):
		blocks_allowed  = blocks_allowed(old_move, temp_block)
		cells = cells_allowed(temp_board, blocks_allowed)
		return cells[random.randrange(len(cells))]

        def blocks_allowed(old_move, block_stat):
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

            return final_blocks_allowed

        def cells_allowed(temp_board, blocks_allowed):

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

                    start_row = (i / 3) * 3
                    start_col = ((i) % 3) * 3

                    for j in xrange(start_row, start_row + 3):
                        for k in xrange(start_col, start_col + 3):
                            if temp_board[j][k] == '-':
                                cells.append((j,k))

            return cells




