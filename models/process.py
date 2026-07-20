class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst

        self.remaining = burst

        self.completion = 0
        self.turnaround = 0
        self.response = -1

        self.started = False

    def reset(self):
        """Reset process so another algorithm can use it."""
        self.remaining = self.burst
        self.completion = 0
        self.turnaround = 0
        self.response = -1
        self.started = False

    def __str__(self):
        return (
            f"{self.pid} "
            f"(AT={self.arrival}, "
            f"BT={self.burst})"
        )