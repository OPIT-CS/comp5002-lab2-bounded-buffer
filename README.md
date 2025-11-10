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
  - Condition variables (`threading.Condition`, `wait()`, `notify()`, `notify_all()`), and condition checking loops.
  - Bounded buffer problem (producers, consumers, capacity constraints).

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

### Task 1 — Initialise the `BoundedBuffer` class

1. Open `lab2_buffer.py`.
2. In `BoundedBuffer.__init__`:
   - Set `self.capacity`.
   - Create `self.buffer` as a `deque(maxlen=capacity)`.
   - Create `self.lock = threading.Lock()`.
   - Create `self.cv_not_full = threading.Condition(self.lock)`.
   - Create `self.cv_not_empty = threading.Condition(self.lock)`.

---

### Task 2 — Implement `put` (producer logic)

1. In `BoundedBuffer.put`:
   - Use `with self.lock:`.
   - While the buffer is full, print a waiting message and `self.cv_not_full.wait()`.
   - Append `item` to `self.buffer`.
   - Print a produced message.
   - Call `self.cv_not_empty.notify()`.

---

### Task 3 — Implement `get` (consumer logic)

1. In `BoundedBuffer.get`:
   - Use `with self.lock:`.
   - While the buffer is empty, print a waiting message and `self.cv_not_empty.wait()`.
   - Remove an item with `self.buffer.popleft()`.
   - Print a consumed message.
   - Call `self.cv_not_full.notify()`.
   - Return the item.

---

### Task 4 — Run and observe

1. Review the provided `producer`, `consumer`, and `main`.
2. Run `python lab2_buffer.py`.
3. Watch the output: verify waiting messages appear when appropriate, run completes without deadlock, and the final buffer size looks reasonable.

---

### Task 5 — Analysis (`analysis.md`)

Answer the following:

1. **Condition variables** Why two conditions (`cv_not_full`, `cv_not_empty`) sharing one lock are used; could one suffice and what are the trade-offs?
2. **`wait()` loops** Why `wait()` must be in a `while` that rechecks the condition; risks of using `if` (spurious wakeups, races after notify).
3. **`notify()` calls** Consequences if producers forget `cv_not_empty.notify()` or consumers forget `cv_not_full.notify()`.
4. **Mutual exclusion** What goes wrong without `with self.lock:` in `put` and `get` (specific buffer state races).

---

## Submission

1. Ensure `lab2_buffer.py` runs correctly.
2. Ensure `analysis.md` is complete.
3. Stage: `git add lab2_buffer.py analysis.md` (or `git add .`)
4. Commit: `git commit -m "Complete Lab 2 Bounded Buffer"`
5. Push: `git push origin main` (or your default branch)
6. Verify on GitHub that `lab2_buffer.py` and `analysis.md` are updated.
