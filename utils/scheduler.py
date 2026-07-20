from algorithms.fcfs import schedule as fcfs
from algorithms.sjf import schedule as sjf
from algorithms.srtf import schedule as srtf
from algorithms.round_robin import schedule as rr
from algorithms.mlfq import schedule as mlfq


def run(choice, processes):
    if choice == 1:
        return fcfs(processes)
    if choice == 2:
        return sjf(processes)
    if choice == 3:
        return srtf(processes)


def run_rr(processes, quantum):
    return rr(processes, quantum)


def run_mlfq(processes, q0, q1, q2, a0, a1, a2):
    return mlfq(processes, q0, q1, q2, a0, a1, a2)