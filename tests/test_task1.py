from src.task1.minmax_divide_conquer import find_min_max

def test_find_min_max_basic():
    arr = [5, 1, 9, -3, 7]
    assert find_min_max(arr) == (-3, 9)
