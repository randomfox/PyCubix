import time

class Fps:
    def __init__(self, update_interval):
        self.last_time = time.time()
        self.frame_count = 0
        self.update_interval = update_interval
        self.fps = 0

    def update(self):
        self.frame_count += 1
        now = time.time()
        delta = now - self.last_time
        if delta >= self.update_interval:
            self.fps = self.frame_count / delta
            print("{:.0f} frames in {:3.1f} seconds = {:6.3f} FPS".format(self.frame_count, delta, self.fps))
            self.last_time = now
            self.frame_count = 0
