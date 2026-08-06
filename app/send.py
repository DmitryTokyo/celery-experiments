"""Put a task message into the broker from the command line."""

import argparse
import ast

from app.celery_app import celery_app


def parse_value(raw: str) -> object:
    """Convert numbers and Python literals; leave ordinary words as strings."""
    try:
        return ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return raw


parser = argparse.ArgumentParser(description="Send a Celery task")
parser.add_argument("task", help="Task name from app/tasks.py")
parser.add_argument("arguments", nargs="*", help="Positional task arguments")
parser.add_argument("--queue", default="default")
parser.add_argument("--count", type=int, default=1)
options = parser.parse_args()

if options.count < 1:
    parser.error("--count must be at least 1")

task_name = f"app.tasks.{options.task}"
task_arguments = [parse_value(value) for value in options.arguments]

for _ in range(options.count):
    result = celery_app.send_task(task_name, args=task_arguments, queue=options.queue)
    print(f"sent {task_name} id={result.id} args={task_arguments} queue={options.queue}")
