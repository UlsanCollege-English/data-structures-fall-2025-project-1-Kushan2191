from dataclasses import dataclass
from typing import Dict, List, Optional

REQUIRED_MENU: Dict[str, int] = {
    "americano": 2,
    "latte": 3,
    "cappuccino": 3,
    "mocha": 4,
    "tea": 1,
    "macchiato": 2,
    "hot_chocolate": 4,
}

@dataclass
class Task:
    task_id: str
    remaining: int

class QueueRR:
    def __init__(self, queue_id: str, capacity: int) -> None:
        self.id = queue_id
        self.capacity = capacity
        self.data = [None] * capacity
        self.front = 0
        self.rear = 0
        self.size = 0

    def enqueue(self, task: Task) -> bool:
        if self.size == self.capacity:
            return False
        self.data[self.rear] = task
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
        return True

    def dequeue(self) -> Optional[Task]:
        if self.size == 0:
            return None
        t = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return t

    def peek(self) -> Optional[Task]:
        if self.size == 0:
            return None
        return self.data[self.front]

    def __len__(self) -> int:
        return self.size

class Scheduler:
    def __init__(self) -> None:
        self.time = 0
        self.queues: Dict[str, QueueRR] = {}
        self.q_order: List[str] = []
        self.id_counters: Dict[str, int] = {}
        self.skip_flags: Dict[str, bool] = {}
        self.menu_map = dict(REQUIRED_MENU)
        self.rr_index = 0

    def menu(self) -> Dict[str, int]:
        return dict(self.menu_map)

    def next_queue(self) -> Optional[str]:
        if not self.q_order:
            return None
        return self.q_order[self.rr_index]

    def create_queue(self, queue_id: str, capacity: int) -> List[str]:
        if queue_id not in self.queues:
            q = QueueRR(queue_id, capacity)
            self.queues[queue_id] = q
            self.q_order.append(queue_id)
            self.id_counters[queue_id] = 1
            self.skip_flags[queue_id] = False
            return [f"time={self.time} event=create queue={queue_id}"]
        return []

    def enqueue(self, queue_id: str, item_name: str) -> List[str]:
        if item_name not in self.menu_map:
            print("Sorry, we don't serve that.")
            return [f"time={self.time} event=reject queue={queue_id} reason=unknown_item"]
        if queue_id not in self.queues:
            return [f"time={self.time} event=reject queue={queue_id} reason=unknown_queue"]
        burst = self.menu_map[item_name]
        tid_num = self.id_counters[queue_id]
        self.id_counters[queue_id] += 1
        task_id = f"{queue_id}-{tid_num:03d}"
        t = Task(task_id, burst)
        q = self.queues[queue_id]
        if not q.enqueue(t):
            print("Sorry, we're at capacity.")
            return [f"time={self.time} event=reject queue={queue_id} reason=full"]
        return [f"time={self.time} event=enqueue queue={queue_id} task={task_id} remaining={burst}"]

    def mark_skip(self, queue_id: str) -> List[str]:
        if queue_id in self.skip_flags:
            self.skip_flags[queue_id] = True
            return [f"time={self.time} event=skip queue={queue_id}"]
        return []

    def run(self, quantum: int, steps: Optional[int]) -> List[str]:
        n = len(self.q_order)
        if n == 0:
            return []
        if steps is not None:
            if not (1 <= steps <= n):
                return [f"time={self.time} event=error reason=invalid_steps"]
        logs: List[str] = []
        turns = steps if steps is not None else n
        visited = 0
        while visited < turns:
            qid = self.q_order[self.rr_index]
            logs.append(f"time={self.time} event=run queue={qid}")
            if self.skip_flags[qid]:
                self.skip_flags[qid] = False
            else:
                q = self.queues[qid]
                if len(q) > 0:
                    t = q.peek()
                    work = min(t.remaining, quantum)
                    t.remaining -= work
                    self.time += work
                    logs.append(f"time={self.time} event=work queue={qid} task={t.task_id} ran={work} rem={t.remaining}")
                    if t.remaining == 0:
                        q.dequeue()
                        logs.append(f"time={self.time} event=finish queue={qid} task={t.task_id}")
            self.rr_index = (self.rr_index + 1) % n
            visited += 1
        return logs

    def display(self) -> List[str]:
        lines: List[str] = []
        next_q = self.next_queue()
        next_str = next_q if next_q is not None else "None"
        lines.append(f"display time={self.time} next={next_str}")
        menu_items = ",".join(f"{k}:{self.menu_map[k]}" for k in sorted(self.menu_map.keys()))
        lines.append(f"display menu=[{menu_items}]")
        for qid in self.q_order:
            q = self.queues[qid]
            skip_tag = " skip" if self.skip_flags[qid] else ""
            tasks_repr = []
            idx = q.front
            count = q.size
            for _ in range(count):
                t = q.data[idx]
                tasks_repr.append(f"{t.task_id}:{t.remaining}")
                idx = (idx + 1) % q.capacity
            tasks_str = ",".join(tasks_repr)
            lines.append(f"display {qid} [{len(q)}/{q.capacity}]{skip_tag} -> [{tasks_str}]")
        return lines


