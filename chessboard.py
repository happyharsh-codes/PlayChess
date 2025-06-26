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

        
        for i in range(8):
            for j in range(8):
                if self.__chessboard[i*8 + j]:
                    print(self.__chessboard[i*8 +j].color[0] + self.__chessboard[i*8 + j].type[0] , end=" ")

                else: print("   ", end="")
            print()

        start = time.time()
        for piece in self.__chessboard:
            if piece:
                moves = self.__generateLegalMoves(piece)
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
                        if piece.type == "pawn":
                            break
                        plainMoves.append(currentPos)
                        break
                    else:
                        break
                else: 
                    break
                if piece.moveRange == 1:
                    break

        #extra pawn moves need piece be addes diagonal capturing and enpassant promotion etc
        if piece.type == "pawn":
            if piece.color == "black":
                if piece.pos[1] == "7" and board[index+8] == None and board[index+16] == None:
                    plainMoves.append(index+16)
                if (index%8) != 0 and 0<=index+7<64:
                    if board[index+7] and board[index+7].color != piece.color:
                        plainMoves.append(index+7)
                if (index%8) != 7 and 0<=index+9<64:
                    if board[index+9] and board[index+9].color != piece.color:
                        plainMoves.append(index+9)
            if piece.color == "white":
                if piece.pos[1] == "2" and board[index-8] == None and board[index-16] == None:
                    plainMoves.append(index-16)
                if (index%8) != 0 and 0<=index-9<64:
                    if board[index-9] and board[index-9].color != piece.color:
                        plainMoves.append(index-9)
                if (index%8) != 7 and 0<=index-7<64:
                    if board[index-7] and board[index-7].color != piece.color:
                        plainMoves.append(index-7)

        #castelling
        if piece.type == "king":
            pass

        #enpassant



        return plainMoves

    def __generateLegalMoves(self, piece):
        index = self.__chessboard.index(piece)
        plainMoves = self.__getPlainMoves(piece, self.__chessboard)
        
        
        #now validating moves .. i.e if piece is pinned the move will be illegal .. so removing those invalid moves now
        legalMoves = plainMoves.copy()
        
        for move in plainMoves:
            boardcopy = self.__chessboard.copy()
            boardcopy[index] = None
            boardcopy[move] = piece
            for pieces in boardcopy:
                if pieces and pieces.type in ["queen", "rook", "bishop"] and pieces.color != piece.color:
                    oppPlainMoves = self.__getPlainMoves(pieces, boardcopy)
                    for oppMoves in oppPlainMoves:
                        if boardcopy[oppMoves] and boardcopy[oppMoves].type == "king":
                            if move in legalMoves:
                                legalMoves.remove(move)
                            break

        return legalMoves


    def __isBoardCheck(self):
        for piece in self.__chessboard:
            if piece and piece.color != self.play_turn:
                for moves in piece.getLegalMoves():
                    if self.__chessboard[moves] and self.__chessboard[moves].type == "king":
                        return True
        return False


    def getPiece(self, loc):
        for piece in self.__chessboard:
            if piece:
                if piece.pos == loc:
                    return piece

        return None
        
    def addCastling(self):
        print("castelling run")
        for piece in self.__chessboard:
            if piece and piece.color == self.play_turn and piece.type == "king":
                if piece.moveHispiecery() != []:
                    return
                index = self.__chessboard.index(piece)
                if self.__chessboard[index-1] == None and self.__chessboard[index-2] == None and self.__chessboard[index-3] == None:
                    for oppPieces in self.__chessboard:
                        if oppPieces and oppPieces.color != self.play_turn:
                            moves = oppPieces.getLegalMoves()
                            if (index-1) in moves or (index-2) in moves or (index-3) in moves:
                                break
                    else:
                        if self.__chessboard[index-4] and self.__chessboard[index-4].moveHispiecery() == []:
                            legalMoves = piece.getLegalMoves()
                            legalMoves.append(index-2)
                            piece.setLegalMoves(legalMoves)
                            print("casteling added")
                if self.__chessboard[index+1] == None and self.__chessboard[index+2] == None:
                    for oppPieces in self.__chessboard:
                        if oppPieces and oppPieces.color != self.play_turn:
                            moves = oppPieces.getLegalMoves()
                            if (index+1) in moves or (index+2) in moves:
                                break
                    else:
                        if self.__chessboard[index+3] and self.__chessboard[index+3].moveHispiecery() == []:
                            legalMoves = piece.getLegalMoves()
                            legalMoves.append(index+2)
                            piece.setLegalMoves(legalMoves)
                            print("casteling added")


    def addEnpassant(self):
        if self.__moveHistory == "": #first move so no hispiecery
            return
        lastMove = self.__moveHistory.split()[-1]
        print("Enpassant enter",lastMove)
        for index, oppPawn in enumerate(self.__chessboard):
            if oppPawn and oppPawn.type == "pawn" and oppPawn.color == self.play_turn:
                if oppPawn.pos[0] != "a" and self.__chessboard[index-1]:
                    if self.__chessboard[index-1].color != self.play_turn and self.__chessboard[index-1].type == "pawn":
                        file = self.__chessboard[index-1].pos[0]
                        if self.play_turn == "black": 
                            expectedLastMove = file+"4" 
                            dest = file+"3"
                        else: 
                            expectedLastMove = file+"5"
                            dest = file+"6"
                        if expectedLastMove == lastMove:
                            legalMoves = oppPawn.getLegalMoves()
                            legalMoves.append(board.index(dest))
                            oppPawn.setLegalMoves(legalMoves)
                            print("enpassant added for ", lastMove)
                            return
                if oppPawn.pos[0] != "h" and self.__chessboard[index+1]:
                    if self.__chessboard[index+1].color != self.play_turn and self.__chessboard[index+1].type == "pawn":
                        file = self.__chessboard[index+1].pos[0]
                        if self.play_turn == "black": 
                            expectedLastMove = file+"4" 
                            dest = file+"3"
                        else: 
                            expectedLastMove = file+"5"
                            dest = file+"6"
                        if expectedLastMove == lastMove:
                            legalMoves = oppPawn.getLegalMoves()
                            legalMoves.append(board.index(dest))
                            oppPawn.setLegalMoves(legalMoves)
                            print("enpassant added for ", lastMove)
                            return
                    

    def promote(self, pending_move, loc, piece, prevNotation):
        if loc[1] not in ['1',"8"]:
            return
        color = piece.split("-")[0]
        piece = piece.split("-")[1]
        notation = prevNotation + "=" + piece[0].upper()
        pending_move["type"] = "promotion"
        piece = ChessPiece(piece, color=color, postion=loc)
        loc = board.index(loc)
        self.__chessboard[loc] = piece
        pieceLegalMoves = self.__generateLegalMoves(piece)
        self.__chessboard[loc].setLegalMoves(pieceLegalMoves)


        if self.__isBoardCheck():
            notation += "+"
            pending_move["check"] = True
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
                pending_move["checkmate"] = True
                print("checkmated haha")
                if piece.color == "black":
                    self.is_white_checkmated = True
                else: 
                    self.is_black_checkmate = True
        
        for king in self.__chessboard:
            if king and king.type == 'king' and king.color != color:
                kingMoves = king.getLegalMoves()
                if king.pos == "e1" and board.index("g1") in kingMoves and (board.index("e1") in pieceLegalMoves or board.index("g1") in pieceLegalMoves or board.index("f1") in pieceLegalMoves or board.index('h1') in pieceLegalMoves) :
                    kingLegalMoves = king.getLegalMoves()
                    kingLegalMoves.remove(board.index("g1"))
                if king.pos == "e1" and board.index("c1") in kingMoves and (board.index("e1") in pieceLegalMoves or board.index("d1") in pieceLegalMoves or board.index("c1") in pieceLegalMoves or board.index('b1') in pieceLegalMoves or board.index("a1")):
                    kingLegalMoves = king.getLegalMoves()
                    kingLegalMoves.remove(board.index("c1"))
                if king.pos == "e8" and board.index("g8") in kingMoves and (board.index("e8") in pieceLegalMoves or board.index("g8") in pieceLegalMoves or board.index("f8") in pieceLegalMoves or board.index('h8')):
                    kingLegalMoves = king.getLegalMoves()
                    kingLegalMoves.remove(board.index("g8"))
                if king.pos == "e8" and board.index("c8") in kingMoves and (board.index("e8") in pieceLegalMoves or board.index("d8") in pieceLegalMoves or board.index("c8") in pieceLegalMoves or board.index('b8') in pieceLegalMoves or board.index("a8")):
                    kingLegalMoves = king.getLegalMoves()
                    kingLegalMoves.remove(board.index("c8"))

        pending_move["notation"] = notation
        print("===== CHESSBOARD =====")
        for i in range(8):
            for j in range(8):
                if self.__chessboard[i*8 + j]:
                    print(self.__chessboard[i*8 +j].color[0] + self.__chessboard[i*8 + j].type[0], end=" ")
                else:
                    print("   ", end="")
            print()
        print(">>>> MOVE: ", pending_move)
        return pending_move
    

    def move(self, piece, loc):
        #Moves the piece piece location .. location must be from piece.legalMoves that has been generated already
        #also move __chessboard list so as piece get correct index
        #regenerate valid moves for all pieces ie. run update after each move
        # checks for : captures, check and checkmate
        # Checks for enPassant
        # NOTE: does not check for promotion as user response it required: handled explitictly -> returns move type = "promotion pending" then you have piece manully call the promote function with the user input and then you'll get the full move summary
        # generates move notations 
        # returns move summarty move["type"] can be from ["move", "capture", "check", "checkmate", "enpassant", "promotion"]
        move = {"piece": None, "initial": piece.pos, "final": loc, "type": None,"check": False, "checkmate": False, "notation": ""}

        #invalid move
        if loc not in self.getLegalMoves(piece):
            move['type'] = "illegal"
            return move
        
        #normal move
        self.play_turn = "white" if piece.color == "black" else "black"
        pos_index = board.index(piece.pos)
        loc_index = board.index(loc)
        notation = ""

        move['piece'] = piece.color+ " " +piece.type
        move["type"] = "move"
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
        elif piece.type != "pawn":
            notation = piece.type[0].upper() + notation

        #Capture Check
        if self.__chessboard[loc_index] != None:
            move["type"] = "capture"
            notation =  notation + "x" + loc
            if piece.type == "pawn":
                notation = board[pos_index][0] + "x" + loc
        else: notation += loc

        #enPassant check:
        if piece.type == "pawn" and self.__chessboard[board.index(loc)] == None and piece.pos[0] != loc[0]:
            if loc[1] == "3":
                capturePiece = loc[0] + "4"
            elif loc[1] == "6":
                capturePiece = loc[0] + "5"

            self.__chessboard[board.index(capturePiece)] = None
            move["type"] = "enpassant"
            notation = piece.pos[0] + "x" +loc

        #Now moving the piece
        piece.movePiece(loc)
        self.__chessboard[loc_index] = piece
        self.__chessboard[pos_index] = None

        #castelling Check
        if piece.type == "king" and abs(loc_index - pos_index) == 2:
            move["type"] = "castle"
            if (loc_index - pos_index) == -2:
                notation = "0-0-0"
                if piece.color == "black":
                    self.__chessboard[loc_index+1] = self.__chessboard[0]
                    self.__chessboard[loc_index+1].pos = "d8"
                    self.__chessboard[0] = None
                if piece.color == "white":
                    self.__chessboard[loc_index+1] = self.__chessboard[56]
                    self.__chessboard[loc_index+1].pos = "d1"
                    self.__chessboard[56] = None
            else: 
                notation = "0-0"
                if piece.color == "black":
                    self.__chessboard[loc_index-1] = self.__chessboard[7]
                    self.__chessboard[loc_index+1].pos = "f8"
                    self.__chessboard[7] = None
                if piece.color == "white":
                    self.__chessboard[loc_index-1] = self.__chessboard[63]
                    self.__chessboard[loc_index+1].pos = "f1"
                    self.__chessboard[63] = None

        # getting brand new updated moves for each piece
        for newpiece in self.__chessboard:
            if newpiece:
                newpiece.setLegalMoves(self.__generateLegalMoves(newpiece))

        #self.addEnpassant()
        if loc in ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"]:
            leftPiece = None
            rightPiece = None
            if piece.pos[0] != "h":
                rightPiece = (self.__chessboard[loc_index + 1])
            if piece.pos[0] != "a":
                leftPiece = (self.__chessboard[loc_index - 1])
            if piece.color == "white": file= "3" 
            else: file= "6"

            if (rightPiece and rightPiece.color != piece.color and rightPiece.type == "pawn"):
                legalMoves = rightPiece.getLegalMoves()
                legalMoves.append(board.index(loc[0]+file))
                rightPiece.setLegalMoves(legalMoves)
            if (leftPiece and leftPiece.color != piece.color and leftPiece.type == "pawn") :
                legalMoves = leftPiece.getLegalMoves()
                legalMoves.append(board.index(loc[0]+file))
                leftPiece.setLegalMoves(legalMoves)
        
                
        #promotions are not dealt here they have been dealt explicitly
        if piece.type == "pawn" and (loc[1] == "8" or loc[1] == "1"):
            move["type"] = "promotion pending"

        #checks and checkmates
        if self.__isBoardCheck():
            move["type"] = "check"
            move["check"] = True
            notation += "+"
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
                print("checkmated haha")
                if piece.color == "black":
                    self.is_white_checkmated = True
                else: 
                    self.is_black_checkmate = True
        else:
            self.is_white_checked = False
            self.is_black_checked = False
            #set castelling move
            self.addCastling()

        #removing all moves for opposite color
        for newpieces in self.__chessboard:
            if newpieces and newpieces.color != self.play_turn:
                newpieces.setLegalMoves([])

        move["notation"] = notation
        self.moveHistory(move["notation"])

        if not move["type"] == "promotion pending":
            print("===== CHESSBOARD =====")
            for i in range(8):
                for j in range(8):
                    if self.__chessboard[i*8 + j]:
                        print(self.__chessboard[i*8 +j].color[0] + self.__chessboard[i*8 + j].type[0], end=" ")
                    else:
                        print("   ", end="")
                print()
            print(">>>> MOVE: ", move)
        return move


    def moveHistory(self, notation):
        self.moveNo += 1
        if self.play_turn == "black":
            #add white move
            self.__moveHistory += f" {self.moveNo}.{notation}"
        else:
            #add black move
            self.__moveHistory += f" {notation}"

    def getGameHistory(self):
        return self.__moveHistory

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

    def moveHispiecery(self):
        return self.__moveHistory
            
    def getLegalMoves(self):
        return self.__legalMoves

    def setLegalMoves(self, moves):
        self.__legalMoves = moves
