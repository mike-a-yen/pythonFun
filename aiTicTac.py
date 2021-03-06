import numpy as np
# ai will always be player 2
class ai(object):
    def __init__(self,difficulty,board):
        self.player = 2
        self.difficulty = difficulty
        self.board = board
        self.rows = len(self.board[0,:])
        self.cols = len(self.board[:,0])
    
    def UpdateBoard(self, board):
        self.board = board

    def Move(self, board):
        self.UpdateBoard(board)
        # make a board to rank moves higher score
        # higher priority
        scoreBoard = np.zeros([self.rows,self.cols], dtype=np.int)

        emptySpaces = np.vstack(np.where(board==0)).T
        for space in emptySpaces:
            scoreBoard[space[0],space[1]] += 1

        attackList = self.Attack()
        for space in attackList:
            scoreBoard[space[0],space[1]] += 1

        # must move into block space
        blockList = self.Block()
        for space in blockList:
            scoreBoard[space[0],space[1]] += 999
            
        move = self.FindMaximum(scoreBoard)
        print move
        return move
        
    def Block(self):
        # check if there are two 1's in each row/col/diag
        # if so add the empty space to the block list
        blockList = []
        for row in xrange(self.rows):
            if 2 in self.board[row]: continue
            if 0 not in self.board[row]:continue
            if len(self.board[row][self.board[row,:]==1]) == 2:
                space = np.argwhere(self.board[row] == 0)[0][0]
                blockList.append([row,space])

        for col in xrange(self.cols):
            if 2 in self.board[:,col]: continue
            if 0 not in self.board[col]:continue
            if len(self.board[:,col][self.board[:,col]==1]) == 2:
                space = np.argwhere(self.board[:,col]==0)[0][0]
                blockList.append([space,col])

        if (len(self.board.diagonal()[self.board.diagonal()==1]) == 2 and 0 in self.board.diagonal()):
            space = np.argwhere(self.board.diagonal()==0)[0][0]
            blockList.append([space,space])
        
        flippedBoard = np.fliplr(self.board)
        if len(flippedBoard.diagonal()[flippedBoard.diagonal()==1]) == 2 and 0 in flippedBoard.diagonal():
            # 2-n for flipping the board back
            # need to take into account for 
            # 0->2, 1->1, 2->0 
            space = np.argwhere(flippedBoard.diagonal()==0)[0][0]
            blockList.append([space,2-space])
        
        return np.array(blockList)

    def Attack(self):
        # check if there are any 2's in each row/col/diag
        # if so add the empty space to the block list
        AttackList = []
        for row in xrange(self.rows):
            if 0 not in self.board[row]:continue
            if 2 in self.board[row]:
                spaces = np.argwhere(self.board[row] == 0)[:,0]
                for col in spaces:
                    AttackList.append([row,col])

        for col in xrange(self.cols):
            if 0 not in self.board[col]:continue
            if 2 in self.board[:,col]:
                spaces = np.argwhere(self.board[:,col] == 0)[:,0]
                for row in spaces:
                    AttackList.append([row,col])
        
        if (2 in self.board.diagonal() and 0 in self.board.diagonal()):
            spaces = np.argwhere(self.board.diagonal() == 0)[:,0]
            for space in spaces:
                AttackList.append([space,space])
        
        flippedBoard = np.fliplr(self.board)
        if (2 in flippedBoard.diagonal() and 0 in flippedBoard.diagonal()):
            # 2-n for flipping the board back
            # need to take into account for
            # 0->2, 1->1, 2->0
            spaces = np.argwhere(flippedBoard.diagonal() == 0)[:,0]
            for space in spaces:
                AttackList.append([space,2-space])
        
        return AttackList

    def FindMaximum(self, scoreBoard):
        currentMax = 0
        space = np.zeros(2)
        
        tieCount = -1
        tieSpaces = []
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                if scoreBoard[row,col] == np.max(scoreBoard):
                    tieCount += 1
                    tieSpaces.append([row,col])
                    space[0] = row
                    space[1] = col

        if tieCount == 0:
            # there is no tie
            return space
        elif tieCount > 0:
            # roll dice to determine winner
            nSides = tieCount + 1. # number of sides of the die
            roll = np.random.randint(0,nSides)
            space[0] = tieSpaces[roll][0]
            space[1] = tieSpaces[roll][1]
            return space

            
