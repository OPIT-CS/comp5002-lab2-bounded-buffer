# lab2_buffer.py
import random
import threading
import time
from collections import deque

# Configuration
BUFFER_SIZE = 5
NUM_PRODUCERS = 2
NUM_CONSUMERS = 2
PRODUCER_DELAY = 0.2  # Avg time for producer to create item
CONSUMER_DELAY = 0.5  # Avg time for consumer to process item
ITEMS_PER_PRODUCER = 8


class BoundedBuffer:
    """A thread-safe bounded buffer using Lock and Condition variables."""

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Capacity must be > 0")

        # Basic buffer state is provided.
        self.capacity = capacity
        self.buffer = deque()

        # --- TODO: Task 1 - Initialise synchronization ---
        # Create ONE threading.Lock shared by both conditions.
        # Create cv_not_full and cv_not_empty as threading.Condition objects
        # that both use that same lock.
        # --- End TODO ---

    def put(self, item):
        """Add an item to the buffer. Blocks if the buffer is full."""
        # --- TODO: Task 2 - Implement put logic ---
        # 1) Acquire the shared lock.
        # 2) While len(self.buffer) >= self.capacity, wait on cv_not_full.
        # 3) Append the item.
        # 4) Print the produced item and current buffer size.
        # 5) Notify one waiter on cv_not_empty.
        # --- End TODO ---
        raise NotImplementedError("Complete Task 2: BoundedBuffer.put")

    def get(self):
        """Remove and return an item from the buffer. Blocks if the buffer is empty."""
        # --- TODO: Task 3 - Implement get logic ---
        # 1) Acquire the shared lock.
        # 2) While the buffer is empty, wait on cv_not_empty.
        # 3) Remove the oldest item with popleft().
        # 4) Print the consumed item and current buffer size.
        # 5) Notify one waiter on cv_not_full.
        # 6) Return the item.
        # --- End TODO ---
        raise NotImplementedError("Complete Task 3: BoundedBuffer.get")


# ==================================
# Producer & Consumer Functions
# ==================================


def producer(thread_id, buffer):
    """Producer thread function."""
    for i in range(ITEMS_PER_PRODUCER):
        item = f"Item-{thread_id}-{i}"
        # Simulate time taken to produce item.
        time.sleep(random.uniform(0, PRODUCER_DELAY * 2))
        buffer.put(item)
    print(f"Producer {thread_id} finished.")


def consumer(thread_id, buffer, items_to_consume):
    """Consumer thread function."""
    for _ in range(items_to_consume):
        buffer.get()
        # Simulate time taken to consume/process the item.
        time.sleep(random.uniform(0, CONSUMER_DELAY * 2))
    print(f"Consumer {thread_id} finished.")


def consumer_workloads(total_items, num_consumers):
    """Distribute total_items exactly across num_consumers consumers."""
    if num_consumers <= 0:
        raise ValueError("Number of consumers must be > 0")

    base, remainder = divmod(total_items, num_consumers)
    return [base + (1 if i < remainder else 0) for i in range(num_consumers)]


def run_worker(errors, error_lock, target, *args):
    """Run a thread target and preserve any exception for the main thread."""
    try:
        target(*args)
    except Exception as exc:
        with error_lock:
            errors.append((threading.current_thread().name, exc))


# ==================================
# Main Execution
# ==================================

if __name__ == "__main__":
    total_items = ITEMS_PER_PRODUCER * NUM_PRODUCERS
    workloads = consumer_workloads(total_items, NUM_CONSUMERS)

    print(f"Starting Bounded Buffer simulation (Capacity: {BUFFER_SIZE})")
    print(f"Producers: {NUM_PRODUCERS}, Consumers: {NUM_CONSUMERS}")
    print(f"Items per Producer: {ITEMS_PER_PRODUCER}")
    print(f"Total items: {total_items}")
    print("-" * 30)

    buffer = BoundedBuffer(BUFFER_SIZE)
    producers = []
    consumers = []
    thread_errors = []
    error_lock = threading.Lock()

    # Create and start producer threads.
    for i in range(NUM_PRODUCERS):
        p_thread = threading.Thread(
            target=run_worker,
            args=(thread_errors, error_lock, producer, i, buffer),
            name=f"producer-{i}",
        )
        producers.append(p_thread)
        p_thread.start()

    # Create and start consumer threads. Each receives an exact workload.
    for i, workload in enumerate(workloads):
        c_thread = threading.Thread(
            target=run_worker,
            args=(thread_errors, error_lock, consumer, i, buffer, workload),
            name=f"consumer-{i}",
        )
        consumers.append(c_thread)
        c_thread.start()

    print("Main: Waiting for producers...")
    for p_thread in producers:
        p_thread.join()
    print("Main: Producers finished.")

    print("Main: Waiting for consumers...")
    for c_thread in consumers:
        c_thread.join()
    print("Main: Consumers finished.")

    if thread_errors:
        print("-" * 30)
        print("Simulation failed because one or more worker threads raised an exception:")
        for thread_name, exc in thread_errors:
            print(f"  {thread_name}: {type(exc).__name__}: {exc}")
        raise SystemExit(1)

    print("-" * 30)
    print(f"Final buffer size: {len(buffer.buffer)}")
    print("Simulation finished.")
