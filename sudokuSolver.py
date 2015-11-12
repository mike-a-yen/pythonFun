import numpy as np

board = np.zeros([9,9,10],dtype=int)

def InitializeBoard(board):
    board[0,3] = 4
    board[0,4] = 8
    board[0,7] = 9
    board[1,6] = 6
    board[2,0] = 3
    board[2,2] = 1
    board[2,3] = 9
    board[3,1] = 7
    board[3,3] = 2
    board[3,4] = 4
    board[3,7] = 1
    board[4,0] = 2
    board[4,8] = 7
    board[5,1] = 4
    board[5,4] = 1
    board[5,5] = 6
    board[5,7] = 3
    board[6,5] = 9
    board[6,6] = 2
    board[6,8] = 4
    board[7,2] = 8
    board[8,1] = 6
    board[8,4] = 7
    board[8,5] = 5
    print "Starting board"
    print board
    return board


board = InitializeBoard(board)
while 0 in board[:,:,0]:
    for x in xrange(len(board)):
        for y in xrange(len(board)):
            for i in xrange(1,10):
                beginX = 3*(x/3)
                endX = beginX+3
                beginY = 3*(y/3)
                endY = beginY+3
                block = board[beginX:endX,beginY:endY]
                if (i not in board[x]) and (i not in board[:,y]) and (i not in block):
                    board[x,y,i] = i
    for x in xrange(len(board)):
        for y in xrange(len(bboard)):
            possibilities = board[x,y,1:]
            for num in possibilities:
                if num == 0: continue
                

