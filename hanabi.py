import math
import os
import random
import string
import time
random.seed(42)

FPS = 5
FRAME_DURATION = 1 / FPS
FADE_SYMBOL = '.'
RISING_SYMBOL = '|'
COLORS = {
    'blue': ['\033[38;5;27m', '\033[38;5;33m', '\033[38;5;39m', '\033[38;5;21m'],
    'green': ['\033[38;5;48m', '\033[38;5;46m', '\033[38;5;118m', '\033[38;5;50m'],
    'yellow': ['\033[38;5;226m', '\033[38;5;220m', '\033[38;5;214m', '\033[38;5;190m'],
    'red': ['\033[38;5;203m', '\033[38;5;208m', '\033[38;5;202m', '\033[38;5;196m'],
}
RESET = '\033[0m'
MIN_SIZE = 6
MAX_SIZE = 11
current_min_size = MIN_SIZE # 後半になるにつれて大きくする

FLAG = 'ASUSN{xxxxxxxxxxxxxxxxxxxxxxxxxxxxx}' # (≧▽≦)
E = 65537

def add_current_size():
    global current_min_size
    current_min_size += 1
    current_min_size = min(current_min_size, MAX_SIZE)

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
    def __init__(self, sky, symbols):
        self.sky = sky
        self.symbols = symbols
        self.x = 0

    def getSymbol(self):
        symbol = self.symbols[self.x * E % len(self.symbols)]
        self.x += 1
        return symbol

    def print_rising(self, current_height):
        self.sky.clear()
        self.sky.canvas[current_height][self.center_x] = RISING_SYMBOL
        self.sky.print_sky()

    def print_burst(self, current_frame, total_frames):
        self.sky.clear()
        is_fade = (current_frame == 0 or current_frame == total_frames - 1)
        max_radius = self.size
        aspect_ratio = 2 # 真円に見えるように横方向にスケーリング

        current_radius = min(max_radius, int(max_radius * ((current_frame + 1) / 3)))

        for radius in range(1, current_radius + 1):
            symbol = self.getSymbol() if not is_fade else FADE_SYMBOL
            s_idx = self.symbols.index(symbol) % len(COLORS) if not is_fade else 0

            for angle_deg in range(0, 360, 15):
                angle_rad = math.radians(angle_deg)
                x = int(self.center_x + aspect_ratio * radius * math.cos(angle_rad) + 0.5)
                y = int(self.center_y + radius * math.sin(angle_rad) + 0.5)
                if 0 <= x < self.sky.width and 0 <= y < self.sky.height:
                    self.sky.canvas[y][x] = '{}{}{}'.format(COLORS[self.color][s_idx], symbol, RESET)

        self.sky.print_sky()
    
    def wait(self, frames):
        self.sky.clear()
        self.sky.print_sky()
        time.sleep(FRAME_DURATION * frames)
    
    def launch(self, rising_frames, wait_frames, ready_frames=None, burst_frames=None, size=None, color=None):
        self.size = size if size is not None else random.randint(current_min_size, current_min_size + 2)
        if self.size % len(self.symbols) == 0:
            self.size -= 1
        self.color = color if color is not None else random.choice(list(COLORS.keys()))
        burst_frames = burst_frames if burst_frames is not None else self.size
        self.center_x = self.sky.width // 2 + random.randint(-10, 10)
        self.center_y = self.sky.height // 2 + random.randint(-5, 0)

        if ready_frames is not None:
            self.wait(ready_frames)

        step_heights = [int(self.sky.height - 1 - i * (self.sky.height // 2 / (rising_frames + 1))) for i in range(rising_frames)]
        for height in step_heights:
            self.sky.clear()
            self.print_rising(height)
            time.sleep(FRAME_DURATION)

        self.wait(wait_frames)
        
        for current_frame in range(burst_frames):
            self.sky.clear()
            self.print_burst(current_frame, burst_frames)
            time.sleep(FRAME_DURATION)

def main():
    sky = Sky(height=36, width=120)
    kiku = Firework(sky, '.o+*')
    botan = Firework(sky, '+☆★◇◆')
    senrin = Firework(sky, string.hexdigits)
    yanagi = Firework(sky, string.printable)
    kamurogiku = Firework(sky, FLAG)
    try:
        while True:
            kiku.launch(ready_frames=5,  rising_frames=8, wait_frames=4)
            kiku.launch(                 rising_frames=0, wait_frames=2)
            kiku.launch(                 rising_frames=0, wait_frames=1)
            kiku.launch(                 rising_frames=0, wait_frames=0)
            kiku.launch(                 rising_frames=0, wait_frames=2)
            kiku.launch(                 rising_frames=0, wait_frames=1)
            kiku.launch(                 rising_frames=0, wait_frames=0)
            add_current_size()
            botan.launch(ready_frames=5, rising_frames=8, wait_frames=4)
            botan.launch(                rising_frames=0, wait_frames=3)
            botan.launch(                rising_frames=0, wait_frames=0)
            botan.launch(                rising_frames=0, wait_frames=3)
            botan.launch(                rising_frames=0, wait_frames=1)
            botan.launch(                rising_frames=0, wait_frames=0)
            botan.launch(                rising_frames=0, wait_frames=2)
            add_current_size()
            senrin.launch(ready_frames=5,rising_frames=8, wait_frames=4)
            kiku.launch(                 rising_frames=0, wait_frames=1)
            senrin.launch(               rising_frames=0, wait_frames=2)
            botan.launch(                rising_frames=0, wait_frames=0)
            senrin.launch(               rising_frames=0, wait_frames=3)
            senrin.launch(               rising_frames=0, wait_frames=0)
            kiku.launch(                 rising_frames=0, wait_frames=1)
            add_current_size()
            yanagi.launch(ready_frames=5,rising_frames=8, wait_frames=4)
            kiku.launch(                 rising_frames=0, wait_frames=1)
            botan.launch(                rising_frames=0, wait_frames=2)
            kiku.launch(                 rising_frames=0, wait_frames=0)
            yanagi.launch(               rising_frames=0, wait_frames=3)
            kiku.launch(                 rising_frames=0, wait_frames=0)
            botan.launch(                rising_frames=0, wait_frames=1)
            add_current_size()
            kamurogiku.launch(ready_frames=5, rising_frames=10, wait_frames=6)
            add_current_size()
            kiku.launch(ready_frames=5,  rising_frames=10, wait_frames=6)
            botan.launch(ready_frames=5, rising_frames=10, wait_frames=6)

    except KeyboardInterrupt:
        sky.clear()
        print('花火大会を中断しました')

if __name__ == '__main__':
    main()
