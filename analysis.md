# Lab 2 Analysis Questions

1. **Condition variables**  
 We use two separate conditions even though they share the same lock because they represent two different states we’re waiting for.
cv_not_full is for producers waiting until there’s space to add items.
cv_not_empty is for consumers waiting until there’s something to remove.
Technically, you could use one condition variable for both, but then every time you notify, threads would have to wake up and check whether they can proceed. This would cause more unnecessary wake-ups and slightly worse performance. Two separate conditions make the signaling more precise and efficient

2. **wait() loop**  
wait() must be inside a while loop because even after being notified, the condition you were waiting for might not actually be true.
This can happen due to spurious wakeups, where a thread wakes up without a notify().
Or because another thread might have grabbed the resource first (race condition).
Using if would assume the condition is guaranteed, which can lead to errors like overfilling the buffer or consuming from an empty buffer

3. **notify() calls**  
If a producer doesn’t call cv_not_empty.notify() after adding an item, a consumer could stay blocked forever, even though there’s now data to consume.
Similarly, if a consumer skips cv_not_full.notify() producers waiting for space might stay blocked indefinitely, causing a deadlock.

4. **Mutual exclusion**  
If we remove with self.lock: from put and get, multiple threads could access and modify the buffer at the same time. This can cause serious issues:
- Lost items: two producers write over each other.
- Duplicate or missing items: consumers read the same item twice or skip items.
- Corrupted counts / broken state: the buffer’s len() may not match actual items.
- Out-of-order operations: items can appear consumed before being added.
Locks ensure only one thread manipulates the buffer at a time, preventing all these problems.