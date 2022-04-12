import unittest
import priority_queue

class TestQueue(unittest.TestCase):
    
    def setUp(self):
        """create an empty queue to test"""
        self.my_queue = priority_queue.PriorityQueue()
    
    def test_init(self):
        """ tests whether init method correctly creates a PriorityQueue"""
        #check that the queue is a PriorityQueue object
        self.assertIsInstance(self.my_queue, priority_queue.PriorityQueue)
        #check that the PriorityQueue is a dictionary
        self.assertIsInstance(self.my_queue.queue, dict)
        #check that queue is empty
        self.assertTrue(len(self.my_queue.queue) == 0)

    def test_push(self):
        """ Test whether the push method correctly adds items to the queue."""
        # make sure we can't add a string as the priority
        with self.assertRaises(ValueError):
            self.my_queue.push("string", "object")
        #add some items to the queue out of order
        self.my_queue.push(3, "banana")
        self.my_queue.push(1, "apple")
        self.my_queue.push(4, "peach")
        self.my_queue.push(2, "grape")
        #test that items were added to queue
        self.assertTrue("apple" in self.my_queue.queue[1][0])
    
    def test_max_priority(self):
        '''check whether the method returns the correct key and value
        pair as a set'''
        #adds items to the queue
        self.my_queue.push(3, "banana")
        self.my_queue.push(1, "apple")
        self.my_queue.push(4, "peach")
        self.my_queue.push(2, "grape")
        max = self.my_queue.max_priority()
        self.assertTrue(max == 4)
    
    def test_pop(self):
        #test that an error is raised when queue is empty
        with self.assertRaises(KeyError):
            self.my_queue.pop()
        #add itmes to the queue
        self.my_queue.push(1, "banana")
        self.my_queue.push(2, "apple")
        self.my_queue.push(3, "peach")
        self.my_queue.push(4, "grape")
        #check that correct item was returned
        item = self.my_queue.pop()
        self.assertTrue(item == (4, "grape"))
        #check that a tuple was returned
        self.assertIsInstance(item, tuple)
        #check that item is no longer in queue
        self.assertFalse("grape" in self.my_queue.queue)
        
    def test_peek(self):
        #test that an error is raised when queue is empty
        with self.assertRaises(KeyError):
            self.my_queue.peek()
        #add items to queue
        self.my_queue.push(1, "banana")
        self.my_queue.push(2, "apple")
        self.my_queue.push(3, "peach")
        self.my_queue.push(4, "grape")
        #calls peek method andd assigns return value to variable
        next = self.my_queue.peek()
        #check variable to see if right value was returned
        self.assertTrue(next == (4, "grape"))
        
    def test_len(self):
        #adds items to queue
        self.my_queue.push(1, "banana")
        self.my_queue.push(2, "apple")
        self.my_queue.push(3, "peach")
        self.my_queue.push(4, "grape")
        #checks for correct length
        self.assertTrue(self.my_queue.__len__() == 4)
        



        
if __name__ == "__main__":
    unittest.main()