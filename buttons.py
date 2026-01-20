import pygame
from pygame.locals import*

class Buttons(pygame.sprite.Sprite):

    def __init__(self, pos, callback, width=200, height=50, label="", color="white", bgcolor = "", image=None):
        super().__init__()
        self.width = width
        self.height = height
        self.radius = min(25,min(width,height)//4)

        self.label_text = label
        self.base_color = pygame.Color(bgcolor)
        self.hover_color = self.base_color.lerp((255, 255, 255), 0.2)
        self.text_color = color
        self.font = pygame.font.SysFont('Monospace', int(self.height * 0.5), bold=True)

        self.image_normal = self._create_button_surface(self.base_color)
        self.image_hover = self._create_button_surface(self.hover_color)
        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=pos)

        self.callback = callback

    def _create_button_surface(self, bg_color):
        shadow_offset = 2
        surf = pygame.Surface((self.width + shadow_offset, self.height + shadow_offset), pygame.SRCALPHA)

        shadow_rect = pygame.Rect(shadow_offset, shadow_offset, self.width, self.height)
        pygame.draw.rect(surf, (0, 0, 0, 70), shadow_rect, border_radius=self.radius)

        button_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(surf, bg_color, button_rect, border_radius=self.radius)

        text_surf = self.font.render(self.label_text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.width//2, self.height//2))
        surf.blit(text_surf, text_rect)

        return surf

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.image_hover
        else:
            self.image = self.image_normal
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    print("Button clicked")
                    self.callback()