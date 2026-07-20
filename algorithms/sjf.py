def schedule(processes):

    completed = 0
    current_time = 0
    gantt = []

    n = len(processes)

    while completed < n:

        ready = [
            p for p in processes
            if p.arrival <= current_time
            and p.remaining > 0
        ]

        if len(ready) == 0:
            gantt.append("IDLE")
            current_time += 1
            continue

        # Shortest Burst Time
        ready.sort(key=lambda p: (p.burst, p.arrival))

        p = ready[0]

        if not p.started:
            p.started = True
            p.response = current_time - p.arrival

        while p.remaining > 0:
            gantt.append(p.pid)
            current_time += 1
            p.remaining -= 1

        p.completion = current_time
        completed += 1

    return gantt