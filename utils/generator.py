import random
from models.process import Process


def generate_processes(n):

    processes = []

    # Unique arrival times
    arrivals = sorted(random.sample(range(0, n * 2 + 2), n))

    for i in range(n):

        burst = random.randint(1, 10)

        processes.append(
            Process(
                f"P{i+1}",
                arrivals[i],
                burst
            )
        )

    return processes