# CPU-SCHEDULING-SIMULATOR

A simple CPU Scheduling Simulator built for an Operating Systems course. It implements five classic CPU scheduling algorithms and lets you run them either from the terminal or through a basic Tkinter GUI.

## Features

- Manual process input (arrival time and burst time)
- Random process generator
- Five scheduling algorithms:
  - First Come First Serve (FCFS)
  - Shortest Job First (SJF)
  - Shortest Remaining Time First (SRTF)
  - Round Robin (RR)
  - Multilevel Feedback Queue (MLFQ)
- Gantt chart output (text-based in the terminal, canvas-based in the GUI)
- Process table with Completion Time, Turnaround Time, and Response Time
- Average Turnaround Time and Average Response Time
- Export results to CSV

## Project Structure

```
cpu_scheduler/
├── main.py                 # Terminal version (CLI menu)
├── gui.py                  # Tkinter GUI version
├── models/
│   └── process.py          # Process class
├── algorithms/
│   ├── fcfs.py
│   ├── sjf.py
│   ├── srtf.py
│   ├── round_robin.py
│   └── mlfq.py
├── utils/
│   ├── generator.py        # Random process generator
│   ├── gantt.py             # Text-based Gantt chart (CLI)
│   ├── metrics.py           # Average TAT / RT calculation
│   ├── export.py            # CSV export
│   ├── scheduler.py         # Calls the correct algorithm
│   └── colors.py             # Terminal color codes
└── sample_inputs/
    └── sample.txt
```

## Requirements

- Python 3.8 or higher
- No external libraries needed (Tkinter comes built in with Python)

If Tkinter is not installed on your system:

```
# Ubuntu / Debian
sudo apt-get install python3-tk
```

## How to Run

### Terminal Version

```
cd cpu_scheduler
python main.py
```

Follow the on-screen menu to choose manual/random input and pick an algorithm.

### GUI Version

```
cd cpu_scheduler
python gui.py
```

1. Choose **Manual Input** or **Random Generator** as the input mode.
2. For Manual Input, enter the number of processes and click **Set Number of Processes**, then fill in the Arrival Time and Burst Time for each process.
3. For Random Generator, enter the number of processes and click **Generate**.
4. Select an algorithm (FCFS, SJF, SRTF, Round Robin, or MLFQ).
   - Round Robin requires a **Time Quantum**.
   - MLFQ requires **Q0/Q1/Q2 Quantum** and **Q0/Q1/Q2 Allotment** values.
5. Click **Run Simulation** to see the Gantt chart and process table.
6. Click **Export CSV** to save the results, or **Refresh** to reset everything and start over.

## Notes

- Process IDs are automatically assigned as P1, P2, P3, ...
- In the Gantt chart, `IDLE` means the CPU was not executing any process.
- MLFQ Gantt chart blocks are labeled with the queue they ran in, e.g. `Q0:P1`.

## Authors

Add your name(s) here.
