def draw(schedule):

    if not schedule:
        print("No schedule to display.")
        return

    print("\n" + "=" * 80)
    print(" " * 30 + "GANTT CHART")
    print("=" * 80)

    blocks = []
    start_times = [0]

    current = schedule[0]
    count = 1

    for i in range(1, len(schedule)):
        if schedule[i] == current:
            count += 1
        else:
            blocks.append((current, count))
            start_times.append(i)
            current = schedule[i]
            count = 1

    blocks.append((current, count))

    print("+", end="")
    for name, length in blocks:
        print("-" * (length * 4) + "+", end="")
    print()

    print("|", end="")
    for name, length in blocks:
        width = length * 4
        print(f"{name:^{width}}|", end="")
    print()

    print("+", end="")
    for name, length in blocks:
        print("-" * (length * 4) + "+", end="")
    print()

    time = 0
    print(f"{time:<2}", end="")

    for _, length in blocks:
        time += length
        print(f"{time:>{length*4+1}}", end="")

    print("\n")