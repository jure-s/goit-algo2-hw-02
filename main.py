import sys

def run_task1_demo():
    from src.task1.minmax_divide_conquer import find_min_max

    arr = [7, -2, 15, 0, 4, 9]
    mn, mx = find_min_max(arr)
    print("=== Task 1: Min/Max Divide and Conquer ===")
    print("Input array:", arr)
    print("Minimum:", mn)
    print("Maximum:", mx)
    print()

def run_task2_demo():
    from src.task2.printing_optimizer import optimize_printing, PrintJob, PrinterConstraints

    jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]
    constraints = {
        "max_volume": 300,
        "max_items": 2,
    }

    result = optimize_printing(jobs, constraints)
    print("=== Task 2: 3D Print Optimizer ===")
    print("Print order:", result["print_order"])
    print("Total print time:", result["total_time"])
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [task1|task2]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "task1":
        run_task1_demo()
    elif command == "task2":
        run_task2_demo()
    else:
        print("Unknown command:", command)
        print("Use: task1 or task2")
        sys.exit(1)
