# coding=utf-8
import os,sys,copy
"""
<N>
<MODE>
<YOUPLAY>
<DEPTH>
<… CELL VALUES …>
<… BOARD STATE …>
"""
readFileList = []
numberOfNodesOnBoard = 0
depthOfPlay = 0
cellValues = []
counter = 0
player = None
root = None
dotPresentInBoard = 0
xPresentInBoard = 1
oPresentInBoard = 2
stake = 1
raid = 2


class node:
    def __init__(self,currentBoard,parent,depth,player):
        global counter
        self.boardState = currentBoard
        self.counter = counter
        self.parent = parent
        self.children = []
        self.depth = depth
        self.valueOfX = None
        self.valueOfO = None
        self.moveType = None
        self.player = player
        self.TotalValue = 0
        counter += 1

    def addChild (self,child):
        self.children.append(child)

    def setValueInBoardState(self,player,i,j):
        self.boardState[i][j] = player

    def checkTheBoardState(self,i,j):
        if self.boardState[i][j] == '.':
            return dotPresentInBoard
        if self.boardState[i][j] == 'X':
            return xPresentInBoard
        if self.boardState[i][j] == 'O':
            return oPresentInBoard

    def setChildToParent(self,child):
        self.children.append(child)


    def calculateValueOfNode(self):
        costOfX = 0
        costOfO = 0
        for i in range(numberOfNodesOnBoard):
            for j in range(numberOfNodesOnBoard):
                if self.boardState[i][j] == "X":
                    costOfX += cellValues[i][j]
                elif self.boardState[i][j] == "O":
                    costOfO += cellValues[i][j]
        self.valueOfX = costOfX
        self.valueOfO = costOfO
        self.TotalValue = self.valueOfX - self.valueOfO if "X" == self.player else self.valueOfO - self.valueOfX

    def setMoveType(self,moveType):
        self.moveType = moveType



def readFile():
    """
    Just read the file and stores in the variable readFile
    :return: nothing
    """
    try:
        if os.path.exists("input.txt"):
            f = open('input.txt', 'r')
            for each_line in f:
                readFileList.append(each_line.strip())
    finally:
        f.close()
        return  0

def construstTree(root):
    depth = 1
    parent = (root)
    currentPlayer = player
    for i in range (depth,depthOfPlay+1):
        #1) Parse through the current board
        #2) Check the current state of the board
        #3) Now determine if there can be a stake, if '.' is returned [create new node if this can be done]
        #4) Now determine if raid can be done, if current player is playing the game [create new node]
        #5) If other player is present in the node then do nothing.
        #6) After creating the node calculate the value of the board, by populating the value of the X player and value of the Y player
        #7) Set the appropriate board player detail
        #8) Calculate the current board value based on the current player set.
        for i in range(0,numberOfNodesOnBoard):
            for j in range(0,numberOfNodesOnBoard):
                boardStateOfParent = copy.deepcopy(parent.boardState)
                boardState = parent.checkTheBoardState(i,j)
                if boardState == dotPresentInBoard:
                    #Create a new node with the board state of the parent
                    child = node(boardStateOfParent,parent,depth,currentPlayer)
                    #Set the stake in the board state
                    child.setValueInBoardState(player,i,j)
                    #set Child to the parent
                    parent.setChildToParent(child)
                    #Calculate the value of the node
                    child.calculateValueOfNode()
                    #Set the stake parameter
                    child.setMoveType(stake)
        

    printTree(root)



def printTree(head):
    headRoot = copy.deepcopy(head)
    queue = []
    queue.append(headRoot)
    while len(queue) != 0:
        top = queue[0]
        queue.pop(0)
        print "Node : " + str(top.counter)
        for i in top.boardState:
            print i
        print "Cost : " , top.TotalValue , "Player : " , top.player , "MoveType : " , top.moveType
        print "-----------------------"

        for temp in top.children:
            queue.append(temp)





def minimax():
    construstTree (root)

if __name__ == "__main__":

    #Read file from input.txt
    readFile()

    numberOfNodesOnBoard = int(readFileList[0])
    #Read the boardState and populate list
    for i in range(4,4+int(readFileList[0])):
        tempList = []
        for j in readFileList[+i].split():
            tempList.append(int(j))
        cellValues.append(tempList)

    tempBoardState = []
    #Read the current board state
    for i in range(4+int(readFileList[0]),4+(int(readFileList[0])*2)):
        tempList = []
        [tempList.append(j) for j in readFileList[i]]
        tempBoardState.append(list(tempList))
    root = node(tempBoardState,None,0,None)

    depthOfPlay = int(readFileList[3])
    player = readFileList[2]

    if readFileList[1].strip() == "MINIMAX":
        minimax()
