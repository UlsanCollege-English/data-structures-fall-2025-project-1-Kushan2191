# Multi-Queue Round-Robin Café (Interactive CLI)

This project simulates a **multi-queue round-robin scheduling system** for a campus café.  
Customers arrive in different queues (e.g., Mobile, Walk-ins, Faculty), and the barista serves them fairly by rotating between queues in a **round-robin** fashion.  

The system provides an **interactive CLI** that:
- Parses commands like `CREATE`, `ENQ`, `SKIP`, and `RUN`.
- Uses a scheduler to manage multiple queues with individual capacities.
- Simulates serving tasks with time quanta, producing logs and display output after each run.

This is Project 1 for **Data Structures – Fall 2025**.

---

## How to run

1. Open a terminal and move to the **project root directory**:

   ```bash
   cd data-structures-fall-2025-project-1-Kushan2191
Run the interactive CLI:

bash
Copy code
python -m src.cli
Enter commands one per line. For example:

css
Copy code
CREATE A 3
CREATE B 2
ENQ A latte
ENQ B mocha
ENQ A tea
RUN 5 2

To end the session, press Enter on a blank line:

css
Copy code
Break time!
How to run tests locally
Make sure pytest is installed:

bash
Copy code
pip install pytest
Run the tests from the project root:

bash
Copy code
# Windows (PowerShell)
$env:PYTHONPATH="src"
python -m pytest

# macOS/Linux
PYTHONPATH=src python -m pytest
This sets the Python module path so the tests can find scheduler and parser under src/.

Complexity Notes
Queue design:
Each queue is implemented using a circular buffer (or collections.deque) to achieve constant-time operations without shifting elements.

Time complexity:

enqueue: O(1) amortized

dequeue: O(1) amortized

run: O(#turns + total_minutes_worked) — each turn processes up to the specified quantum.

Space complexity:

O(N), where N is the total number of enqueued items plus metadata for queues.

Each queue uses a fixed-size buffer equal to its capacity.