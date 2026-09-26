# COMP-5002 – Lab 2 • Bounded Buffer Implementation

**Module** Module 3. Advanced Concurrency & Synchronization Techniques  
**Objective** Implement a bounded buffer (producer–consumer) using `threading.Lock` and `threading.Condition` to manage producer–consumer interactions correctly.

## Prerequisites

- Python 3 installed.
- Git installed and basic familiarity with `clone`, `add`, `commit`, `push`.
- Understanding from Modules 2 and 3:
  - Threads (`threading.Thread`, `start()`, `join()`).
  - Race conditions and critical sections.
  - Mutual exclusion locks (`threading.Lock`, `with` statement).
  - Condition variables (`threading.Condition`, `wait()`, `notify()`, `notify_all()`), and condition-checking loops.
  - The bounded-buffer problem (producers, consumers, capacity constraints).

## Files Provided

- `README.md` this file
- `lab2_buffer.py` starter with `BoundedBuffer`, `producer`, `consumer`, and a `main` block
- `analysis.md` where you answer the analysis questions

## Tasks

**General instructions**

- Clone the repository created for you by GitHub Classroom.
- Modify `lab2_buffer.py` to complete the tasks.
- Run the script and observe producer–consumer behaviour.
- Answer the analysis questions in `analysis.md`.
- Commit frequently with meaningful messages.
- Push your final changes before the deadline.

---

### Task 1 — Initialise synchronization for `BoundedBuffer`

The starter already validates the capacity and creates the underlying `deque`. Your task is to add the synchronization objects.

1. Open `lab2_buffer.py`.
2. In `BoundedBuffer.__init__`:
   - Create one shared `threading.Lock`.
   - Create `cv_not_full` and `cv_not_empty` as `threading.Condition` objects that both use that same lock.
3. Do not create separate locks for the two conditions.

The buffer intentionally uses a normal `deque()` rather than `deque(maxlen=...)`. Capacity must be enforced by your synchronization logic; the container should not silently discard old items if your logic is wrong.

---

### Task 2 — Implement `put` (producer logic)

In `BoundedBuffer.put`:

1. Acquire the shared lock.
2. While the buffer is full, print a waiting message and wait on `cv_not_full`.
3. Append the new item only after space is available.
4. Print a produced message.
5. Notify one thread waiting on `cv_not_empty`.

Use a `while` loop for the condition check, not an `if`.

---

### Task 3 — Implement `get` (consumer logic)

In `BoundedBuffer.get`:

1. Acquire the shared lock.
2. While the buffer is empty, print a waiting message and wait on `cv_not_empty`.
3. Remove and store the oldest item with `popleft()`.
4. Print a consumed message.
5. Notify one thread waiting on `cv_not_full`.
6. Return the item.

Use a `while` loop for the condition check, not an `if`.

---

### Task 4 — Run and verify

1. Review the provided `producer`, `consumer`, and `main`.
2. Run `python lab2_buffer.py`.
3. Verify that:
   - producers wait when the buffer is full;
   - consumers wait when the buffer is empty;
   - no item is consumed before it has been produced;
   - the buffer size never exceeds `BUFFER_SIZE`;
   - the program completes without deadlock;
   - all produced items are consumed and the final buffer size is `0`.

The driver distributes the total number of items exactly across the configured consumers, including when `NUM_PRODUCERS * ITEMS_PER_PRODUCER` is not evenly divisible by `NUM_CONSUMERS`.

---

### Task 5 — Analysis (`analysis.md`)

Answer the following:

1. **Condition variables** Why two conditions (`cv_not_full`, `cv_not_empty`) sharing one lock are used; could one condition suffice and what are the trade-offs?
2. **`wait()` loops** Why `wait()` must be in a `while` that rechecks the condition; include spurious wakeups and the fact that another thread may change the state before a woken thread proceeds.
3. **`wait()` behaviour** What happens to the associated lock while a thread is blocked in `Condition.wait()`, and why is that necessary?
4. **`notify()` calls** Consequences if producers forget `cv_not_empty.notify()` or consumers forget `cv_not_full.notify()`.
5. **Mutual exclusion** What happens if the shared lock is not held while checking or changing the buffer state, and what does Python require when calling `Condition.wait()` and `Condition.notify()`?

---

## Submission

1. Ensure `lab2_buffer.py` runs correctly.
2. Ensure `analysis.md` is complete.
3. Stage: `git add lab2_buffer.py analysis.md` (or `git add .`)
4. Commit: `git commit -m "Complete Lab 2 Bounded Buffer"`
5. Push: `git push origin main` (or your default branch)
6. Verify on GitHub that `lab2_buffer.py` and `analysis.md` are updated.
