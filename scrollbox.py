import pygame
from pygame.locals import*
from buttons import Buttons

class Scrollbox(pygame.sprite.Sprite):

    def __init__(self, pos, width, height, bgcolor):
        super().__init__()

        self.width = width,
        self.height = height

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)

        self.scroll_y = 0
        self.padding = 10
        self.line_height = 32

        self.buttons = pygame.sprite.Group()

        self._redraw_bg()

    def _redraw_bg(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image,self.bgcolor,self.image.get_rect(),border_radius=15)

    def add_move(self, moveNo, turn, notation, callback=None):
        y = self.padding + self.line_height*moveNo + self.height*moveNo
        x = 10 if turn == "white" else 80
        
        btn = Buttons((x,y), callback, width=self.width-self.padding*2, height=26, label=notation, bgcolor=(60, 60, 60, 230))

        self.buttons.add(btn)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        previous_clip = surface.get_clip()
        surface.set_clip(self.rect)

        self.buttons.draw(surface)

        surface.set_clip(previous_clip)

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == MOUSEWHEEL and self.rect.collidepoint(mouse_pos):
                self.scroll_y += event.y * 20
            
        max_scroll = max(0,len(self.buttons) * self.line_height - self.height + self.padding)
        self.scroll_y = max(-max_scroll, min(0, self.scroll_y))
        for i, btn in enumerate(self.buttons):
            #btn.rect.x = self.rect.x + self.padding
            btn.rect.y = (self.rect.y+ self.padding+ i * self.line_height+ self.scroll_y)

            btn.update(events)