import pygame
from src.event_managing import EVENT_HANDLER

class Timer:
    _instances = []

    @staticmethod
    def update_all():
        for timer in Timer._instances:
            timer.update()

    @staticmethod
    def pause_all():
        for timer in Timer._instances:
            timer.pause()

    @staticmethod
    def resume_all():
        for timer in Timer._instances:
            timer.resume()

    def __init__(self, duration, starting_func = None, running_func = None, ending_func = None):
        Timer._instances.append(self)
        self.duration = duration
        self.duration_time = duration
        self.consumed_time = 0
        self.starting_func = starting_func # run this 1 time when the timer starts
        self.running_func = running_func #run this every frame that the timer is active
        self.ending_func = ending_func #run this 1 time when the timer finishes
        self.start_time = 0
        self.active = False
        self.paused = False 
        self.animation_buffer = 0 # buffer to prevent running func to run every frame if deisred
        self.animation_ticks = 0 # counter that resets after buffer is exceeded
        self.clock = pygame.time.Clock() #for creating a framerate independant animation setup. 

    def set_animation_buffer(self, buffer:int) -> None:
        """Set to 0 to run every frame"""
        self.animation_buffer = buffer

    def pause(self):
        self.paused = True
        self.pause_time = pygame.time.get_ticks()
        self.consumed_time = self.pause_time - self.start_time

    def resume(self):
        self.paused = False
        self.start_time = pygame.time.get_ticks()
        self.duration = self.duration - self.consumed_time
        
    def activate(self):
        self.active = True
        self.duration = self.duration_time
        if self.starting_func:
            self.starting_func()
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        if self.ending_func:
            self.ending_func()
        self.active = False
        self.start_time = 0

    def update(self):
        if self.paused:
            return
        
        current_time = pygame.time.get_ticks()
        if self.active:
            self.animation_ticks += EVENT_HANDLER.dt
            if self.running_func and self.animation_ticks > self.animation_buffer:
                self.running_func(EVENT_HANDLER.dt)
                self.animation_ticks = 0
            if current_time - self.start_time > self.duration:
                self.deactivate()
