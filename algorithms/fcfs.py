def schedule(processes):

    processes.sort(key=lambda p: (p.arrival, p.pid))

    gantt = []
    current_time = 0

    for p in processes:

        # CPU idle until process arrives
        while current_time < p.arrival:
            gantt.append("IDLE")
            current_time += 1

        # Response Time
        if not p.started:
            p.started = True
            p.response = current_time - p.arrival

        # Execute completely
        for _ in range(p.burst):
            gantt.append(p.pid)
            current_time += 1

        p.remaining = 0
        p.completion = current_time

    return gantt