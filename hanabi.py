import time
import random
import os
import math
from math import cos, sin
import string

fps = 5
frame_duration = 1 / fps
random.seed(42)

fade_symbol = '.'
symbols = ['.', '+', '*', 'o']
colors = {
    'blue': ['\033[38;5;27m', '\033[38;5;33m', '\033[38;5;39m', '\033[38;5;21m'],
    'green': ['\033[38;5;48m', '\033[38;5;46m', '\033[38;5;118m', '\033[38;5;50m'],
    'yellow': ['\033[38;5;226m', '\033[38;5;220m', '\033[38;5;214m', '\033[38;5;190m'],
    'red': ['\033[38;5;203m', '\033[38;5;208m', '\033[38;5;202m', '\033[38;5;196m'],
}
reset = '\033[0m'

class Sky:
    def __init__(self, height, width):
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
    def __init__(self, sky, size=None, color=None):
        self.sky = sky
        self.size = size if size is not None else random.randint(8, 13)
        self.color = color if color is not None else random.choice(list(colors.keys()))
        self.center_x = sky.width // 2
        self.center_y = sky.height // 2
        self.symbols = random.sample(string.printable, 4)

    def print_rising(self, current_height):
        self.sky.clear()
        self.sky.canvas[current_height][self.center_x] = '|'
        self.sky.print_sky()

    def print_burst(self, current_frame, total_frames):
        self.symbols = random.sample(string.printable, 4)
        self.sky.clear()
        is_fade = (current_frame == 0 or current_frame == total_frames - 1)
        max_radius = self.size
        aspect_ratio = 2 # 真円に見えるように横方向にスケーリング

        current_radius = min(max_radius, int(max_radius * ((current_frame + 1) / 3)))

        for radius in range(1, current_radius + 1):
            symbol = random.choice(self.symbols) if not is_fade else fade_symbol
            s_idx = self.symbols.index(symbol) if not is_fade else 0

            for angle_deg in range(0, 360, 15):
                angle_rad = math.radians(angle_deg)
                x = int(self.center_x + aspect_ratio * radius * cos(angle_rad) + 0.5)
                y = int(self.center_y + radius * sin(angle_rad) + 0.5)
                if 0 <= x < self.sky.width and 0 <= y < self.sky.height:
                    self.sky.canvas[y][x] = '{}{}{}'.format(colors[self.color][s_idx], symbol, reset)

        self.sky.print_sky()
    
    def wait(self, frames):
        self.sky.clear()
        self.sky.print_sky()
        time.sleep(frame_duration * frames)
    
    def launch(self, rising_frames, wait_frames, burst_frames):
        symbols = random.sample(string.printable, 4)
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
    fw_green = Firework(sky)
    fw_blue = Firework(sky)
    fw_red = Firework(sky)
    fw_yellow = Firework(sky)
    try:
        while True:
            fw_green.launch(rising_frames=9, wait_frames=5, burst_frames=12)
            fw_blue.launch(rising_frames=8, wait_frames=4, burst_frames=11)
            fw_red.launch(rising_frames=8, wait_frames=4, burst_frames=12)
            fw_yellow.launch(rising_frames=8, wait_frames=4, burst_frames=11)

    except KeyboardInterrupt:
        sky.clear()
        print('花火大会は終了しました')

if __name__ == '__main__':
    main()
