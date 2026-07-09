from pygame.sprite import Sprite
from src.utils.cameras import overlay_sprites, overlay_layers


class OverlaySprite(Sprite):
    def __init__(self, display_group=overlay_sprites) -> None:
        super().__init__(display_group)
        self.children:list[OverlaySprite] = []
        self.deactivate()

    def set_position(self, x, y) -> None:
        pass

    def activate(self) -> None:
        overlay_sprites.add(self)

    def activate_children(self) -> None:
        for child in self.children:
            child.activate()
    
    def deactivate(self) -> None:
        overlay_sprites.remove(self)
        for child in self.children:
            child.deactivate()