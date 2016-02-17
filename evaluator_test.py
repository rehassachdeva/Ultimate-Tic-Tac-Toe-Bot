''' 

This is the engine for the Ultimate TicTacToe Tournament. The code in this file is not for reproduction.
@author: Devansh Shah

The structure of the code is as below:
1. Header Files
2. Sample implementations of your class (Player and ManualPlayer)
3. Game Logic
4. Game simulator

In case of any queries, please post on moodle.iiit.ac.in

'''

import sys
import random
import signal
import copy

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()


class ManualPlayer:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))
		
class Player1:
	
	def __init__(self):
            # You may initialize your object here and use any variables for storing throughout the game
            self.win_pos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
            self.moves = " "
            self.flag = " "
            self.block_stat = " "
            self.opp_flag = " "
            
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
                    
            return final_blocks_allowed

        def cells_allowed(self, temp_board, blocks_allowed):

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

        def heuristic(self, node, temp_block):

            utility = 0

            for i in xrange(9):

                start_row = (i / 3) * 3
                start_col = ((i) % 3) * 3

                i_stat = []

                for j in xrange(start_row, start_row + 3):
                    for k in xrange(start_col, start_col + 3):
                        i_stat.append(node[j][k])

                for each in self.win_pos:
                    
                    if i_stat[each[0]] == self.flag and i_stat[each[1]] == self.flag and i_stat[each[2]] == self.flag:
                        temp_block_stat[i] = self.flag
                        utility += 5
                        break

                    if i_stat[each[0]] == self.opp_flag and i_stat[each[1]] == self.opp_flag and i_stat[each[2]] == self.opp_flag:
                        temp_block_stat[i] = self.opp_flag
                        utility -= 5
                        break

            for each in self.win_pos:
            	if temp_block[each[0]] == self.flag and temp_block[each[1]] == self.flag and temp_block[each[2]] == self.flag:
                    utility += 10000
                    break
                
                if temp_block[each[0]] == self.opp_flag and temp_block[each[1]] == self.opp_flag and temp_block[each[2]] == self.opp_flag:
                    utility -= 10000
                    break   
            
            return utility      

        def genChild(self, node, temp_block, mov):
            
            temp_node = copy.copy(node)
            
            temp_node[mov[0]][mov[1]] = self.flag
            
            current_temp_block = copy.copy(temp_block)
            
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

            blocks_allowed = self.blocks_allowed(self, node, temp_block)
            
            cells_allowed = self.cells_allowed(self, node, blocks_allowed)

            ret_mov = " "
            
            if depth == 0: 
                return self.heuristic(node, temp_block)

            if maximizingPlayer:
                v = -sys.maxsize - 1
                for mov in cells_allowed:
                    tmp = self.genChild(node, temp_block, mov)
                    child = tmp[0]
                    current_temp_block = tmp[1]                  
                    
                    temp = self.alphabeta(child, depth - 1, alpha, beta, False, mov, current_temp_block)
                    if v < temp:
                        v = temp
                        ret_mov = mov
                    alpha = max(alpha, v)
                    if beta <= alpha:
                        break
                
                if depth == 2:
                    return ret_mov
                else:
                    return v

            else:
                v = sys.maxsize
                for mov in cells_allowed:
                    tmp = self.genChild(node, temp_block, mov)
                    child = tmp[0]
                    current_temp_block = tmp[1]                  
                    
                    temp = self.alphabeta(child, depth - 1, alpha, beta, True, mov, current_temp_block)
                    if v > temp:
                        v = temp
                        ret_mov = mov
                    beta = min(beta, v)
                    if beta <= alpha:
                        break
                if depth == 2:
                    return ret_mov
                else:
                    return v

	def move(self, temp_board, temp_block, old_move, flag):
                self.flag = flag
                if self.opp_flag == " ":
                    if self.flag == 'x':
                        self.opp_flag = 'o'
                    else:
                        self.opp_flag = 'x'
		
                #Choose a move based on some algorithm, here it is a random move.
		#return cells[random.randrange(len(cells))]
                ret =  self.alphabeta(temp_board, 2,  -sys.maxsize - 1, sys.maxsize, True, old_move, temp_block)
                return ret

class Player2:
	
	def __init__(self):
		# You may initialize your object here and use any variables for storing throughout the game
		pass

	def move(self,temp_board,temp_block,old_move,flag):
		#List of permitted blocks, based on old move.
		blocks_allowed  = determine_blocks_allowed(old_move, temp_block)
		#Get list of empty valid cells
		cells = get_empty_out_of(temp_board, blocks_allowed)
		#Choose a move based on some algorithm, here it is a random move.
		return cells[random.randrange(len(cells))]

def determine_blocks_allowed(old_move, block_stat):
	blocks_allowed = []
	if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
		blocks_allowed = [1,3]
	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
		blocks_allowed = [1,5]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
		blocks_allowed = [3,7]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
		blocks_allowed = [5,7]
	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
		blocks_allowed = [0,2]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
		blocks_allowed = [0,6]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
		blocks_allowed = [6,8]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
		blocks_allowed = [2,8]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
		blocks_allowed = [4]
	else:
		sys.exit(1)
	final_blocks_allowed = []
	for i in blocks_allowed:
		if block_stat[i] == '-':
			final_blocks_allowed.append(i)
	return final_blocks_allowed

#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
def get_empty_out_of(gameb, blal):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		new_blal = [0,1,2,3,4,5,6,7,8]
		for idb in new_blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))
	return cells
		
# Returns True if move is valid
def check_valid_move(game_board, block_stat, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True

	#List of permitted blocks, based on old move.
        blocks_allowed  = determine_blocks_allowed(old_move, block_stat)
	print blocks_allowed
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
	cells = get_empty_out_of(game_board, blocks_allowed)
	print cells
	#Checks if you made a valid move. 
	if current_move in cells:
		return True
	else:
		return False

def update_lists(game_board, block_stat, move_ret, fl):

	game_board[move_ret[0]][move_ret[1]] = fl

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3	
	id1 = block_no/3
	id2 = block_no%3
	mflg = 0
	if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                                mflg = 1
                                break
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                                mflg = 1
                                break
	if mflg == 1:
		block_stat[block_no] = fl
	
	return mflg

#Check win
def terminal_state_reached(game_board, block_stat,point1,point2):
	### we are now concerned only with block_stat
	bs = block_stat
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-') or (bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		return True, 'W'
	## Col win
	elif (bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[7] and bs[0]!='-') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-'):
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			for j in range(9):
				if game_board[i][j] == '-':
					smfl = 1
					break
		if smfl == 1:
			return False, 'Continue'
		
		else:
			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
				return True, 'D'	


def decide_winner_and_get_message(player,status, message):
	if status == 'P1':
		return ('P1', 'MORE BLOCKS')
	elif status == 'P2':
		return ('P2', 'MORE BLOCKS')
	elif player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NONE','DRAW')
	return


def print_lists(gb, bs):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print
	

def simulate(obj1,obj2):
	
	# Game board is a 9x9 list of lists & block_stat is a list of 9 elements indicating if a block has been won.
	game_board, block_stat = get_init_board_and_blockstatus()

	pl1 = obj1 
	pl2 = obj2

	# Player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1) # For the first move

	WINNER = ''
	MESSAGE = ''
	TIMEALLOWED = 12
	p1_pts=0
	p2_pts=0

	print_lists(game_board, block_stat)

	while(1): # Main game loop
		
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)

		try:
			ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
		except:
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
			print MESSAGE
			break
		signal.alarm(0)
	
		# Check if list is tampered.
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		# Check if the returned move is valid
		if not check_valid_move(game_board, block_stat, ret_move_pl1, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break
			

		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl
		# Update the 'game_board' and 'block_stat' move
		p1_pts += update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)

		gamestatus, mesg =  terminal_state_reached(game_board, block_stat,p1_pts,p2_pts)
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')	
			break

		
		old_move = ret_move_pl1
		print_lists(game_board, block_stat)

        	temp_board_state = game_board[:]
        	temp_block_stat = block_stat[:]

        	signal.signal(signal.SIGALRM, handler)
        	signal.alarm(TIMEALLOWED)
        	try:
           		ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
        	except:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
        	signal.alarm(0)

        	if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
			
        	if not check_valid_move(game_board, block_stat, ret_move_pl2, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break

        	print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
        
        	p2_pts += update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)

        	# Now check if the last move resulted in a terminal state
        	gamestatus, mesg =  terminal_state_reached(game_board, block_stat,p1_pts,p2_pts)
        	if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
			break
        	else:
			old_move = ret_move_pl2
			print_lists(game_board, block_stat)
	
	print WINNER
	print MESSAGE

if __name__ == '__main__':
	## get game playing objects

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Player1()
		obj2 = Player2()

	elif option == '2':
		obj1 = Player1()
		obj2 = ManualPlayer()
	elif option == '3':
		obj1 = ManualPlayer()
		obj2 = ManualPlayer()
	else:
		print 'Invalid option'
		sys.exit(1)

	num = random.uniform(0,1)
	if num > 0.5:
		simulate(obj2, obj1)
	else:
		simulate(obj1, obj2)
		
	
