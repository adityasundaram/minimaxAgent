'''
Author: Aditya Sundaram
Course : Artificial Intelligence
Project: Game playing agent
'''
from collections import deque
import sys,math,time
from random import shuffle

class FruitNinjaNode(object):
	def __init__(self,board,boardSize,maxScore,minScore,numFruits,limit):
		self.board = board
		self.boardSize = boardSize
		self.maxScore = maxScore
		self.minScore = minScore
		self.numFruits = numFruits
		self.count = None
		self.limit = limit
		self.moveStart = None

	def displayBoard(self):
		print self.board
		print "Your Score " + str(self.maxScore)
		print "Opponents Score" + str(self.minScore)

	def updateMaxScore(self,tiles):
		self.maxScore = self.maxScore + tiles*tiles

	def updateMinScore(self,tiles):
		self.minScore = self.minScore + tiles*tiles


def checkAndAppend(queue, x, y,val,grid,visited,islandNodes):
	"""Append to the queue only if in bounds of the grid and the cell value is 1."""
	if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
		key = hash((x,y))
		if grid[x][y] == val and key not in visited:
			queue.append((x, y))
			visited[key] = 1
			islandNodes.append((x,y))

def findNeighbhoursInIsland(row, col,grid,val,visited):
	"""Mark all the cells in the current island with value = 2. Breadth-first search."""
	queue = deque()
	islandNodes = []
	key = hash((row,col))
	if key in visited:
		return None
	queue.append((row, col))
	visited[key] = 1
	islandNodes.append((row,col))
	while queue:
		x, y = queue.pop()
		checkAndAppend(queue, x - 1, y,val,grid,visited,islandNodes)
		checkAndAppend(queue, x, y - 1,val,grid,visited,islandNodes)
		checkAndAppend(queue, x + 1, y,val,grid,visited,islandNodes)
		checkAndAppend(queue, x, y + 1,val,grid,visited,islandNodes)

	return islandNodes

def FindIslands(grid,boardSize,val,counter,islandList):
	"""
	:type grid: List[List[str]]
	:rtype: int
	"""

	if len(grid) == 0 or len(grid[0]) == 0:
		return 0
	island_counter = counter
	visited ={}
	for row in range(boardSize):
		for col in range(boardSize):
			if grid[row][col] == val:
				# found an island
				island = findNeighbhoursInIsland(row, col,grid,val,visited)
				if island is not None:
					islandList.append(island)
					island_counter = island_counter + 1

	return islandList,island_counter

def generateBoard(node,move,maxMove):
	moveSize = len(move)
	moveNode = FruitNinjaNode([x[:] for x in node.board],node.boardSize,node.maxScore,node.minScore,node.numFruits,node.limit)
	#moveNode = pickle.loads(pickle.dumps(node,-1))
	moveNode.size = moveSize
	colList = []
	#print move
	firstMove = True
	for index in move:
		if firstMove:
			moveNode.moveStart = ((index[0],index[1]))
			firstMove = False
		moveNode.board[index[0]][index[1]] = '*'
		if index[1] not in colList:
			colList.append(index[1])
	for col in colList:
		eleRows = []
		emptyRows = []
		for i in range(moveNode.boardSize):
			if(moveNode.board[i][col] == '*'):
				emptyRows.append('*')
			else:
				eleRows.append(moveNode.board[i][col])
		row = moveNode.boardSize-1
		while(eleRows):
			moveNode.board[row][col] = eleRows.pop()
			row = row -1
		while(emptyRows):
			moveNode.board[row][col] = emptyRows.pop()
			row = row -1
	if maxMove:
		moveNode.updateMaxScore(len(move))
	else:
		moveNode.updateMinScore(len(move))
	return moveNode


def generatePossibleMoves(node,fruitTypes,maxMove):

	allIslands = []
	totalMoves = 0
	for i in range(0,fruitTypes+1):
		allIslands,islandsFound = FindIslands(node.board,boardSize,str(i),totalMoves,allIslands)
		totalMoves = totalMoves + islandsFound


	allIslands = sorted(allIslands,key= lambda k:len(k) ,reverse=maxMove)
	return totalMoves,allIslands

def checkEmptyBoard(board,boardSize):
	for row in range(boardSize):
		for col in range(boardSize):
			if(board[row][col]!='*'):
				return False
	return True


def findUtility(board,maxScore,minScore,isEmpty):
	if isEmpty:
		return maxScore-minScore

def alpha_beta_search(initNode,alpha,beta):
	#print board
	maxVal, maxBoardNode = alphaBetaMaxValue(initNode, alpha, beta, 0)
	return maxVal, maxBoardNode

#The Alpha Beta Max Value
def alphaBetaMaxValue(node, alpha, beta, depth):

	if(checkEmptyBoard(node.board) == True):
		return findUtility(node.board,node.maxScore,node.minScore,True), node.board

	if(node.limit is not None and node.limit == depth):
		return findUtility(node.board,node.maxScore,node.minScore,True), node.board

	v = -sys.maxint - 1
	key = hash(str(node.board))
	try:
		totalMoves,allMoves = moveMap[key]
	except :
		totalMoves,allMoves = generatePossibleMoves(node,node.numFruits,False)
		moveMap[key] = (totalMoves,allMoves)

	moveToReturn = None
	for i in allMoves:
		newMove = None
		Moveboard = generateBoard(node,i,True)
		val, c = alphaBetaMinValue(Moveboard, alpha, beta, depth + 1)


		#v = max( v, val)
		if val > v:
			newMove = Moveboard
			v= val

		if( v >= beta ):
			#print "pruned "
			return v, Moveboard
		if v > alpha:
			alpha = v
			moveToReturn = newMove
		#node.alpha = max( alpha, v )
	return v, moveToReturn

def checkEmptyBoard(board):
	for i in range(boardSize):
		for j in range(boardSize):
			if board[i][j]!='*' :
				return False
	return True

#The Alpha Beta Min Value
def alphaBetaMinValue(node, alpha, beta, depth):
	if(checkEmptyBoard(node.board) == True):
		return findUtility(node.board,node.maxScore,node.minScore,True), node.board
	if(node.limit is not None and node.limit == depth):
		return findUtility(node.board,node.maxScore,node.minScore,True), node.board

	v = sys.maxint
	key = hash(str(node.board))
	try:
		totalMoves,allMoves = moveMap[key]
	except :
		totalMoves,allMoves = generatePossibleMoves(node,node.numFruits,False)
		moveMap[key] = (totalMoves,allMoves)
	moveToReturn = None
	for j in allMoves:
		newMove = None
		Moveboard = generateBoard(node,j,False)
		val, c = alphaBetaMaxValue(Moveboard, alpha, beta, depth + 1)
		#v = min( v, val)
		if val < v:
			v = val
			newMove = Moveboard
		if(v <= alpha):
			#print "pruned "
			return v,Moveboard
		if v < beta:
			beta = v
			moveToReturn = newMove

	return v, moveToReturn

#Write to file
def PrintBoard(current, n):
	with open('output.txt', 'w') as out:
		out.write(chr(newBoard.moveStart[1] + 65) + str(newBoard.moveStart[0]+1) + '\n')
		for i in range(n):
			line = ""
			for j in range(n):
				line = line + str(current.board[i][j])
			out.write(line + '\r\n')
	out.close()
	return


#Input file
with open('input.txt') as f:
	lines = f.readlines()

#Process input and call algorithms
boardSize = int(lines[0].strip('\n'))
fruitTypes = int(lines[1].strip('\n'))
timeRemaining = float(lines[2].strip('\n'))
board=[]
fruitCount = 0
for i in range(boardSize):
	line = []
	for ele in list(lines[i+3].strip()):
		if ele!='*':
			fruitCount = fruitCount + 1
		line.append(ele)
	board.append(line)

moveMap = {}

tempBoard = FruitNinjaNode(board,boardSize,0,0,fruitTypes,3)
totalIslands = generatePossibleMoves(tempBoard,fruitTypes,True)
totalIslands = len(totalIslands[1])
#print totalIslands
if timeRemaining > 100:
	depth = (timeRemaining*fruitCount)/(totalIslands*boardSize*boardSize*fruitTypes) + 1
else:
	depth = (timeRemaining*fruitCount)/(totalIslands*boardSize*boardSize*fruitTypes)
print depth
if depth <= 0:
	depth = 1

fruitInitialBoard = FruitNinjaNode(board,boardSize,0,0,fruitTypes,min(5,math.ceil(depth)))
print fruitInitialBoard.limit
value,newBoard = alpha_beta_search(fruitInitialBoard,-sys.maxint-1,sys.maxint)
#print value
#newBoard.displayBoard()
PrintBoard(newBoard,newBoard.boardSize)
with open("score.txt","w") as pointer:
	pointer.write(str(newBoard.size)+'\r\n')
#numIslands,possiblemoves = generatePossibleMoves(board,fruitTypes,True)
#print possiblemoves
#sortedMoveIndices = sorted(possiblemoves, key=lambda k: len(possiblemoves[k]), reverse=True)
#for index in sortedMoveIndices:
#	print possiblemoves[index]
'''
if timeRemaining > 100:
	depth = (timeRemaining*fruitTypes)/(totalIslands*boardSize)
else:
	depth = (timeRemaining*fruitTypes)/(totalIslands*boardSize) -1
#print depth
if depth <= 0:
	depth = 1'''




