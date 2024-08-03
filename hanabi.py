import time
import random
import os
import sys
from const import *
from math import cos, sin

class Sky:
    def __init__(self, height=20, width=40):
        self.height = height
        self.width = width
        self.canvas = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.canvas = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def print_sky(self):
        for line in self.canvas:
            print('\033[91m' + ''.join(line) + '\033[0m', file=sys.stderr)

class Firework:
    def __init__(self, sky, size=10):
        self.sky = sky
        self.size = size
        self.center_x = sky.width // 2
        self.center_y = sky.height // 2

    def print_rising(self, current_height):
        self.sky.clear()
        self.sky.canvas[current_height][self.center_x] = '|'
        self.sky.print_sky()

    def print_burst(self):
        self.sky.clear()
        for _ in range(random.randint(5, 15)):
            length = random.randint(2, self.size)
            angle = random.random() * 360
            rad = angle * (3.14159 / 180)
            
            for i in range(1, length):
                x = int(self.center_x + i * cos(rad))
                y = int(self.center_y + i * sin(rad))
                if 0 <= x < self.sky.width and 0 <= y < self.sky.height:
                    self.sky.canvas[y][x] = '*'
        self.sky.print_sky()
    
    def wait(self, frames):
        self.sky.clear()
        self.sky.print_sky()
        time.sleep(frame_duration * frames)
    
    def launch(self, rising_frames, wait_frames, burst_frames):
        step_heights = [int(self.sky.height - 1 - i * (self.sky.height // 2 / rising_frames)) for i in range(rising_frames)]

        for height in step_heights:
            self.sky.clear()
            self.print_rising(height)
            time.sleep(frame_duration)

        self.wait(wait_frames)
        
        for _ in range(burst_frames):
            self.sky.clear()
            self.print_burst()
            time.sleep(frame_duration)

def main():
    sky = Sky(height=20, width=40)
    firework = Firework(sky=sky, size=10)
    try:
        firework.wait(2)
        firework.launch(rising_frames=5, wait_frames=3, burst_frames=6)
        firework.wait(2)
        firework.launch(rising_frames=10, wait_frames=5, burst_frames=6)
    except KeyboardInterrupt:
        sky.clear()
        print("\033[91m花火大会は終了しました\033[0m", file=sys.stderr)

if __name__ == '__main__':
    main()
