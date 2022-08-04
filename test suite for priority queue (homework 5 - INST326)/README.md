## ASSIGNMENT INSTRUCTIONS
This homework involves writing unit tests for an implementation of a priority queue. A regular queue is like a line at the store. Items are added in a certain order via an operation called push or enqueue; this is analogous to people getting in line. Items can be removed (and retrieved) via an operation called pop, pull, or dequeue; this is analogous to people at the store getting served and leaving the line. At any given time, one can determine the length of the queue. If the queue is non-empty, an operation called peek can be used to see which item is at the front of the queue (in other words, which item will be the next item returned by pop).

A priority queue is like a regular queue except that the user also specifies a priority for each item as it is added to the queue. The pop operation determines the highest priority of any item in the queue and returns the next item with that priority.

For this assignment, you will use the unittest framework to create a test suite for an implementation of a simple priority queue.
