import sys
import time
from typing import Callable

import pygame

class PeriodicTimer:
    @staticmethod
    def from_frequency(frequency: float, callback: Callable, start=True):
        return PeriodicTimer(1./frequency, callback, start)

    def __init__(self, period: float, callback: Callable, start=True):
        self.callback = callback
        self.period = period
        self.running = start
        self._last_time = 0
        if start:
            self.start()

    def start(self):
        self.running = True
        self._last_time = time.perf_counter()

    def check(self, current_time=None):
        if not self.running:
            return
        if current_time is None:
            current_time = time.perf_counter()
        if current_time - self._last_time > self.period:
            self.callback()
            self._last_time += self.period

class Oscillator:
    def __init__(self, frequency: float, on_callback: Callable, off_callback: Callable):
        self.timer = PeriodicTimer.from_frequency(frequency, self._flip)
        self.on = True
        self._on_callback = on_callback
        self._off_callback = off_callback

    def restart(self):
        self.timer.start()

    def check(self, current_time=None):
        self.timer.check(current_time)

    def _flip(self):
        if self.on:
            self._on_callback()
        else:
            self._off_callback()
        self.on = not self.on

def main():
    pygame.init()
    display = pygame.display.set_mode((400, 400))
    black = pygame.surface.Surface(size=(50,50))
    white = pygame.surface.Surface(size=(50, 50))
    black.fill((0, 0, 0))
    white.fill((255, 255, 255))
    blinker = Oscillator(2, lambda: display.blit(black, (0, 0)), lambda: display.blit(white, (0, 0)))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        blinker.check()
        pygame.display.update()

if __name__ == '__main__':
    main()