from src.task2.printing_optimizer import optimize_printing

def test_optimizer_smoke():
    jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]
    constraints = {"max_volume": 300, "max_items": 2}
    res = optimize_printing(jobs, constraints)
    assert isinstance(res, dict)
    assert "print_order" in res and "total_time" in res
