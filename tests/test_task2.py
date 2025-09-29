from src.task2.printing_optimizer import optimize_printing

def test_expected_from_pdf_same_priority():
    jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]
    constraints = {"max_volume": 300, "max_items": 2}
    res = optimize_printing(jobs, constraints)
    # порядок зберігає вхідний у межах пріоритету
    assert res["print_order"] == ["M1", "M2", "M3"]
    # партія1: M1+M2 => max(120,90)=120; партія2: M3 => 150; разом 270
    assert res["total_time"] == 270

def test_expected_from_pdf_diff_priority():
    jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лаба
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # диплом
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150},  # особистий
    ]
    constraints = {"max_volume": 300, "max_items": 2}
    res = optimize_printing(jobs, constraints)
    assert res["print_order"] == ["M2", "M1", "M3"]
    # партії: [M2, M1] => max(90,120)=120; [M3] => 150; разом 270
    assert res["total_time"] == 270

def test_expected_from_pdf_over_limits():
    jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]
    constraints = {"max_volume": 300, "max_items": 2}
    res = optimize_printing(jobs, constraints)
    assert res["print_order"] == ["M1", "M2", "M3"]
    # партії: [M1] => 180; [M2] => 150; [M3] => 120; разом 450
    assert res["total_time"] == 450
