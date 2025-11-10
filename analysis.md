# Lab 2 Analysis Questions

1. **Condition variables**  
   Why are two separate conditions (`cv_not_full`, `cv_not_empty`) used with the same lock? Could one condition work, and what are the trade-offs?

2. **wait() loop**  
   Explain why `wait()` must be inside a `while` that rechecks the condition. What can go wrong with an `if` (spurious wakeups, races after notify)?

3. **notify() calls**  
   What happens if a producer skips `cv_not_empty.notify()` after adding, or a consumer skips `cv_not_full.notify()` after removing?

4. **Mutual exclusion**  
   Describe the incorrect behaviours if `with self.lock:` is removed from `put` and `get` (e.g., lost items, duplicates, corrupted counts, out-of-order state).
