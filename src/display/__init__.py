from pygame.sprite import Sprite
from src.utils.cameras import overlay_sprites, overlay_layers


class OverlaySprite(Sprite):
    def __init__(self) -> None:
        super().__init__(overlay_sprites)
        self.children:list[OverlaySprite] = []
        self.deactivate()

    def activate(self) -> None:
        overlay_sprites.add(self)
        for child in self.children:
            child.activate()
    
    def deactivate(self) -> None:
        overlay_sprites.remove(self)
        for child in self.children:
            child.deactivate()