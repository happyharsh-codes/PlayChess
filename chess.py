import pygame
from __init__ import*
import math

class ChessSprite(pygame.sprite.Sprite):

    def __init__(self, type, color, position):
        super().__init__()

        self.type = type
        self.color = color
        self.position = position
        self.grabbed = False
        self.moving = False

        self.image = GAME_SPRITES[f"{self.color}-{self.type}"]
        self.rect = self.image.get_rect()

        self.setPosition()

    def move(self, location):
        self.position = location
        self.setPosition()

    def setPosition(self):
        self.moving = False
        self.veloctiyX = 0
        self.veloctiyY = 0

        rank = int(self.position[1])
        file = ord(self.position[0]) - 97

        self.rect.x = BOARD_RECT.x  + SIDE*file
        self.rect.y = SIDE*(8-rank)

    def moveToPosition(self, position, velocity):
        """Moves the piece to destination but slowly to create animation effect"""
        self.position = position
        rank = int(self.position[1])
        file = ord(self.position[0]) - 97

        target_x = BOARD_RECT.x  + SIDE*file
        target_y = SIDE*(8-rank)

        i = target_x - self.rect.x
        j = target_y - self.rect.y

        mod = math.sqrt(i**2 + j**2)
        self.veloctiyX = velocity*(i/mod)
        self.veloctiyY = velocity*(j/mod)
        self.moving = True

    def update(self, events: pygame.event, chess):

        for event in events:
            if self.moving:
                rank = int(self.position[1])
                file = ord(self.position[0]) - 97

                x = BOARD_RECT.x  + SIDE*file
                y = SIDE*(8-rank)

                self.rect.x += self.veloctiyX
                self.rect.y += self.veloctiyY
                
                if abs(x - self.rect.x) < 10 or abs(y - self.rect.y) < 10:
                    self.setPosition()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if self.moving:
                        return
                    self.grabbed = True

            elif event.type == pygame.MOUSEMOTION and self.grabbed:
                self.rect.center = event.pos

            elif event.type == pygame.MOUSEBUTTONUP and self.grabbed:
                self.grabbed = False
                x = (event.pos[0] - BOARD_RECT.x)//SIDE
                if x > 7 or x < 0:
                    #left outside chess board : INVALID
                    self.moveToPosition(self.position, 20)
                    return
                file = chr(97+int(x))
                rank = int(8-(event.pos[1]//SIDE))
                print(self.position)
                legalMoves = chess.getLegalMoves(chess.getPiece(self.position))
                print(legalMoves)
                #moving
                myMove = f"{file}{rank}"
                if myMove in legalMoves:
                    #process
                    move = chess.move( chess.getPiece(self.position) , f"{file}{rank}")
                    if move["type"] == "illegal":
                        self.moveToPosition(self.position, 20)
                        return
                    
                    self.position = move["final"]
                    self.moveToPosition(self.position, 20)

                    GAME_SOUNDS[move["type"]].play()
                else:
                    self.moveToPosition(self.position, 20)
                    return