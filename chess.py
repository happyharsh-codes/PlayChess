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

        if (abs(i) < 10 or abs(j) < 10):
            self.setPosition()
            return

        mod = math.sqrt(i**2 + j**2)
        self.veloctiyX = velocity*(i/mod)
        self.veloctiyY = velocity*(j/mod)
        self.moving = True

    def highLightMoves(self, legalMoves):
        pass
        # overlay = pygame.Surface((SCREEN.get_width(), SCREEN.get_height()), pygame.SRCALPHA)
        # for move in legalMoves:
        #     rank = int(move[1])
        #     file = ord(move[0]) - 97

        #     x = BOARD_RECT.x + SIDE*file + SIDE//2
        #     y = SIDE*(8-rank) + SIDE//2
            
        #     pygame.draw.circle(overlay, (225, 0, 0, 100), (x,y), SIDE//3)
        #     SCREEN.blit(overlay, (0,0))
        #     pygame.display.update()

    def keepMoving(self):
        rank = int(self.position[1])
        file = ord(self.position[0]) - 97

        x = BOARD_RECT.x  + SIDE*file
        y = SIDE*(8-rank)

        self.rect.x += self.veloctiyX
        self.rect.y += self.veloctiyY
        
        if abs(x - self.rect.x) < 10 or abs(y - self.rect.y) < 10:
            self.setPosition()

    def update(self, events: pygame.event, chess, game):

        for event in events:

            if self.grabbed:
                legalMoves = chess.getLegalMoves(chess.getPiece(self.position))
                self.highLightMoves(legalMoves)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if self.moving:
                        return
                    self.grabbed = True
                    print("GRABBED PIECE: ", chess.getPiece(self.position).color + chess.getPiece(self.position).type, self.position, chess.getLegalMoves(chess.getPiece(self.position)))

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
                legalMoves = chess.getLegalMoves(chess.getPiece(self.position))
                #moving
                myMove = f"{file}{rank}"
                if myMove in legalMoves:
                    #process
                    move = chess.move( chess.getPiece(self.position) , f"{file}{rank}")
                    if move["type"] == "illegal":
                        self.moveToPosition(self.position, 20)
                        GAME_SOUNDS["illegal"].play()
                        return
                    
                    if move["type"] == "capture" or "x" in move["notation"]:
                        for sprite in game.chessSprites:
                            if sprite.position == move["final"] and sprite.color != self.color:
                                sprite.kill()

                    if move["type"] == "castle":
                        if move["final"] == "g1":
                            target = "h1"
                            target_dest = "f1"
                        elif move["final"] == "c1":
                            target = "a1"
                            target_dest = "d1"    
                        elif move["final"] == "c8":
                            target = "a8"
                            target_dest = "d8"
                        elif move["final"] == "g8":
                            target = "h8"
                            target_dest = "f8"
                        for sprite in game.chessSprites:
                            if sprite.position == target:
                                sprite.position == target_dest
                                sprite.moveToPosition(target_dest, 15)
                                break

                    if move["type"] == "enpassant":
                        if move["final"][1] == "3":
                            target = move["final"][0] + "4"
                        elif move["final"][1] == "6":
                            target = move["final"][0] + "5"
                        for sprite in game.chessSprites:
                            if sprite.position == target:
                                sprite.kill()
                                break
                    
                    if move["type"] == "checkmate":
                        print("game Over")

                    if move["type"] == "promotion pending":
                        user_promote_to_piece = game.promotionScreen(chess.play_turn)
                        move = chess.promote(move, move["final"], user_promote_to_piece, move["notation"])
                        self.image = GAME_SPRITES[user_promote_to_piece]
                    
                    self.position = move["final"]
                    self.moveToPosition(self.position, 20)
                    GAME_SOUNDS[move["type"]].play()

                else:
                    self.moveToPosition(self.position, 20)
                    return