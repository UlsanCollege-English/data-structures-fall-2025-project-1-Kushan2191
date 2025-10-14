import sys
from typing import List
from src.parser import parse_command
from src.scheduler import Scheduler

def main() -> None:
    sched = Scheduler()

    for raw in sys.stdin:
        line = raw.rstrip("\n")

        if line == "":
            print("Break time!")
            return

        parsed = parse_command(line)
        logs: List[str] = []

        if parsed is None:
            continue

        cmd, args = parsed

        try:
            if cmd == "CREATE":
                if len(args) != 2:
                    logs.append("time=? event=error reason=bad_args")
                else:
                    qid, cap_str = args
                    cap = int(cap_str)
                    logs.extend(sched.create_queue(qid, cap))

            elif cmd == "ENQ":
                if len(args) != 2:
                    logs.append("time=? event=error reason=bad_args")
                else:
                    qid, item = args
                    logs.extend(sched.enqueue(qid, item))

            elif cmd == "SKIP":
                if len(args) != 1:
                    logs.append("time=? event=error reason=bad_args")
                else:
                    (qid,) = args
                    logs.extend(sched.mark_skip(qid))

            elif cmd == "RUN":
                if not (1 <= len(args) <= 2):
                    logs.append("time=? event=error reason=bad_args")
                else:
                    quantum = int(args[0])
                    steps = int(args[1]) if len(args) == 2 else None
                    logs.extend(sched.run(quantum, steps))
                    display = sched.display()
                    if display:
                        logs.append(display)

            else:
                logs.append("time=? event=error reason=unknown_command")

        except ValueError:
            logs.append("time=? event=error reason=bad_args")

        if logs:
            print("\n".join(logs))

if __name__ == "__main__":
    main()
