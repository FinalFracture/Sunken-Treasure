import sys
import pygame
from dataclasses import dataclass
from typing import Any


@dataclass
class Trigger:
    type: str
    payload:Any = None


class EventHandler:
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.view_context = [] #list of display objects thay may react to input
        self.trigger_queue:list[Trigger] = []

    def run(self) -> None:
        """Event handler is the sole checker for mouse and keyboard inputs. Should only have one instance per game instance."""
        self.dt = self.clock.tick() / 1000
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        for event in events:
            #check for events to exit the game.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
                
        for obj in self.view_context:
            if hasattr(obj, "input"):
                obj.input(keys=keys, mouse_pos=mouse_pos, buttons=mouse_buttons, events=events, dt=self.dt)

    def set_context(self, view_context:list) -> None:
        self.view_context = view_context

    def emit(self, trigger:Trigger) -> None:
        self.trigger_queue.append(trigger)
    
    def get_triggers(self) -> list[Trigger]:
        return self.trigger_queue
    
    def clear_triggers(self) -> None:
        self.trigger_queue.clear()


EVENT_HANDLER = EventHandler()
