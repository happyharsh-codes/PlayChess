"""Loads all game sprites and returns them"""
import pygame
from pygame.locals import*

import json
with open("./src/theme.json", "r") as f:
    currentTheme = json.load(f)
    piecesTheme = currentTheme["pieces"]
    soundsTheme = currentTheme["sounds"]


SCREENHEIGHT = 710
SCREENWIDTH = 1310
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)
FPS = 30
FPSCLOCK = pygame.time.Clock()
GAME_SPRITES = {}
GAME_SOUNDS = {}
PIECES = []
    
pygame.init()
BOARD = pygame.transform.scale(pygame.image.load(currentTheme["board"]["chessboard"]).convert_alpha(),(SCREENHEIGHT, SCREENHEIGHT))
LENGTH = BOARD.get_width()
BOARD_RECT = BOARD.get_rect(topleft = ((SCREENWIDTH-LENGTH) // 2, 0))
SIDE = LENGTH/8


def get_SPRITES():
    GAME_SPRITES["black-bishop"] = pygame.transform.scale(pygame.image.load(piecesTheme["black-bishop"]),(SIDE, SIDE)).convert_alpha()
    GAME_SPRITES["black-king"] = pygame.transform.scale(pygame.image.load(piecesTheme["black-king"]),(SIDE, SIDE)).convert_alpha()
    GAME_SPRITES["black-night"] = pygame.transform.scale(pygame.image.load(piecesTheme["black-night"]),(SIDE, SIDE)).convert_alpha()
    GAME_SPRITES["black-queen"] = pygame.transform.scale(pygame.image.load(piecesTheme["black-queen"]),(SIDE, SIDE)).convert_alpha()
    GAME_SPRITES["black-pawn"] = pygame.transform.scale(pygame.image.load(piecesTheme["black-pawn"]),(SIDE, SIDE)).convert_alpha()
    GAME_SPRITES["black-rook"] = pygame.transform.scale(pygame.image.load(piecesTheme["black-rook"]),(SIDE, SIDE)).convert_alpha()
    GAME_SPRITES["white-king"] = pygame.transform.scale(pygame.image.load(piecesTheme["white-king"]),(SIDE, SIDE)).convert_alpha()
    GAME_SPRITES["white-queen"] = pygame.transform.scale(pygame.image.load(piecesTheme["white-queen"]),(SIDE, SIDE)).convert_alpha()
    GAME_SPRITES["white-pawn"] = pygame.transform.scale(pygame.image.load(piecesTheme["white-pawn"]),(SIDE, SIDE)).convert_alpha()
    GAME_SPRITES["white-rook"] = pygame.transform.scale(pygame.image.load(piecesTheme["white-rook"]),(SIDE, SIDE)).convert_alpha()
    GAME_SPRITES["white-night"] = pygame.transform.scale(pygame.image.load(piecesTheme["white-night"]),(SIDE, SIDE)).convert_alpha()
    GAME_SPRITES["white-bishop"] = pygame.transform.scale(pygame.image.load(piecesTheme["white-bishop"]),(SIDE, SIDE)).convert_alpha()
    return GAME_SPRITES

def get_SOUNDS():
    GAME_SOUNDS["capture"] = pygame.mixer.Sound(soundsTheme["capture"])
    GAME_SOUNDS["checkmate"] = pygame.mixer.Sound(soundsTheme["game-end"])
    GAME_SOUNDS["game-end"] = pygame.mixer.Sound(soundsTheme["game-end"])
    GAME_SOUNDS["game-start"] = pygame.mixer.Sound(soundsTheme["game-start"])
    GAME_SOUNDS["check"] = pygame.mixer.Sound(soundsTheme["move-check"])
    GAME_SOUNDS["move"] = pygame.mixer.Sound(soundsTheme["move-self"])
    GAME_SOUNDS["enpassant"] = pygame.mixer.Sound(soundsTheme["capture"])
    GAME_SOUNDS["promotion"] = pygame.mixer.Sound(soundsTheme["promote"])
    GAME_SOUNDS["castle"] = pygame.mixer.Sound(soundsTheme["castle"])
    GAME_SOUNDS["illegal"] = pygame.mixer.Sound(soundsTheme["illegal"])
    return GAME_SOUNDS

GAME_SPRITES = get_SPRITES()
GAME_SOUNDS = get_SOUNDS()
    

print("__INIT__ Was runned")