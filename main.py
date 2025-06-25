import pygame
from pygame.locals import*

import os, sys
from __init__ import*
from chess import ChessSprite
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
        self.chessSprite = [ChessSprite("rook","black","a8"), ChessSprite("knight","black","b8"), ChessSprite("bishop","black","c8"),ChessSprite("queen","black","d8"), ChessSprite("king","black","e8"), ChessSprite("bishop","black","f8"), ChessSprite("knight","black","g8"), ChessSprite("rook","black","h8")]
        self.chessSprite.extend([ChessSprite("pawn","black",f"{chr(96+i)}7") for i in range(1, 9) ])
        self.chessSprite.extend([ChessSprite("pawn","white",f"{chr(96+i)}2") for i in range(1, 9) ])
        self.chessSprite.extend([ChessSprite("rook","white","a1"), ChessSprite("knight","white","b1"), ChessSprite("bishop","white","c1"),ChessSprite("queen","white","d1"), ChessSprite("king","white","e1"), ChessSprite("bishop","white","f1"), ChessSprite("knight","white","g1"), ChessSprite("rook","white","h1")])

    def __initializeChessGame__(self):
        self.__initializePieces__()

    def mainGame(self):
        self.__initializeChessGame__()
        group = pygame.sprite.Group()
        for piece in self.chessSprite:
            group.add(piece)
        while True: 
            FPSCLOCK.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            group.update(events, self.chess)
            SCREEN.blit(BOARD, BOARD_RECT)
            group.draw(SCREEN)
            pygame.display.update()

def runGame():
    init()
    game = Game()
    game.welcomeScreen()
    game.mainGame()

if __name__ == "__main__":
    runGame()