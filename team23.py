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

        def blocks_allowed(old_move, temp_block):
            pass
        
        def cells_allowed(temp_board, blocks_allowed):
            
            cells = []

            for block in blocks_allowed:
                
                start_row = (block / 3) * 3
                start_col = ((block) % 3) * 3

                for i in range(start_row, start_row + 3):
                    for j in range(start_col, start_col + 3):
                        if temp_board[i][j] == '-':
                            cells.append((i,j))

            if not cells:

                for i in range(9):

                    start_row = (i / 3) * 3
                    start_col = ((i) % 3) * 3
                    
                    for j in range(start_row, start_row + 3):
                        for k in range(start_col, start_col + 3):
                            if temp_board[j][k] == '-':
                                cells.append((j,k))

            return cells




