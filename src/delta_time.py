import time

class DeltaTime:
    def __init__(self):
        self.last_time = None
        self.elapsed_time = 0

    def update(self):
        now = time.time()
        if self.last_time != None:
            self.elapsed_time = now - self.last_time
        self.last_time = now

    def elapsed(self):
        return self.elapsed_time
