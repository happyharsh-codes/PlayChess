import pygame
from pygame.locals import*

import os, sys
from __init__ import*
from chess import ChessSprite
from buttons import Buttons
from scrollbox import Scrollbox
from chessboard import Chessboard
from chessbot import Bot

#====== Initializing ======#
def init():
    pygame.init()
    pygame.display.set_caption("PlayChess.Org")


#====== Game Functions ======#

class Game:
    
    def __init__(self):
        self.chess = Chessboard()
        self.chessSprites = []

    def welcomeScreen(self):
        pass

    def __initializePieces__(self):
        self.chessSprites = [ChessSprite("rook","black","a8"), ChessSprite("night","black","b8"), ChessSprite("bishop","black","c8"),ChessSprite("queen","black","d8"), ChessSprite("king","black","e8"), ChessSprite("bishop","black","f8"), ChessSprite("night","black","g8"), ChessSprite("rook","black","h8")]
        self.chessSprites.extend([ChessSprite("pawn","black",f"{chr(96+i)}7") for i in range(1, 9) ])
        self.chessSprites.extend([ChessSprite("pawn","white",f"{chr(96+i)}2") for i in range(1, 9) ])
        self.chessSprites.extend([ChessSprite("rook","white","a1"), ChessSprite("night","white","b1"), ChessSprite("bishop","white","c1"),ChessSprite("queen","white","d1"), ChessSprite("king","white","e1"), ChessSprite("bishop","white","f1"), ChessSprite("night","white","g1"), ChessSprite("rook","white","h1")])

    def __initializeChessGame__(self):
        self.__initializePieces__()

    def updatePieces(self):
        for sprite in self.chessSprites:
            if sprite.moving:
                sprite.keepMoving()

    def promotionScreen(self, turn):
        overlay = pygame.Surface((LENGTH, LENGTH), pygame.SRCALPHA)
        overlay.fill((200, 200, 200, 180))

        if turn == "white": piecesPlate = ["black-queen", "black-rook", "black-night", "black-bishop"] 
        else: piecesPlate = ["white-queen", "white-rook", "white-night", "white-bishop"]
        SCREEN.blit(overlay, (BOARD_RECT.x, 0))
        rects = []
        for i, piece in enumerate(piecesPlate):
            pieceRect = pygame.Rect(BOARD_RECT.x + (2*SIDE) + i*(SIDE+10), 3.5 * SIDE, SIDE, SIDE)
            rects.append(pieceRect)
            SCREEN.blit(GAME_SPRITES[piece], pieceRect)
        
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    for r in rects:
                        if r.collidepoint(event.pos):
                            return piecesPlate[rects.index(r)]
            pygame.display.update()


    def mainGame(self):
        self.__initializeChessGame__()

        #pieces
        pieces = pygame.sprite.Group()
        for piece in self.chessSprites:
            pieces.add(piece)

        #buttons
        buttons = pygame.sprite.Group()
        def new_game():
            print("new game called")
            self.__initializeChessGame__()
            self.chess = Chessboard()
            pieces.empty()
            for piece in self.chessSprites:
                pieces.add(piece)    
        buttons.add(Buttons((BOARD_RECT.topright[0] + 50, 800), new_game, width=300, height=80, label="New Game", color=(255, 255, 255, 255), bgcolor=(129, 186, 76, 225)))

        #scrollbox
        scrollbox_group = pygame.sprite.Group()
        scrollbox = Scrollbox((BOARD_RECT.topright[0] + 50, 200), 300, 400, (31, 31, 31, 200))
        scrollbox_group.add(scrollbox)


        background = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
        background.fill((23, 23, 23, 180))

        while True: 
            FPSCLOCK.tick(FPS)
            events = pygame.event.get()
            moveHistory = self.chess.getGameHistory().split()

            
            for event in events:
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            pieces.update(events, self.chess, self)
            buttons.update(events)
            scrollbox_group.update(events)
            self.updatePieces()
            SCREEN.blit(background, (0,0))
            SCREEN.blit(BOARD, BOARD_RECT)
            pieces.draw(SCREEN)
            buttons.draw(SCREEN)
            scrollbox.draw(SCREEN)
            pygame.display.update()

def runGame():
    init()
    game = Game()
    game.welcomeScreen()
    game.mainGame()

if __name__ == "__main__":
    runGame()