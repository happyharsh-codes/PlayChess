import time

board = ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
         "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
         "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6", 
         "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
         "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
         "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
         "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
         "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]

class Chessboard:

    # Creates a vitual ChessBoard and keeps track of all the pieces and moves during the game

    def __init__(self):
        self.__chessboard = []
        self.is_black_checked = False
        self.is_white_checked = False
        self.is_white_checkmated = False
        self.is_black_checkmate = False

        self.black_material_points = 0
        self.white_material_points = 0

        self.black_can_castle = False
        self.white_can_castle = False

        self.play_turn = "white"
        self.moveNo = 0
        self.__moveHistory = ""

        self.__initializeBoard__()

    def __initializeBoard__(self):
        self.__chessboard = [ChessPiece("rook","black","a8"), ChessPiece("night","black","b8"), ChessPiece("bishop","black","c8"),ChessPiece("queen","black","d8"), ChessPiece("king","black","e8"), ChessPiece("bishop","black","f8"), ChessPiece("night","black","g8"), ChessPiece("rook","black","h8")]
        self.__chessboard.extend([ChessPiece("pawn","black",f"{chr(96+i)}7") for i in range(1, 9) ])
        self.__chessboard.extend([None for i in range(32)])
        self.__chessboard.extend([ChessPiece("pawn","white",f"{chr(96+i)}2") for i in range(1, 9) ])
        self.__chessboard.extend([ChessPiece("rook","white","a1"), ChessPiece("night","white","b1"), ChessPiece("bishop","white","c1"),ChessPiece("queen","white","d1"), ChessPiece("king","white","e1"), ChessPiece("bishop","white","f1"), ChessPiece("night","white","g1"), ChessPiece("rook","white","h1")])
        self.__history = ""

        print(self.__chessboard)
        start = time.time()
        for piece in self.__chessboard:
            if piece:
                moves = self.__generateLegalMoves(piece)
                print(piece.movement)
                print("Position: ", piece.pos, board[self.__chessboard.index(piece)])
                print(moves)
                piece.setLegalMoves(moves)
        print("Latency: generated all moves in ", time.time()-start)

    def __getPlainMoves(self, piece, board):
        plainMoves = []
        index = board.index(piece)
        for direction in piece.movement:
            currentPos = index
            while True:
                currentPos += direction
                if (0 <= currentPos < 64):
                    if piece.type == "night" and abs((currentPos%8)-(index%8)) > 2: 
                        break
                    if board[currentPos] == None:
                        plainMoves.append(currentPos)
                    elif board[currentPos].color != piece.color:
                        plainMoves.append(currentPos)
                        break
                    else:
                        break
                else: 
                    break
                if piece.moveRange == 1:
                    break
        #extra pawn moves need to be addes diagonal capturing and enpassant promotion etc

        return plainMoves

    def __generateLegalMoves(self, piece):
        index = self.__chessboard.index(piece)
        plainMoves = self.__getPlainMoves(piece, self.__chessboard)
        
        
        #now validating moves .. i.e if piece is pinned the move will be illegal .. so removing those invalid moves now
        print("plain moves:", plainMoves)
        legalMoves = plainMoves.copy()
        
        for move in plainMoves:
            for pieces in self.__chessboard:
                if pieces and pieces.type in ["queen", "rook", "bishop"] and pieces.color != piece.color:
                    boardcopy = self.__chessboard.copy()
                    boardcopy[index] = None
                    boardcopy[move] = piece
                    oppPlainMoves = self.__getPlainMoves(pieces, boardcopy)
                    for oppMoves in oppPlainMoves:
                        if boardcopy[oppMoves].type == "king":
                            legalMoves.remove(move)
                            break

        return legalMoves


    def __isBoardCheck(self):
        for piece in self.__chessboard:
            if piece and piece.color != self.play_turn:
                for moves in piece.getLegalMoves():
                    if self.__chessboard[moves] andself.__chessboard[moves].type == "king":
                        return True
        return False


    def getPiece(self, loc = None):
        for piece in self.__chessboard:
            if piece:
                if piece.pos == loc:
                    return piece

        return None
        

    def move(self, piece, loc):
        #Moves the piece to location .. location must be from piece.legalMoves that has been generated already
        #also move __chessboard list so as to get correct index
        #regenerate valid moves for all pieces ie. run update after each move
        # checks for : captures, check and checkmate
        # does not check for promotion as user response it required: handled explitictly
        # generates move notations 
        move = {"piece": None, "initial": piece.pos, "final": loc, "type":None, "capture" : False, "check": False, "checkmate": False, "promotion": False, "notation": ""}

        #invalid move
        if loc not in self.getLegalMoves(piece):
            move['type'] = "illegal"
            return move
        
        #normal move
        self.play_turn = "white" if piece.color == "black" else "black"
        pos_index = board.index(piece.pos)
        loc_index = board.index(loc)
        notation = ""

        piece.movePiece(loc)
        move['piece'] = piece
        move["type"] = None
        if piece.type == "night" or piece.type == "rook":
            for i in self.__chessboard:
                if i and i.color == piece.color and loc in self.getLegalMoves(i):
                    file = board[pos_index][0]
                    if file != i.pos[0]:
                        notation = piece.type[0].upper() + file + notation 
                    else:
                        rank = board[pos_index][1]
                        notation = piece.type[0].upper() + rank + notation 
                    break
            else:
                notation = piece.type[0].upper() + notation                    
        elif piece != "pawn":
            notation = piece.type[0].upper() + notation

        if self.__chessboard[loc_index] != None: # capture check
            move["type"] = "capture"
            move["capture"] = True
            notation =  notation + "x" + loc
            if piece.type == "pawn":
                notation = board[pos_index][0] + "x" + loc
        else: notation += loc
        self.__chessboard[loc_index] = piece
        self.__chessboard[pos_index] = None



        #castelling Check
        if piece.type == "king" and abs(loc_index - pos_index) == 2:
            move["type"] = "castle"
            if (loc_index - pos_index) == 2:
                notation = "0-0-0"
                if piece.color == "black":
                    self.__chessboard[loc_index+1] = self.__chessboard[0]
                    self.__chessboard[0] = None
                if piece.color == "white":
                    self.__chessboard[loc_index+1] = self.__chessboard[57]
                    self.__chessboard[57] = None
            else: 
                notation = "0-0"
                if piece.color == "black":
                    self.__chessboard[loc_index-1] = self.__chessboard[7]
                    self.__chessboard[7] = None
                if piece.color == "white":
                    self.__chessboard[loc_index-1] = self.__chessboard[63]
                    self.__chessboard[63] = None
            move["type"] = "castle"

        # getting brand new updated moves for each piece
        for newpiece in self.__chessboard:
            if newpiece:
                newpiece.setLegalMoves(self.__generateLegalMoves(piece))

        #promotions are not dealt here they have been dealt explicitly

        #checks and checkmates
        move["check"] = self.__isBoardCheck()

        if move["check"]:
            notation += "+"
            move["type"] = "check"
            if piece.color == "black":
                self.is_white_checked = True
                self.white_can_castle = False
            else:
                self.is_black_checked = True
                self.black_can_castle = False
            allLegalMoves = []
            for newpiece in self.__chessboard:
                if newpiece and newpiece.color != piece.color:
                    allLegalMoves.extend(newpiece.getLegalMoves())

            if allLegalMoves == []:
                #checkmated Haha >_< 
                notation = notation[:-1] + "#"
                move["type"] = "checkmate"
                move["checkmate"] = True
                if piece.color == "black":
                    self.is_white_checkmated = True
                else: 
                    self.is_black_checkmate = True
        else:
            self.is_white_checked = False
            self.is_black_checked = False


        move["notation"] = notation
        self.moveHistory(move["notation"])


        return move


    def moveHistory(self, notation):
        self.moveNo += 1
        if self.play_turn == "black":
            #add white move
            self.__history += f" {self.moveNo}. {notation}"
        else:
            #add black move
            self.__history += f" {notation}"

    def undoMove():
        pass

    def getLegalMoves(self, piece):
        moves = []
        for move in piece.getLegalMoves():
            moves.append(board[move])
        return moves



class ChessPiece():

    def __init__(self, type, color, postion = None):
        """Type: <pawn bishop rook queen king night>. Color: <black white>. Position: chess notiaion"""
        if type.lower() not in ["pawn", "bishop", "queen", "king", "night", "rook"]:
            raise "Invalid chess piece error"
        if color.lower() not in ["black", "white"]:
            raise "Invalid chess color"
        self.type = type.lower()
        self.color = color.lower()
        self.movement = []
        self.captureMovement = "same" # only for pawns: 'same' for all piece so it will be ignored, but for pawn can be : -9, -7, +7, +9 
        self.moveRange = None

        self.__moveHistory = []
        self.__legalMoves = []
        self.pos = postion
        self.setMovement()

    def setMovement(self):
        if self.type == "pawn":
            if self.color == "black":
                self.movement = [+8]
                self.moveRange = +1
                self.captureMovement = [+7, +9]
            elif self.color == "white":
                self.movement = [-8]
                self.moveRange = +1
                self.captureMovement = [-7, -9]

        elif self.type == "rook":
            self.movement = [+8, -8, +1, -1]
            self.moveRange = "infinite"

        elif self.type == "bishop":
            self.movement = [-9, -7, +7, +9]
            self.moveRange = "infinite"

        elif self.type == "night":
            self.movement = [-17, -15, -10, -6, +6, +10, +15, +17]
            self.moveRange = 1

        elif self.type == "king":
            self.movement = [-9, -8, -7, -1, +1, +7, +8, +9]
            self.moveRange = 1

        elif self.type == "queen":
            self.movement = [-9, -8, -7, -1, +1, +7, +8, +9]
            self.moveRange = "infinite"
        
    def movePiece(self, loc):
        self.pos = loc
        self.__moveHistory.append(loc)

    def moveHistory(self):
        return self.__moveHistory
            
    def getLegalMoves(self):
        return self.__legalMoves

    def setLegalMoves(self, moves):
        self.__legalMoves = moves
