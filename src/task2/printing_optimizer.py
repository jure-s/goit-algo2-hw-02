from dataclasses import dataclass
from typing import List, Dict, Iterable, Tuple

@dataclass(frozen=True)
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int  # хвилини

@dataclass(frozen=True)
class PrinterConstraints:
    max_volume: float
    max_items: int

def _normalize_jobs(print_jobs: Iterable[Dict]) -> List[PrintJob]:
    jobs: List[PrintJob] = []
    for i, j in enumerate(print_jobs):
        try:
            pid = str(j["id"])
            vol = float(j["volume"])
            pr = int(j["priority"])
            pt = int(j["print_time"])
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid job at index {i}: {j}") from e
        if vol <= 0 or pt <= 0:
            raise ValueError(f"Job {pid} must have positive volume and print_time")
        jobs.append(PrintJob(pid, vol, pr, pt))
    if not jobs:
        raise ValueError("print_jobs must be a non-empty list")
    return jobs

def _normalize_constraints(constraints: Dict) -> PrinterConstraints:
    try:
        mv = float(constraints["max_volume"])
        mi = int(constraints["max_items"])
    except (KeyError, ValueError, TypeError) as e:
        raise ValueError("constraints must include numeric 'max_volume' and integer 'max_items'") from e
    if mv <= 0 or mi <= 0:
        raise ValueError("constraints must be positive")
    return PrinterConstraints(mv, mi)

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Враховує:
      - Пріоритети: нижче число = вище пріоритет; між завданнями з ОДНАКОВИМ пріоритетом зберігаємо вихідний порядок.
      - Групування: пакуємо послідовно у партії, не перевищуючи max_items та max_volume.
      - Час: загальний = сума (максимальний print_time у кожній партії).

    Повертає:
      {"print_order": [ID...], "total_time": int}
    """
    jobs = _normalize_jobs(print_jobs)
    cons = _normalize_constraints(constraints)

    # Стабільне сортування: лише за пріоритетом (Python sort — stable), вихідний порядок у межах одного пріоритету збережеться
    jobs.sort(key=lambda j: j.priority)

    print_order: List[str] = []
    total_time = 0

    batch: List[PrintJob] = []
    batch_volume = 0.0

    def flush_batch():
        nonlocal batch, batch_volume, total_time, print_order
        if not batch:
            return
        # Час партії — максимум серед print_time у партії
        batch_time = max(j.print_time for j in batch)
        total_time += batch_time
        # Підсумковий «плоский» порядок — у тій самій послідовності, як додавали в партію
        print_order.extend([j.id for j in batch])
        batch.clear()
        batch_volume = 0.0

    for job in jobs:
        # Якщо одна модель більша за допустимий об'єм — її фізично надрукувати неможливо (пропускаємо)
        if job.volume > cons.max_volume:
            continue

        fits_items = (len(batch) + 1) <= cons.max_items
        fits_volume = (batch_volume + job.volume) <= cons.max_volume

        # Якщо не влазить — друкуємо поточну партію і починаємо нову
        if not (fits_items and fits_volume):
            flush_batch()

        # Додаємо до (нової/поточн.) партії
        batch.append(job)
        batch_volume += job.volume

    # Остання партія
    flush_batch()

    return {"print_order": print_order, "total_time": total_time}
