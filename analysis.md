# Lab 2 Analysis Questions

1. **Condition variables**
   Why are two separate conditions (`cv_not_full`, `cv_not_empty`) used with the same lock? Could one condition work, and what are the trade-offs?

2. **`wait()` loop**
   Explain why `wait()` must be inside a `while` that rechecks the condition. Include both spurious wakeups and the possibility that another thread changes the buffer state before a woken thread can proceed.

3. **Lock behaviour during `wait()`**
   What happens to the condition's associated lock while a thread is blocked in `Condition.wait()`? Why must the lock be released while waiting and reacquired before `wait()` returns?

4. **`notify()` calls**
   What happens if a producer skips `cv_not_empty.notify()` after adding an item, or a consumer skips `cv_not_full.notify()` after removing one?

5. **Mutual exclusion and condition ownership**
   Explain what can go wrong if the buffer-full / buffer-empty checks and the corresponding mutations are not protected by the shared lock. Also state what Python requires when calling `Condition.wait()` or `Condition.notify()` without owning the associated lock.
