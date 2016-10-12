# coding=utf-8
import os,sys,copy, datetime , time
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
playerConstantValue = None
root = None
dotPresentInBoard = 0
xPresentInBoard = 1
oPresentInBoard = 2
stake = 1
raid = 2
asciiOfA = ord("A")


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
        self.pawnPlaced = None
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

    def checkForEligibilityOfRaid(self,i,j):
        if (i-1 >= 0 and (self.checkTheBoardState(i-1,j) == self.player)):
            return True
        elif (j+1 < numberOfNodesOnBoard and (self.checkTheBoardState(i,j+1)==self.player)):
            return True
        elif (j-1 >= 0 and (self.checkTheBoardState(i,j-1)==self.player)):
            return True
        elif (i+1 < numberOfNodesOnBoard and (self.checkTheBoardState(i+1,j) == self.player)):
            return True
        else:
            return False

    def performRaid(self,i,j):
        raid = False
        if self.player == 1:
            player = "X"
        elif self.player == 2:
            player = "O"
        if (i-1 >= 0 and (self.checkTheBoardState(i-1,j) != (self.player and dotPresentInBoard))):
            self.setValueInBoardState(player,i-1,j)
            raid = True
        if (j+1 < numberOfNodesOnBoard and (self.checkTheBoardState(i,j+1)!= (self.player and dotPresentInBoard))):
            self.setValueInBoardState(player, i , j+1)
            raid = True
        if (j-1 >= 0 and (self.checkTheBoardState(i,j-1)!= (self.player and dotPresentInBoard))):
            self.setValueInBoardState(player, i , j - 1)
            raid = True
        if (i+1 < numberOfNodesOnBoard and (self.checkTheBoardState(i+1,j) != (self.player and dotPresentInBoard))):
            self.setValueInBoardState(player, i + 1 , j)
            raid = True
        return raid

    def performRaid2(self,i,j):
        raid = False
        if  self.player == 1:
            player = "X"
        if  self.player == 2:
            player = "O"
        if  i-1 >= 0:
            temp = self.checkTheBoardState(i-1,j)
            if  not ((temp == self.player) or (temp == dotPresentInBoard)):
                self.setValueInBoardState(player,i-1,j)
                raid = True

        if j+1 < numberOfNodesOnBoard :
            temp = self.checkTheBoardState(i,j+1)
            if  not ((temp == self.player) or (temp == dotPresentInBoard)):
                self.setValueInBoardState(player, i, j + 1)
                raid = True

        if  j - 1 >= 0:
            temp = self.checkTheBoardState(i, j - 1)
            if not ((temp == self.player) or (temp == dotPresentInBoard)):
                self.setValueInBoardState(player, i, j - 1)
                raid = True

        if  i + 1 < numberOfNodesOnBoard:
            temp = self.checkTheBoardState(i + 1, j)
            if  not ((temp == self.player) or (temp == dotPresentInBoard)):
                self.setValueInBoardState(player, i + 1, j)
                raid = True
        return raid


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
        self.TotalValue = self.valueOfX - self.valueOfO if playerConstantValue == xPresentInBoard else self.valueOfO - self.valueOfX
        # self.TotalValue = self.valueOfX - self.valueOfO if xPresentInBoard == self.player else self.valueOfO - self.valueOfX

    def setMoveType(self,moveType):
        self.moveType = moveType

    def setThePlaceWhereThePawnIsPlaced(self, location):
        self.pawnPlaced = location



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
    queue = []
    queue.append(parent)
    # for i in range (depth,depthOfPlay+1):
    while len(queue) != 0:
        top = queue[0]
        queue.pop(0)
        if top.depth >= depthOfPlay:
            break
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
                boardStateOfParent = copy.deepcopy(top.boardState)
                boardState = top.checkTheBoardState(i,j)
                if boardState == dotPresentInBoard:
                    isEligibleForRaid = False
                    performRaid = False

                    #Create a new node with the board state of the parent
                    child = node(boardStateOfParent,top,top.depth+1,xPresentInBoard if oPresentInBoard == top.player \
                    else oPresentInBoard)

                    #Set the value of the board state of the parent to null
                    boardStateOfParent = None

                    #Set the stake in the board state
                    child.setValueInBoardState("X" if oPresentInBoard == top.player else "O",i,j)

                    #set Child to the parent
                    top.setChildToParent(child)


                    #Now check if there are corresponding same in the current board of the same player
                    isEligibleForRaid = child.checkForEligibilityOfRaid(i,j)

                    #If eligible check if there are any pawns to raid of the other player and then raid them
                    if isEligibleForRaid == True:
                        performRaid = child.performRaid2(i,j)

                    #Calculate the value of the node
                    child.calculateValueOfNode()

                    #Set the stake parameter
                    child.setMoveType(raid if True == performRaid else stake)

                    #Placement of pawn
                    child.setThePlaceWhereThePawnIsPlaced(chr(asciiOfA + j) + str(i+1))

                    #Add this child to the queue
                    queue.append(child)
                    #
                    # print "Node : " + str(child.counter)
                    # for printing in child.boardState:
                    #     print printing
                    # print "Cost : ", str(child.TotalValue) , "Player : ", child.player, "MoveType : ", child.moveType , "Depth : " , child.depth ,\
                    #     "Pawn : " + child.pawnPlaced , "Parent : " , child.parent.counter
                    # print "-----------------------"
                    # print child.counter
    print "#####################################################"
    # printTree(root)

def printTree(head):
    headRoot = copy.deepcopy(head)
    queue = []
    queue.append(headRoot)
    while len(queue) != 0:
        tempQ = []
        top = queue[0]
        queue.pop(0)
        print "Node : " + str(top.counter)
        for printing in top.boardState:
            print printing
        print "Cost : ", str(
            top.TotalValue), "Player : ", top.player, "MoveType : ", top.moveType, "Depth : ", top.depth, \
            "Pawn : " + "..." if top.pawnPlaced == None else top.pawnPlaced , "Parent : ", "..." if top.parent == None\
            else top.parent.counter
        print "-----------------------"
        for temp in top.children:
            tempQ.append(temp)
        queue = tempQ + queue

def minimax():
    construstTree (root)
    iteratorRoot = copy.deepcopy(root)
    value = []
    for childIterator in iteratorRoot.children:
        value.append(miniMaxValue2(childIterator,False))
    selectedNode = value[0]
    # if selectedNode.player == playerConstantValue:
    for i in range(1, len(value)):
        selectedNode = value[i] if value[i].TotalValue > selectedNode.TotalValue or \
                                   (value[i].moveType == 1 and selectedNode.moveType == 2 and\
                                    value[i].TotalValue == selectedNode.TotalValue) else selectedNode

    print "#########################################################"
    print selectedNode

    for printing in selectedNode.boardState:
        print printing

    print "Cost : ", str(selectedNode.TotalValue), "Player : ", selectedNode.player, "MoveType : ", \
        selectedNode.moveType, "Depth : ",\
        selectedNode.depth, \
        "Pawn : " + selectedNode.pawnPlaced , "Move Type : " + "Raid" if selectedNode.moveType == 2 else "Stake"

    print "#######################################################"
    # printTree(root)

def miniMaxValue2(root,maximize):

    if len(root.children) == 0:
        return  root

    elif maximize:
        v = miniMaxValue2(root.children[0],False)
        for i in range(1,len(root.children)):
            temp = miniMaxValue2(root.children[i],False)
            v = temp if temp.TotalValue > v.TotalValue else v
        root.TotalValue = v.TotalValue
        return root
    else:
        v = miniMaxValue2(root.children[0],True)
        for i in range(1,len(root.children)):
            temp = miniMaxValue2(root.children[i],True)
            v = temp if temp.TotalValue < v.TotalValue else v
        root.TotalValue = v.TotalValue
        return root

def miniMaxValue(root):

    if depthOfPlay == root.depth and len(root.children) == 0:
        return root

    elif root.player == playerConstantValue:
        # print "Return the Highest Value"
        childToSend = root.children[0]
        for i in range(1,len(root.children)):
            childToSend = root.children[i] if root.children[i].TotalValue > childToSend.TotalValue else childToSend
        # root.TotalValue = childToSend.TotalValue
        return miniMaxValue(childToSend)

    else:
        # print "Return the lowest value"
        childToSend = root.children[0]
        for i in range(1,len(root.children)):
            childToSend = root.children[i] if root.children[i].TotalValue < childToSend.TotalValue else childToSend
        # root.TotalValue = childToSend.TotalValue
        return miniMaxValue(childToSend)

def buildChildrenForOneLevel(root):
    depth = root.depth+1
    parent = (root)
    currentPlayer = player
    queue = []
    queue.append(parent)
    while len(queue) != 0:
        top = queue[0]
        queue.pop(0)
        if top.depth >= depth:
            break
        for i in range(0, numberOfNodesOnBoard):
            for j in range(0, numberOfNodesOnBoard):
                boardStateOfParent = copy.deepcopy(top.boardState)
                boardState = top.checkTheBoardState(i, j)
                if boardState == dotPresentInBoard:
                    isEligibleForRaid = False
                    performRaid = False

                    # Create a new node with the board state of the parent
                    child = node(boardStateOfParent, top, top.depth + 1,
                                 xPresentInBoard if oPresentInBoard == top.player \
                                     else oPresentInBoard)

                    #Set the board state to none
                    boardStateOfParent = None

                    # Set the stake in the board state
                    child.setValueInBoardState("X" if oPresentInBoard == top.player else "O", i, j)

                    # set Child to the parent
                    top.setChildToParent(child)

                    # Now check if there are corresponding same in the current board of the same player
                    isEligibleForRaid = child.checkForEligibilityOfRaid(i, j)

                    # If eligible check if there are any pawns to raid of the other player and then raid them
                    if isEligibleForRaid == True:
                        performRaid = child.performRaid2(i, j)

                    # Calculate the value of the node
                    child.calculateValueOfNode()

                    # Set the stake parameter
                    child.setMoveType(raid if True == performRaid else stake)

                    # Placement of pawn
                    child.setThePlaceWhereThePawnIsPlaced(chr(asciiOfA + j) + str(i + 1))

                    # Add this child to the queue
                    queue.append(child)

def alphaBeta():

    buildChildrenForOneLevel(root)
    #Run algorithm from here
    value = alphaBetaMinValue(root.children[0], float("-inf"), float("inf"))
    for i in range(1,len(root.children)):
        temp = alphaBetaMinValue(root.children[i],float("-inf"),float("inf"))
        value = temp if temp.TotalValue > value.TotalValue else value
        temp = None
        value.children = None

    value = root.children[0]
    for i in range(1,len(root.children)):
        # value = root.children[i] if root.children[i].TotalValue > value.TotalValue else value

        value = root.children[i] if root.children[i].TotalValue > value.TotalValue or \
                                    (root.children[i].TotalValue == value.TotalValue and \
                                     root.children[i].moveType == 1 and value.moveType == 2)\
                                    else value

    print "#########################################################"
    print value

    for printing in value.boardState:
        print printing

    print "Cost : ", str(value.TotalValue), "Player : ", value.player, "MoveType : ", \
        value.moveType, "Depth : ", \
        value.depth, \
        "Pawn : " + value.pawnPlaced , "Move Type : " + "Raid" if value.moveType == 2 else "Stake"

    print "#######################################################"

def alphaBetaMaxValue(root,alpha,beta):
    if root.depth == depthOfPlay:
        return root
    buildChildrenForOneLevel(root)
    value = alphaBetaMinValue(root.children[0],alpha,beta)
    for i in range(1,len(root.children)):
        temp = alphaBetaMinValue(root.children[i],alpha,beta)
        # print "Child Counter : ", temp.counter
        value = temp if temp.TotalValue > value.TotalValue else value
        if value.TotalValue >= beta:
            return value
        alpha = value.TotalValue if value.TotalValue > alpha else alpha
    root.TotalValue = alpha
    return value

def alphaBetaMinValue(root,alpha,beta):
    if root.depth == depthOfPlay:
        return root
    # value = float("inf")
    buildChildrenForOneLevel(root)
    value = alphaBetaMaxValue(root.children[0],alpha,beta)
    for i in range(1,len(root.children)):
        temp = alphaBetaMaxValue(root.children[i],alpha,beta)
        # print "Child Counter : ", temp.counter
        value = temp if temp.TotalValue < value.TotalValue else value
        if value.TotalValue <= alpha:
            return value
        beta = value.TotalValue if value.TotalValue < beta else beta
    root.TotalValue = beta
    return value

def alphaBetaMaxValue2(root,alpha,beta):
    value = None
    if root.depth == depthOfPlay:
        return root

    depth = root.depth + 1
    parent = (root)
    currentPlayer = player
    queue = []
    queue.append(parent)
    while len(queue) != 0:
        top = queue[0]
        queue.pop(0)
        if top.depth >= depth:
            break
        for i in range(0, numberOfNodesOnBoard):
            for j in range(0, numberOfNodesOnBoard):
                boardStateOfParent = copy.deepcopy(top.boardState)
                if i>=numberOfNodesOnBoard or j>=numberOfNodesOnBoard:
                    print "break"
                boardState = top.checkTheBoardState(i, j)
                if boardState == dotPresentInBoard:
                    isEligibleForRaid = False
                    performRaid = False

                    # Create a new node with the board state of the parent
                    child = node(boardStateOfParent, top, top.depth + 1,
                                 xPresentInBoard if oPresentInBoard == top.player \
                                     else oPresentInBoard)

                    # Set the stake in the board state
                    child.setValueInBoardState("X" if oPresentInBoard == top.player else "O", i, j)

                    # set Child to the parent
                    top.setChildToParent(child)

                    # Now check if there are corresponding same in the current board of the same player
                    isEligibleForRaid = child.checkForEligibilityOfRaid(i, j)

                    # If eligible check if there are any pawns to raid of the other player and then raid them
                    if isEligibleForRaid == True:
                        performRaid = child.performRaid2(i, j)

                    # Calculate the value of the node
                    child.calculateValueOfNode()

                    # Set the stake parameter
                    child.setMoveType(raid if True == performRaid else stake)

                    # Placement of pawn
                    child.setThePlaceWhereThePawnIsPlaced(chr(asciiOfA + j) + str(i + 1))

                    # Add this child to the queue
                    queue.append(child)

                    temp = alphaBetaMinValue2(child, alpha, beta)
                    if value != None:
                        value = temp if temp.TotalValue > value.TotalValue else value
                    else:
                        value = temp
                    if value.TotalValue >= beta:
                        return value
                    alpha = value.TotalValue if value.TotalValue > alpha else alpha
                    print "Child Counter : " , child.counter
    root.TotalValue = alpha
    return value

def alphaBetaMinValue2(root,alpha,beta):
    value = None
    if root.depth == depthOfPlay:
        return root
    depth = root.depth + 1
    parent = (root)
    currentPlayer = player
    queue = []
    queue.append(parent)
    while len(queue) != 0:
        top = queue[0]
        queue.pop(0)
        if top.depth >= depth:
            break
        for i in range(0, numberOfNodesOnBoard):
            for j in range(0, numberOfNodesOnBoard):
                boardStateOfParent = copy.deepcopy(top.boardState)
                boardState = top.checkTheBoardState(i, j)
                if boardState == dotPresentInBoard:
                    isEligibleForRaid = False
                    performRaid = False

                    # Create a new node with the board state of the parent
                    child = node(boardStateOfParent, top, top.depth + 1,
                                 xPresentInBoard if oPresentInBoard == top.player \
                                     else oPresentInBoard)

                    # Set the stake in the board state
                    child.setValueInBoardState("X" if oPresentInBoard == top.player else "O", i, j)

                    # set Child to the parent
                    top.setChildToParent(child)

                    # Now check if there are corresponding same in the current board of the same player
                    isEligibleForRaid = child.checkForEligibilityOfRaid(i, j)

                    # If eligible check if there are any pawns to raid of the other player and then raid them
                    if isEligibleForRaid == True:
                        performRaid = child.performRaid2(i, j)

                    # Calculate the value of the node
                    child.calculateValueOfNode()

                    # Set the stake parameter
                    child.setMoveType(raid if True == performRaid else stake)

                    # Placement of pawn
                    child.setThePlaceWhereThePawnIsPlaced(chr(asciiOfA + j) + str(i + 1))

                    # Add this child to the queue
                    queue.append(child)

                    temp = alphaBetaMinValue2(child, alpha, beta)
                    if value != None:
                        value = temp if temp.TotalValue < value.TotalValue else value
                    else:
                        value = temp
                    if value.TotalValue <= alpha:
                        return value
                    beta = value.TotalValue if value.TotalValue < beta else beta
    root.TotalValue = beta
    return value

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
    root = node(tempBoardState,None,0,oPresentInBoard if str(readFileList[2]) == "X" else xPresentInBoard)



    depthOfPlay = int(readFileList[3])
    player = readFileList[2]
    playerConstantValue = oPresentInBoard if player == "O" else xPresentInBoard

    start = time.time()
    if readFileList[1].strip() == "MINIMAX":
        minimax()
    if readFileList[1].strip() == "ALPHABETA":
        alphaBeta()
    end = time.time()
    print end - start