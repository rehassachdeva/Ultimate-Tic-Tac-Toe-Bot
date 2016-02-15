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
            pass



