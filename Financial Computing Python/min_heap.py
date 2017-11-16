
# File: min_heap_test_solution.py
# Author(s): Jingyi Guo

# complete the definition of the min_heap class, including:
#
# add(val) -- add a value to the min_heap
# pop()    -- remove and return the value at the top
#             of the min_heap
# size()   -- return the number of elements in the min_heap
# print_pretty() -- display the min_heap in binary tree form,
#                   top to bottom (you should be able to figure
#                   out nice indentation at each level)

import math

# 1.a
class min_heap:
    def __init__(self):
        self.a = []
    def __str__(self):
        return str(self.a)
    # we need subscripts from 0 through N-1, not 1 through N, so tweak
    def _parent_idx(self, i):
        if i <= 0:
            return -1
        else:
            return (i + 1) // 2 - 1  # 1 and 2 map to 0, etc.
    def _left_idx(self, i):
        return (i + 1) * 2 - 1       # 0 maps to 1, etc.
    def _right_idx(self, i):
        return (i + 1) * 2           # 0 maps to 2, etc.
    def add(self, val):
        self.a.append(val)
        # swap upward to maintain min heap property
        v_idx = self.size() - 1
        p_idx = self._parent_idx(v_idx)
        while p_idx >= 0 and val < self.a[p_idx]:
            self.a[p_idx], self.a[v_idx] = self.a[v_idx], self.a[p_idx]
            v_idx = p_idx
            p_idx = self._parent_idx(v_idx)
    def pop(self):
        # this will throw exception if len(a) == 0, caller should check first or try/except
        ret_val = self.a[0]
        self.a[0] = self.a[-1]  # last element in self.a
        self.a.pop(-1)
        # swap downward to maintain min heap property
        p_idx = 0
        lf_idx = self._left_idx(p_idx)
        rt_idx = self._right_idx(p_idx)
        # when there is no left child remaining, we are done
        while lf_idx < self.size():
            # swap with minimum child
            min_idx = lf_idx if (rt_idx >= self.size()) or (self.a[lf_idx] < self.a[rt_idx]) else rt_idx
            # if current node is less than (or equal to) minimum child, we are done
            if self.a[p_idx] <= self.a[min_idx]:
                return ret_val
            if min_idx == lf_idx:
                self.a[p_idx], self.a[lf_idx] = self.a[lf_idx], self.a[p_idx]
                p_idx = lf_idx
            else:  # min_idx == rt_idx
                self.a[p_idx], self.a[rt_idx] = self.a[rt_idx], self.a[p_idx]
                p_idx = rt_idx
            lf_idx = self._left_idx(p_idx)
            rt_idx = self._right_idx(p_idx)
        return ret_val
    def size(self):
        return len(self.a)
    def print_pretty(self):
        # print(self.a) # for testing
        if self.size() == 0:
            print('empty heap')
            return
        # maximum line width depends on tree depth
        tree_depth = math.ceil(math.log(self.size() + 1,2))  # 1 node: 1; 2,3 nodes: 2; 4,5,6,7 nodes: 3; etc. 
        val_width = 4  # between 0 and 1000: 4 characters wide
        # we want at least 1 space on either side of a 4-char-wide value (0 through 1000)
        line_width = (1 + val_width + 1) * 2 ** (tree_depth - 1)
        for cur_depth in range(1, tree_depth + 1):
            field_width = int(line_width / (2 ** (cur_depth - 1)))
            line = ''
            for i in range(2 ** (cur_depth - 1) - 1, min(self.size(), 2 ** cur_depth - 1)): # 0; 1,2; 3,4,5,6; 7-14; 15-30; etc.
                # center the value in the field: '^'
                val_str = ('{:^' + str(field_width) + 'd}').format(self.a[i])
                line += val_str
            print(line, '\n')  # extra blank line makes tree a little easier to read

# 1.b
def heapsort(a):
    h = min_heap()
    for v in a:
        h.add(v)
    for i in range(len(a)):
        a[i] = h.pop()

def test_heapsort():
    # 1.b -- quick heapsort testing code
    import random
    a = [random.randint(0,1000) for i in range(1000)]
    b = a.copy()
    b.sort()
    heapsort(a)
    if a == b:
        print('heapsort seems to work')
    else:
        print('heapsort does NOT work')

def test_min_heap():
    import random
    random.seed(0)    # we need repeatable randomness
    h = min_heap()    # create a new empty min_heap
    results = []
    for i in range(40):
        for j in range(10):
            h.add(random.randint(0,1000))
        if i <= 3:
            h.print_pretty()
        results.append(h.pop())
        print('iteration {:2d}: size: {:5d}'.format(i,h.size()))
    print('results:', results)

if __name__ == '__main__':
    test_min_heap()
    test_heapsort()
    
