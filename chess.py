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

    def keepMoving(self):
        rank = int(self.position[1])
        file = ord(self.position[0]) - 97

        x = BOARD_RECT.x  + SIDE*file
        y = SIDE*(8-rank)

        self.rect.x += self.veloctiyX
        self.rect.y += self.veloctiyY
        
        if abs(x - self.rect.x) < 10 or abs(y - self.rect.y) < 10:
            self.setPosition()

    def draw_highlights(self, chess, surface):
        for square in chess.getLegalMoves(chess.getPiece(self.position)):
            ring_surf = pygame.Surface((SIDE, SIDE), pygame.SRCALPHA)
            file = ord(square[0]) - 97
            rank = 8 - int(square[1])

            x = BOARD_RECT.x + file * SIDE
            y = BOARD_RECT.y + rank * SIDE

            piece = chess.getPiece(square)
            if piece:
                pygame.draw.circle(ring_surf, (48, 46, 43, 100),(SIDE // 2, SIDE // 2),SIDE // 2,width=6)
            else:
                pygame.draw.circle(ring_surf, (48, 46, 43, 100), (SIDE // 2, SIDE // 2), SIDE //6)
            surface.blit(ring_surf, (x, y))


    def update(self, events: pygame.event, chess, game):

        for event in events:

            if self.grabbed:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if self.moving:
                        return
                    self.grabbed = True
                    legalMoves = chess.getLegalMoves(chess.getPiece(self.position))
                    print("GRABBED PIECE: ", chess.getPiece(self.position).color + chess.getPiece(self.position).type, self.position,legalMoves)

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
                    move = chess.move(chess.getPiece(self.position) , f"{file}{rank}")
                    if "illegal" in move["type"]:
                        self.moveToPosition(self.position, 20)
                        GAME_SOUNDS["illegal"].play()
                        return
                    
                    if "capture" in move["type"] or "x" in move["notation"]:
                        for sprite in game.chessSprites:
                            if sprite.position == move["final"] and sprite.color != self.color:
                                sprite.kill()

                    if "castle" in move["type"]:
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

                    if "enpassant" in move["type"]:
                        if move["final"][1] == "3":
                            target = move["final"][0] + "4"
                        elif move["final"][1] == "6":
                            target = move["final"][0] + "5"
                        for sprite in game.chessSprites:
                            if sprite.position == target:
                                sprite.kill()
                                break
                    
                    if "checkmate" in move["type"]:
                        print("game Over")

                    if "promotion pending" in move["type"]:
                        user_promote_to_piece = game.promotionScreen(chess.play_turn)
                        move = chess.promote(move, move["final"], user_promote_to_piece, move["notation"])
                        self.image = GAME_SPRITES[user_promote_to_piece]
                    
                    self.position = move["final"]
                    self.moveToPosition(self.position, 20)
                    for sound in GAME_SOUNDS:
                        if sound in move['type']:
                            GAME_SOUNDS[sound].play()
                    if "checkmate" in move["type"]:
                        GAME_SOUNDS["game-end"].play()

                    #add button
                    game.add_move(chess.moveNo, chess.play_turn, move['notation'])

                else:
                    self.moveToPosition(self.position, 20)
                    return