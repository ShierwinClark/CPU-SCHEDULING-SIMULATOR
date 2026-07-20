import csv


def export_results(processes, avg_tat, avg_rt, filename="results.csv"):

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "PID",
                "Arrival Time",
                "Burst Time",
                "Completion Time",
                "Turnaround Time",
                "Response Time",
            ]
        )

        for p in processes:

            writer.writerow(
                [
                    p.pid,
                    p.arrival,
                    p.burst,
                    p.completion,
                    p.turnaround,
                    p.response,
                ]
            )

        writer.writerow([])
        writer.writerow(["Average Turnaround Time", avg_tat])
        writer.writerow(["Average Response Time", avg_rt])

    print(f"\nResults exported successfully to '{filename}'.")