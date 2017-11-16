class BinaryTree:
    class _BTNode:
        def __init__(self, value, left = None, right = None):
            self._value = value
            self._left = left
            self._right = right
    def __init__(self):
        self._top = None
    def insert(self, value):
        if self._top == None:
            self._top = BinaryTree._BTNode(value)
        else:
            self._insert_help(self._top, value)
    def _insert_help(self, cur_node, value):
        if value < cur_node._value:
            if cur_node._left == None:
                cur_node._left = BinaryTree._BTNode(value)
            else:
                self._insert_help(cur_node._left, value)
        elif value > cur_node._value:
            if cur_node._right == None:
                cur_node._right = BinaryTree._BTNode(value)
            else:
                self._insert_help(cur_node._right, value)
    def __str__(self):
        return self._str(self._top)
    def _str(self, cur_node):
        if cur_node == None:
            return '';
        else:
            left_str = self._str(cur_node._left)
            right_str = self._str(cur_node._right)
            ret = str(cur_node._value)
            if left_str:
                ret = left_str + ' ' + ret
            if right_str:
                ret = ret + ' ' + right_str
            return ret
    def size(self):
        return self._size_help(self._top)
    def _size_help(self, cur_node):
        if cur_node == None:
            return 0
        else:
            return 1 + self._size_help(cur_node._left) + self._size_help(cur_node._right)
    def depth(self):
        return self._depth_help(self._top)
    def _depth_help(self, cur_node):
        if cur_node == None:
            return 0
        else:
            return 1 + max(self._depth_help(cur_node._left), self._depth_help(cur_node._right))
    def print_pretty(self):
        self._print_pretty_help(self._top, 0)
    def _print_pretty_help(self, cur_node, level):
        if cur_node != None:
            self._print_pretty_help(cur_node._right, level + 1)
            print('    ' * level, cur_node._value)
            self._print_pretty_help(cur_node._left, level + 1)
            

# test code:

bt = BinaryTree()
print(bt)
print(bt.size())
print(bt.depth())
bt.insert(7)
bt.insert(3)
bt.insert(2)
bt.insert(13)
bt.insert(9)
bt.insert(3)
print(bt)
print(bt.size())
print(bt.depth())
bt.print_pretty()
