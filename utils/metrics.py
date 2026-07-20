def compute(processes):

    total_tat = 0
    total_rt = 0

    for p in processes:

        p.turnaround = p.completion - p.arrival

        total_tat += p.turnaround
        total_rt += p.response

    avg_tat = total_tat / len(processes)
    avg_rt = total_rt / len(processes)

    return avg_tat, avg_rt