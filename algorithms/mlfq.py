from collections import deque


def schedule(
    processes,
    q0_quantum,
    q1_quantum,
    q2_quantum,
    q0_allotment,
    q1_allotment,
    q2_allotment,
):

    processes.sort(key=lambda p: p.arrival)

    for p in processes:
        p.remaining = p.burst
        p.started = False
        p.response = -1
        p.completion = 0

        p.allotment_used = 0

    q0 = deque()
    q1 = deque()
    q2 = deque()
    q3 = deque()

    gantt = []

    time = 0
    completed = 0
    index = 0

    while completed < len(processes):

        while index < len(processes) and processes[index].arrival <= time:
            processes[index].allotment_used = 0
            q0.append(processes[index])
            index += 1


        if q0:

            p = q0.popleft()

            if not p.started:
                p.started = True
                p.response = time - p.arrival

            run = min(q0_quantum, p.remaining)

            executed = 0

            while executed < run:

                gantt.append(f"Q0:{p.pid}")

                time += 1
                executed += 1
                p.remaining -= 1

                while (
                    index < len(processes)
                    and processes[index].arrival <= time
                ):
                    processes[index].allotment_used = 0
                    q0.append(processes[index])
                    index += 1

            if p.remaining == 0:
                p.completion = time
                completed += 1
            else:
                p.allotment_used += 1

                if p.allotment_used >= q0_allotment:
                    p.allotment_used = 0
                    q1.append(p)
                else:
                    q0.append(p)

            continue


        if q1:

            p = q1.popleft()

            if not p.started:
                p.started = True
                p.response = time - p.arrival

            run = min(q1_quantum, p.remaining)

            executed = 0
            preempt = False

            while executed < run:

                gantt.append(f"Q1:{p.pid}")

                time += 1
                executed += 1
                p.remaining -= 1

                while (
                    index < len(processes)
                    and processes[index].arrival <= time
                ):
                    processes[index].allotment_used = 0
                    q0.append(processes[index])
                    index += 1

                if q0:
                    preempt = True
                    break

            if p.remaining == 0:
                p.completion = time
                completed += 1
            else:

                if preempt:
                    q1.appendleft(p)
                else:
                    p.allotment_used += 1

                    if p.allotment_used >= q1_allotment:
                        p.allotment_used = 0
                        q2.append(p)
                    else:
                        q1.append(p)

            continue


        if q2:

            p = q2.popleft()

            if not p.started:
                p.started = True
                p.response = time - p.arrival

            run = min(q2_quantum, p.remaining)

            executed = 0
            preempt = False

            while executed < run:

                gantt.append(f"Q2:{p.pid}")

                time += 1
                executed += 1
                p.remaining -= 1

                while (
                    index < len(processes)
                    and processes[index].arrival <= time
                ):
                    processes[index].allotment_used = 0
                    q0.append(processes[index])
                    index += 1

                if q0:
                    preempt = True
                    break

            if p.remaining == 0:
                p.completion = time
                completed += 1
            else:

                if preempt:
                    q2.appendleft(p)
                else:
                    p.allotment_used += 1

                    if p.allotment_used >= q2_allotment:
                        p.allotment_used = 0
                        q3.append(p)
                    else:
                        q2.append(p)

            continue


        if q3:

            p = q3.popleft()

            if not p.started:
                p.started = True
                p.response = time - p.arrival

            preempt = False

            while p.remaining > 0:

                gantt.append(f"Q3:{p.pid}")

                time += 1
                p.remaining -= 1

                while (
                    index < len(processes)
                    and processes[index].arrival <= time
                ):
                    processes[index].allotment_used = 0
                    q0.append(processes[index])
                    index += 1

                if q0:
                    preempt = True
                    break

            if p.remaining == 0:
                p.completion = time
                completed += 1
            else:

                if preempt:
                    q3.appendleft(p)
                else:
                    q3.append(p)

            continue


        gantt.append("IDLE")
        time += 1

    return gantt