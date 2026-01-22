import pygame
from pygame.locals import*
from buttons import Buttons

class Scrollbox(pygame.sprite.Sprite):

    def __init__(self, pos, width, height, bgcolor):
        super().__init__()

        self.width = width
        self.height = height

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)

        self.scroll_y = 0
        self.padding = 10
        self.line_height = 32
        self.font = pygame.font.SysFont("Monospace", 16, bold=True)

        self.buttons = pygame.sprite.Group()
    
        self._redraw_bg(bgcolor)

    def _redraw_bg(self, bgcolor):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image,bgcolor,self.image.get_rect(),border_radius=15)

    def add_move(self, moveNo, turn, notation, callback=None):
        width = (self.width)//4
        y = self.padding * moveNo + self.line_height * (moveNo-1)
        if turn == "white":
            text_surf = self.font.render(str(moveNo), True, (255,255,255,255))
            text_rect = text_surf.get_rect(topleft=(3, y + self.line_height//4))
            x = self.padding + 20
            self.image.blit(text_surf, text_rect)
            pygame.display.update()
        else:
            x = 20 + 2*self.padding + width
        
        btn = Buttons((self.rect.x + x, self.rect.y + y), callback, width=width, height=self.line_height, label=notation, bgcolor=(60, 60, 60, 230))

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