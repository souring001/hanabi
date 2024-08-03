import time
import random
import os
from math import cos, sin

fps = 5
frame_duration = 1 / fps

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
            print(''.join(line))

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

    def print_burst(self, current_frame, total_frames):
        self.sky.clear()
        is_fade = (current_frame == 0 or current_frame == total_frames - 1)
        symbols = ['.', 'o', '+', '*'] if not is_fade else ['.']
        max_radius = self.size
        aspect_ratio = 2 # 真円に見えるように横方向にスケーリング

        current_radius = min(max_radius, int(max_radius * ((current_frame + 1) / 3)))

        for radius in range(1, current_radius + 1):
            symbol = random.choice(symbols)
            for angle_deg in range(0, 360, 15):
                angle_rad = angle_deg * (3.14159 / 180)
                x = int(self.center_x + aspect_ratio * radius * cos(angle_rad) + 0.5)
                y = int(self.center_y + radius * sin(angle_rad) + 0.5)
                if 0 <= x < self.sky.width and 0 <= y < self.sky.height:
                    self.sky.canvas[y][x] = symbol

        self.sky.print_sky()
    
    def wait(self, frames):
        self.sky.clear()
        self.sky.print_sky()
        time.sleep(frame_duration * frames)
    
    def launch(self, rising_frames, wait_frames, burst_frames):
        step_heights = [int(self.sky.height - 1 - i * (self.sky.height // 2 / (rising_frames + 1))) for i in range(rising_frames)]
        for height in step_heights:
            self.sky.clear()
            self.print_rising(height)
            time.sleep(frame_duration)

        self.wait(wait_frames)
        
        for current_frame in range(burst_frames):
            self.sky.clear()
            
            self.print_burst(current_frame, burst_frames)
            time.sleep(frame_duration)

def main():
    sky = Sky(height=30, width=60)
    firework = Firework(sky=sky, size=8)
    try:
        firework.wait(2)
        firework.launch(rising_frames=9, wait_frames=5, burst_frames=9)
        firework.wait(2)
        firework.launch(rising_frames=8, wait_frames=4, burst_frames=8)
        firework.wait(2)
    except KeyboardInterrupt:
        sky.clear()
        print('花火大会は終了しました')

if __name__ == '__main__':
    main()
