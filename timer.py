import pygame

class Timer:
    def __init__(self, duration, starting_func = None, running_func = None, ending_func = None):
        self.duration = duration
        self.starting_func = starting_func # run this 1 time when the timer starts
        self.running_func = running_func #run this every frame that the timer is active
        self.ending_func = ending_func #run this 1 time when the timer finishes
        self.start_time = 0
        self.active = False
        self.paused = False 
        self.clock = pygame.time.Clock() #for creating a framerate independant animation setup. 



    def activate(self):
        self.active = True
        if self.starting_func:
            self.starting_func()
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        if self.ending_func:
            self.ending_func()
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        dt = self.clock.tick() / 1000 #miltipler for animation speeds.

        if self.active and not self.paused:
            if self.running_func:
                    self.running_func(dt)
            if current_time - self.start_time > self.duration:
                self.deactivate()