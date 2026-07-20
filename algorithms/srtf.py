def schedule(processes):

    current_time = 0
    completed = 0
    gantt = []

    n = len(processes)

    while completed < n:

        # Processes that have arrived
        ready = [
            p for p in processes
            if p.arrival <= current_time
            and p.remaining > 0
        ]

        if len(ready) == 0:

            gantt.append("IDLE")
            current_time += 1
            continue

        # Shortest Remaining Time
        ready.sort(key=lambda p: (p.remaining, p.arrival))

        p = ready[0]

        # Response Time
        if not p.started:

            p.started = True
            p.response = current_time - p.arrival

        # Execute for ONE time unit only
        gantt.append(p.pid)

        p.remaining -= 1
        current_time += 1

        # Finished?
        if p.remaining == 0:

            p.completion = current_time
            completed += 1

    return gantt