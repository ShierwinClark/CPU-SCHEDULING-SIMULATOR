from collections import deque


def schedule(processes, quantum):

    processes.sort(key=lambda p: (p.arrival, p.pid))

    queue = deque()

    gantt = []

    current_time = 0
    completed = 0
    index = 0

    while completed < len(processes):

        while (
            index < len(processes)
            and processes[index].arrival <= current_time
        ):

            queue.append(processes[index])
            index += 1

        if len(queue) == 0:

            gantt.append("IDLE")
            current_time += 1
            continue

        p = queue.popleft()

        if not p.started:

            p.started = True
            p.response = current_time - p.arrival

        run_time = min(quantum, p.remaining)

        for _ in range(run_time):

            gantt.append(p.pid)

            p.remaining -= 1
            current_time += 1

            while (
                index < len(processes)
                and processes[index].arrival <= current_time
            ):

                queue.append(processes[index])
                index += 1

            if p.remaining == 0:
                break

        if p.remaining == 0:

            p.completion = current_time
            completed += 1

        else:

            queue.append(p)

    return gantt