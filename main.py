from copy import deepcopy

from models.process import Process
from utils.generator import generate_processes
from utils.scheduler import run, run_rr, run_mlfq
from utils.gantt import draw
from utils.metrics import compute
from utils.export import export_results


def manual_input():
    processes = []
    n = int(input("\nNumber of Processes: "))

    for i in range(n):
        print(f"\nProcess P{i+1}")
        arrival = int(input("Arrival Time : "))
        burst = int(input("Burst Time   : "))
        processes.append(Process(f"P{i+1}", arrival, burst))

    return processes


def display(processes, gantt):
    draw(gantt)

    avg_tat, avg_rt = compute(processes)

    print("\n" + "=" * 60)
    print(f"{'PID':<6}{'AT':<6}{'BT':<6}{'CT':<6}{'TAT':<6}{'RT':<6}")
    print("=" * 60)

    for p in processes:
        print(
            f"{p.pid:<6}"
            f"{p.arrival:<6}"
            f"{p.burst:<6}"
            f"{p.completion:<6}"
            f"{p.turnaround:<6}"
            f"{p.response:<6}"
        )

    print("=" * 60)
    print(f"Average Turnaround Time : {avg_tat:.2f}")
    print(f"Average Response Time   : {avg_rt:.2f}")


def get_processes():
    print("\n========== INPUT ==========")
    print("1. Manual Input")
    print("2. Random Generator")

    choice = input("\nChoice: ")

    if choice == "1":
        return manual_input()

    if choice == "2":
        n = int(input("Number of Processes: "))
        processes = generate_processes(n)

        print("\nGenerated Processes")
        for p in processes:
            print(f"{p.pid}  AT={p.arrival}  BT={p.burst}")

        return processes

    return None


def main():

    while True:

        processes = get_processes()

        if not processes:
            print("Invalid Input.")
            continue

        print("\n========== ALGORITHMS ==========")
        print("1. FCFS")
        print("2. SJF")
        print("3. SRTF")
        print("4. Round Robin")
        print("5. MLFQ")

        algo = input("\nSelect Algorithm: ")

        p = deepcopy(processes)

        if algo in ["1", "2", "3"]:

            gantt = run(int(algo), p)

        elif algo == "4":

            quantum = int(input("Time Quantum: "))
            gantt = run_rr(p, quantum)

        elif algo == "5":

            print("\n------ MLFQ Configuration ------")

            q0 = int(input("Q0 Quantum : "))
            q1 = int(input("Q1 Quantum : "))
            q2 = int(input("Q2 Quantum : "))

            a0 = int(input("Q0 Allotment : "))
            a1 = int(input("Q1 Allotment : "))
            a2 = int(input("Q2 Allotment : "))

            gantt = run_mlfq(
                p,
                q0,
                q1,
                q2,
                a0,
                a1,
                a2,
            )

        else:
            print("Invalid Algorithm.")
            continue

        display(p, gantt)

        export = input("\nExport results to CSV? (y/n): ").lower()

        if export == "y":
            avg_tat, avg_rt = compute(p)
            export_results(p, avg_tat, avg_rt)

        again = input("\nDo you want to run another simulation? (y/n): ").lower()

        if again != "y":
            print("\nThank you for using the CPU Scheduling Simulator!")
            break

if __name__ == "__main__":
    main()