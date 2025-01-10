import time

class Timer:
    def __init__(self):
        self.start_time = time.perf_counter_ns()

    def elapsed(self, radix=5):
        return round((time.perf_counter_ns() - self.start_time)/1000000000,int(radix))
