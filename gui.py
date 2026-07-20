import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from copy import deepcopy

from models.process import Process
from utils.generator import generate_processes
from utils.scheduler import run, run_rr, run_mlfq
from utils.metrics import compute
from utils.export import export_results


root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("1000x800")

random_processes = []
manual_rows = []

result_processes = []
result_avg_tat = 0
result_avg_rt = 0

mode_var = tk.StringVar(value="manual")
algo_var = tk.StringVar(value="fcfs")

block_colors = ["#ffb3ba", "#bae1ff", "#baffc9", "#ffffba",
                "#ffdfba", "#e0baff", "#c9c9ff", "#baffe4"]
color_map = {}


def get_color(name):
    if name == "IDLE":
        return "#d3d3d3"
    if name not in color_map:
        color_map[name] = block_colors[len(color_map) % len(block_colors)]
    return color_map[name]


main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

title_label = tk.Label(main_frame, text="CPU Scheduling Simulator", font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, pady=10)


# ---------------------------------------------------------------
# Input Mode Selection
# ---------------------------------------------------------------

mode_frame = tk.LabelFrame(main_frame, text="Input Mode")
mode_frame.grid(row=1, column=0, sticky="we", pady=5)


def toggle_mode():
    if mode_var.get() == "manual":
        manual_frame.grid()
        random_frame.grid_remove()
    else:
        random_frame.grid()
        manual_frame.grid_remove()


tk.Radiobutton(mode_frame, text="Manual Input", variable=mode_var, value="manual",
               command=toggle_mode).pack(side="left", padx=10, pady=5)
tk.Radiobutton(mode_frame, text="Random Generator", variable=mode_var, value="random",
               command=toggle_mode).pack(side="left", padx=10, pady=5)


# ---------------------------------------------------------------
# Manual Input
# ---------------------------------------------------------------

manual_frame = tk.LabelFrame(main_frame, text="Manual Input")
manual_frame.grid(row=2, column=0, sticky="we", pady=5)

tk.Label(manual_frame, text="Number of Processes:").grid(row=0, column=0, padx=5, pady=5)
manual_num_entry = tk.Entry(manual_frame, width=6)
manual_num_entry.grid(row=0, column=1, padx=5, pady=5)

manual_rows_frame = tk.Frame(manual_frame)
manual_rows_frame.grid(row=1, column=0, columnspan=3, pady=5)


def make_manual_rows():
    for widget in manual_rows_frame.winfo_children():
        widget.destroy()
    manual_rows.clear()

    try:
        n = int(manual_num_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number of processes")
        return

    tk.Label(manual_rows_frame, text="PID").grid(row=0, column=0, padx=8)
    tk.Label(manual_rows_frame, text="Arrival Time").grid(row=0, column=1, padx=8)
    tk.Label(manual_rows_frame, text="Burst Time").grid(row=0, column=2, padx=8)

    for i in range(n):
        tk.Label(manual_rows_frame, text=f"P{i + 1}").grid(row=i + 1, column=0)
        at_entry = tk.Entry(manual_rows_frame, width=8)
        at_entry.grid(row=i + 1, column=1, padx=5, pady=2)
        bt_entry = tk.Entry(manual_rows_frame, width=8)
        bt_entry.grid(row=i + 1, column=2, padx=5, pady=2)
        manual_rows.append((at_entry, bt_entry))


tk.Button(manual_frame, text="Set Number of Processes",
          command=make_manual_rows).grid(row=0, column=2, padx=5, pady=5)


def get_manual_processes():
    procs = []
    for i, (at_entry, bt_entry) in enumerate(manual_rows):
        at = int(at_entry.get())
        bt = int(bt_entry.get())
        procs.append(Process(f"P{i + 1}", at, bt))
    return procs


# ---------------------------------------------------------------
# Random Generator
# ---------------------------------------------------------------

random_frame = tk.LabelFrame(main_frame, text="Random Process Generator")
random_frame.grid(row=2, column=0, sticky="we", pady=5)

tk.Label(random_frame, text="Number of Processes:").grid(row=0, column=0, padx=5, pady=5)
random_num_entry = tk.Entry(random_frame, width=6)
random_num_entry.grid(row=0, column=1, padx=5, pady=5)

random_output_label = tk.Label(random_frame, text="", justify="left", anchor="w")
random_output_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=5, pady=5)


def generate_random():
    global random_processes
    try:
        n = int(random_num_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number of processes")
        return

    random_processes = generate_processes(n)

    text = ""
    for p in random_processes:
        text += f"{p.pid}   AT={p.arrival}   BT={p.burst}\n"

    random_output_label.config(text=text)


tk.Button(random_frame, text="Generate", command=generate_random).grid(row=0, column=2, padx=5, pady=5)

random_frame.grid_remove()


# ---------------------------------------------------------------
# Algorithm Selection
# ---------------------------------------------------------------

algo_frame = tk.LabelFrame(main_frame, text="Algorithm")
algo_frame.grid(row=3, column=0, sticky="we", pady=5)


def on_algo_change():
    algo = algo_var.get()

    if algo == "rr":
        quantum_frame.grid()
    else:
        quantum_frame.grid_remove()

    if algo == "mlfq":
        mlfq_frame.grid()
    else:
        mlfq_frame.grid_remove()


algo_names = [
    ("FCFS", "fcfs"),
    ("SJF", "sjf"),
    ("SRTF", "srtf"),
    ("Round Robin", "rr"),
    ("MLFQ", "mlfq"),
]

for i, (text, value) in enumerate(algo_names):
    tk.Radiobutton(algo_frame, text=text, variable=algo_var, value=value,
                   command=on_algo_change).grid(row=0, column=i, padx=10, pady=5)


# Round Robin options

quantum_frame = tk.LabelFrame(main_frame, text="Round Robin Options")
quantum_frame.grid(row=4, column=0, sticky="we", pady=5)

tk.Label(quantum_frame, text="Time Quantum:").grid(row=0, column=0, padx=5, pady=5)
quantum_entry = tk.Entry(quantum_frame, width=6)
quantum_entry.grid(row=0, column=1, padx=5, pady=5)

quantum_frame.grid_remove()


# MLFQ options

mlfq_frame = tk.LabelFrame(main_frame, text="MLFQ Options")
mlfq_frame.grid(row=4, column=0, sticky="we", pady=5)

tk.Label(mlfq_frame, text="Q0 Quantum:").grid(row=0, column=0, padx=5, pady=5)
q0_quantum_entry = tk.Entry(mlfq_frame, width=6)
q0_quantum_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(mlfq_frame, text="Q1 Quantum:").grid(row=0, column=2, padx=5, pady=5)
q1_quantum_entry = tk.Entry(mlfq_frame, width=6)
q1_quantum_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(mlfq_frame, text="Q2 Quantum:").grid(row=0, column=4, padx=5, pady=5)
q2_quantum_entry = tk.Entry(mlfq_frame, width=6)
q2_quantum_entry.grid(row=0, column=5, padx=5, pady=5)

tk.Label(mlfq_frame, text="Q0 Allotment:").grid(row=1, column=0, padx=5, pady=5)
q0_allot_entry = tk.Entry(mlfq_frame, width=6)
q0_allot_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(mlfq_frame, text="Q1 Allotment:").grid(row=1, column=2, padx=5, pady=5)
q1_allot_entry = tk.Entry(mlfq_frame, width=6)
q1_allot_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Label(mlfq_frame, text="Q2 Allotment:").grid(row=1, column=4, padx=5, pady=5)
q2_allot_entry = tk.Entry(mlfq_frame, width=6)
q2_allot_entry.grid(row=1, column=5, padx=5, pady=5)

mlfq_frame.grid_remove()


# ---------------------------------------------------------------
# Run Simulation
# ---------------------------------------------------------------

def run_simulation():
    global result_processes, result_avg_tat, result_avg_rt

    if mode_var.get() == "manual":
        if len(manual_rows) == 0:
            messagebox.showerror("Error", "Please set the number of processes first")
            return
        try:
            procs = get_manual_processes()
        except ValueError:
            messagebox.showerror("Error", "Fill all Arrival/Burst fields with numbers")
            return
    else:
        if len(random_processes) == 0:
            messagebox.showerror("Error", "Please generate random processes first")
            return
        procs = deepcopy(random_processes)

    algo = algo_var.get()

    if algo == "fcfs":
        gantt = run(1, procs)
    elif algo == "sjf":
        gantt = run(2, procs)
    elif algo == "srtf":
        gantt = run(3, procs)
    elif algo == "rr":
        try:
            quantum = int(quantum_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid time quantum")
            return
        gantt = run_rr(procs, quantum)
    elif algo == "mlfq":
        try:
            q0 = int(q0_quantum_entry.get())
            q1 = int(q1_quantum_entry.get())
            q2 = int(q2_quantum_entry.get())
            a0 = int(q0_allot_entry.get())
            a1 = int(q1_allot_entry.get())
            a2 = int(q2_allot_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Fill all MLFQ fields with numbers")
            return
        gantt = run_mlfq(procs, q0, q1, q2, a0, a1, a2)
    else:
        return

    avg_tat, avg_rt = compute(procs)

    result_processes = procs
    result_avg_tat = avg_tat
    result_avg_rt = avg_rt

    draw_gantt(gantt)
    fill_table(procs)

    avg_label.config(
        text=f"Average Turnaround Time: {avg_tat:.2f}    Average Response Time: {avg_rt:.2f}"
    )


def reset_all():
    global random_processes, result_processes, result_avg_tat, result_avg_rt, color_map

    manual_num_entry.delete(0, tk.END)
    for widget in manual_rows_frame.winfo_children():
        widget.destroy()
    manual_rows.clear()

    random_num_entry.delete(0, tk.END)
    random_output_label.config(text="")
    random_processes = []

    quantum_entry.delete(0, tk.END)
    q0_quantum_entry.delete(0, tk.END)
    q1_quantum_entry.delete(0, tk.END)
    q2_quantum_entry.delete(0, tk.END)
    q0_allot_entry.delete(0, tk.END)
    q1_allot_entry.delete(0, tk.END)
    q2_allot_entry.delete(0, tk.END)

    canvas.delete("all")

    for row in table.get_children():
        table.delete(row)

    avg_label.config(text="Average Turnaround Time: -    Average Response Time: -")

    result_processes = []
    result_avg_tat = 0
    result_avg_rt = 0
    color_map = {}

    mode_var.set("manual")
    algo_var.set("fcfs")
    toggle_mode()
    on_algo_change()


button_frame = tk.Frame(main_frame)
button_frame.grid(row=5, column=0, pady=10)

run_button = tk.Button(button_frame, text="Run Simulation", font=("Arial", 12, "bold"),
                       bg="#4caf50", fg="white", command=run_simulation)
run_button.pack(side="left", padx=5)

refresh_button = tk.Button(button_frame, text="Refresh", font=("Arial", 12, "bold"),
                           bg="#f44336", fg="white", command=reset_all)
refresh_button.pack(side="left", padx=5)


# ---------------------------------------------------------------
# Gantt Chart
# ---------------------------------------------------------------

gantt_label = tk.Label(main_frame, text="Gantt Chart", font=("Arial", 12, "bold"))
gantt_label.grid(row=6, column=0, sticky="w")

gantt_container = tk.Frame(main_frame)
gantt_container.grid(row=7, column=0, sticky="we", pady=5)

gantt_scroll = tk.Scrollbar(gantt_container, orient="horizontal")
gantt_scroll.pack(side="bottom", fill="x")

canvas = tk.Canvas(gantt_container, height=90, bg="white", xscrollcommand=gantt_scroll.set)
canvas.pack(fill="x")

gantt_scroll.config(command=canvas.xview)


def draw_gantt(gantt):
    canvas.delete("all")

    if not gantt:
        return

    blocks = []
    current = gantt[0]
    count = 1

    for i in range(1, len(gantt)):
        if gantt[i] == current:
            count += 1
        else:
            blocks.append((current, count))
            current = gantt[i]
            count = 1
    blocks.append((current, count))

    unit_width = 30
    x = 10
    y = 10
    height = 40

    time = 0
    canvas.create_text(x, y + height + 12, text=str(time), anchor="w")

    for name, length in blocks:
        width = length * unit_width
        color = get_color(name)

        canvas.create_rectangle(x, y, x + width, y + height, fill=color, outline="black")
        canvas.create_text(x + width / 2, y + height / 2, text=name)

        x += width
        time += length
        canvas.create_text(x, y + height + 12, text=str(time), anchor="w")

    canvas.config(scrollregion=canvas.bbox("all"))


# ---------------------------------------------------------------
# Results Table
# ---------------------------------------------------------------

table_label = tk.Label(main_frame, text="Process Table", font=("Arial", 12, "bold"))
table_label.grid(row=8, column=0, sticky="w", pady=(10, 0))

columns = ("pid", "at", "bt", "ct", "tat", "rt")
table = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)

table.heading("pid", text="PID")
table.heading("at", text="Arrival Time")
table.heading("bt", text="Burst Time")
table.heading("ct", text="Completion Time")
table.heading("tat", text="Turnaround Time")
table.heading("rt", text="Response Time")

for col in columns:
    table.column(col, width=120, anchor="center")

table.grid(row=9, column=0, sticky="we", pady=5)


def fill_table(procs):
    for row in table.get_children():
        table.delete(row)

    for p in procs:
        table.insert("", "end", values=(p.pid, p.arrival, p.burst,
                                         p.completion, p.turnaround, p.response))


avg_label = tk.Label(main_frame, text="Average Turnaround Time: -    Average Response Time: -",
                      font=("Arial", 11))
avg_label.grid(row=10, column=0, pady=10)


# ---------------------------------------------------------------
# Export CSV
# ---------------------------------------------------------------

def export_csv():
    if len(result_processes) == 0:
        messagebox.showerror("Error", "Run a simulation first")
        return

    filename = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="results.csv")
    if not filename:
        return

    export_results(result_processes, result_avg_tat, result_avg_rt, filename)
    messagebox.showinfo("Export", "Results exported successfully")


export_button = tk.Button(main_frame, text="Export CSV", command=export_csv)
export_button.grid(row=11, column=0, pady=5)


root.mainloop()