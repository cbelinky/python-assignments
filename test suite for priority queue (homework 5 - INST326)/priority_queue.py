""" Module that provides an implementation of a priority queue. """

class PriorityQueue:
    """ PriorityQueue.
    
    Attributes:
        queue (dict of int: list of object): queue where keys are
            priorities (higher numbers = higher priorities) and values
            are prioritized items.
    """
    def __init__(self):
        """ Initialize an empty priority queue. """
        self.queue = dict()
    
    def push(self, priority, item):
        """ Add a prioritized item to the queue.
        
        Args:
            priority (int): the priority of the item to be added to the
                queue.
            item (object): the value to be added to the queue.
        
        Side effects:
            Adds item to the queue with the requested priority.
            
        Raises:
            ValueError: specified priority is not an integer.
        """
        if not isinstance(priority, int):
            raise ValueError("priority must be an int")
        if priority not in self.queue:
            self.queue[priority] = []
        self.queue[priority].append(item)
    
    def max_priority(self):
        """ Get the highest priority in the queue. """
        return max(self.queue) if len(self) else None

    def pop(self):
        """ Get the next item from the queue along with its priority;
        remove the item from the queue.
        
        Returns:
            tuple of (int, object): the priority of the item and the
            item itself.
        
        Side effects:
            Removes the item from the queue.
            
        Raises:
            KeyError: the queue is empty.
        """
        priority = self.max_priority()
        if priority is None:
            raise KeyError("dequeue from empty queue")
        value = self.queue[priority].pop(0)
        if len(self.queue[priority]) == 0:
            del self.queue[priority]
        return priority, value
    
    def peek(self):
        """ Get the next item from the queue and its priority, but do
        not remove the item from the queue.
        
        Returns:
            tuple of (int, object): the priority of the item and the
            item itself.

        Raises:
            KeyError: queue is empty.        
        """
        priority = self.max_priority()
        if priority is None:
            raise KeyError("dequeue from empty queue")
        return priority, self.queue[priority][0]
    
    def __len__(self):
        """ Return the number of items in the priority queue. """
        return (0 if not self.queue
                else sum(len(self.queue[key]) for key in self.queue))
